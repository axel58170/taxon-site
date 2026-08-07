#!/bin/bash

set -euo pipefail

usage() {
  echo "Usage: scripts/publish_site.sh --build-only | --publish" >&2
}

case "${1:-}" in
  --build-only)
    publish=false
    ;;
  --publish)
    publish=true
    ;;
  *)
    usage
    exit 2
    ;;
esac

if [[ $# -ne 1 ]]; then
  usage
  exit 2
fi

repository_root=$(git rev-parse --show-toplevel)
cd "$repository_root"

if [[ -n "$(git status --porcelain --untracked-files=all)" ]]; then
  echo "Refusing to build or publish from a dirty checkout." >&2
  exit 1
fi

current_branch=$(git symbolic-ref --quiet --short HEAD || true)
source_commit=$(git rev-parse HEAD)
if [[ "$publish" == true ]]; then
  if [[ "$current_branch" != "main" ]]; then
    echo "Refusing to publish from '$current_branch'; check out main." >&2
    exit 1
  fi

  git fetch origin main
  remote_main=$(git rev-parse origin/main)
  if [[ "$source_commit" != "$remote_main" ]]; then
    echo "Refusing to publish: main does not match origin/main." >&2
    exit 1
  fi
fi

python3 -m unittest discover -s tests -v
container system start

generated_site="$repository_root/_site"
if [[ "$generated_site" != "$repository_root/_site" ]]; then
  echo "Unexpected generated-site path." >&2
  exit 1
fi
rm -rf "$generated_site"

container run --rm \
  --platform linux/amd64 \
  --rosetta \
  --volume "$repository_root:/github/workspace" \
  --workdir /github/workspace \
  --entrypoint jekyll \
  jekyll/jekyll:4.2.2 \
  build --disable-disk-cache --source website --destination _site

python3 scripts/validate_site.py "$generated_site"

if [[ "$publish" == false ]]; then
  echo "Validated site for $source_commit; publication skipped."
  exit 0
fi

current_branch=$(git symbolic-ref --quiet --short HEAD || true)
current_commit=$(git rev-parse HEAD)
if [[ "$current_branch" != "main" || "$current_commit" != "$source_commit" || -n "$(git status --porcelain --untracked-files=all)" ]]; then
  echo "Refusing to publish: the source checkout changed during validation." >&2
  exit 1
fi

git fetch origin main
latest_remote_main=$(git rev-parse origin/main)
if [[ "$source_commit" != "$latest_remote_main" ]]; then
  echo "Refusing to publish: origin/main advanced during validation." >&2
  exit 1
fi

publish_worktree=$(mktemp -d "${TMPDIR:-/tmp}/taxon-site-publish.XXXXXX")
worktree_registered=false
cleanup() {
  if [[ "$worktree_registered" == true ]]; then
    git worktree remove --force "$publish_worktree" >/dev/null 2>&1 || true
  else
    rm -rf "$publish_worktree"
  fi
}
trap cleanup EXIT

if git ls-remote --exit-code --heads origin refs/heads/gh-pages >/dev/null 2>&1; then
  git fetch origin refs/heads/gh-pages
  git worktree add --detach "$publish_worktree" FETCH_HEAD
else
  git worktree add --detach "$publish_worktree" "$source_commit"
fi
worktree_registered=true

find "$publish_worktree" -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf -- {} +
cp -R "$generated_site/." "$publish_worktree/"
touch "$publish_worktree/.nojekyll"
printf '%s\n' 'taxon.axelgraff.fr' > "$publish_worktree/CNAME"

git -C "$publish_worktree" add --all
if git -C "$publish_worktree" diff --cached --quiet; then
  echo "Validated site already matches the published branch."
  exit 0
fi

git -C "$publish_worktree" commit -m "Publish site from ${source_commit:0:12}"
git fetch origin main
final_remote_main=$(git rev-parse origin/main)
if [[ "$source_commit" != "$final_remote_main" ]]; then
  echo "Refusing to publish: origin/main advanced while preparing publication." >&2
  exit 1
fi
git -C "$publish_worktree" push origin HEAD:refs/heads/gh-pages
echo "Published validated site from $source_commit to origin/gh-pages."
