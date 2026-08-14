# Website publication

The Taxon Translate product, privacy, and support site is served by GitHub Pages.
Page content is Markdown in `website/`; Jekyll combines it with the layouts and
includes in that directory to generate the published HTML.

## Public URLs

- Product and marketing: <https://taxon.axelgraff.fr/>
- Privacy policy: <https://taxon.axelgraff.fr/privacy/>
- Support: <https://taxon.axelgraff.fr/support/>
- Beta testing guide: <https://taxon.axelgraff.fr/beta-testing/>

The GitHub project-site fallback is
<https://axel58170.github.io/taxon-site/>.

## Publication model

For normal prose changes, edit the appropriate `.md` file under `website/`.
Keep its YAML front matter intact. Reusable navigation, metadata, and media
markup belongs in `_layouts/` and `_includes/`, while images and styles belong
in `assets/`.

The repository contains no GitHub Actions workflow. Pull requests are validated
locally. After an accepted change reaches `main`, an authorized maintainer builds
and validates the site locally, then publishes only the generated output to the
`gh-pages` branch. GitHub Pages serves that branch without a repository-authored
workflow. GitHub may still display its own platform-managed Pages deployment run
after the branch is updated; that unavoidable run is the sole exception.

## Local build and validation

From a clean checkout on an Apple silicon Mac with macOS 26 or later, run:

```sh
scripts/publish_site.sh --build-only
```

Build-only validation accepts any clean branch. The script runs the Python
validator tests, starts Apple Container, builds with a pinned Jekyll image, and
validates `_site/`. The container receives no GitHub credentials. Publication
adds the stricter requirement that `main` is clean and equal to `origin/main`.

The validator requires the four public routes, stable support-page anchors,
valid internal links and assets, and accessible animated demonstrations with
reduced-motion fallbacks. `_site/` is generated output and should not be
committed on `main`.

## Publishing

After a reviewed change is merged, update the clean local `main` branch and run:

```sh
git pull --ff-only origin main
scripts/publish_site.sh --publish
```

Publication repeats every local validation gate, creates a detached temporary
worktree, replaces its contents with validated `_site/`, adds `.nojekyll` and
the production `CNAME`, and pushes the resulting commit to `origin/gh-pages`.
It refuses dirty, non-`main`, or out-of-date source checkouts. The temporary
worktree is removed on success or failure.

Configure the repository's Pages settings to **Deploy from a branch**, using
`gh-pages` and `/ (root)`. Keep the custom domain and HTTPS enforcement enabled.
The source `main` branch must never contain generated site output.

The Pages custom domain is `taxon.axelgraff.fr`. Its DNS record is:

| Type | Name | Target |
| --- | --- | --- |
| CNAME | `taxon` | `axel58170.github.io` |

After GitHub validates DNS and provisions the certificate, enable
**Enforce HTTPS**.

## Deployment verification

After every deployment:

1. Confirm `origin/gh-pages` points to the commit created for the intended
   `main` source SHA.
2. Open `/`, `/privacy/`, `/support/`, and `/beta-testing/` over HTTPS without
   authentication.
3. Check navigation, the support email, media, and external links.
4. Confirm the custom domain serves a valid HTTPS certificate.

## Rollback

Do not rewrite `main` or `gh-pages`. Revert the problematic source change on a
reviewed `main` branch, merge that revert, then run the normal publication
command again. This creates an auditable newer `gh-pages` commit containing the
restored site. If publication itself fails, the previous `gh-pages` commit
remains the served version; investigate locally before retrying.
