# Website publication

The Taxon Bridge product, privacy, and support site is served by GitHub Pages.
Page content is Markdown in `website/`; Jekyll combines it with the layouts and
includes in that directory to generate the published HTML.

## Public URLs

- Product and marketing: <https://taxon.axelgraff.fr/>
- Privacy policy: <https://taxon.axelgraff.fr/privacy/>
- Support: <https://taxon.axelgraff.fr/support/>

The GitHub project-site fallback is
<https://axel58170.github.io/taxon-site/>.

## Deployment

For normal prose changes, edit the appropriate `.md` file under `website/`.
Keep its YAML front matter intact. Reusable navigation, metadata, and media
markup belongs in `_layouts/` and `_includes/`, while images and styles belong
in `assets/`.

`.github/workflows/pages.yml` builds and validates the generated `_site/` on
website pull requests. It uploads and deploys `_site/` only when a change
reaches `main` or the workflow is run manually. Configure GitHub Pages to use
**GitHub Actions** as its source.

## Local build and validation

From the repository root on an Apple silicon Mac with macOS 26 or later, start
[Apple Container](https://github.com/apple/container) and use the compatible
GitHub Pages Jekyll builder image below. The image is Linux/AMD64, so this
command enables Rosetta translation. The build's metadata plugin also needs a
GitHub token; the command reads the existing GitHub CLI credential without
printing or storing it:

```sh
container system start
container run --rm \
  --platform linux/amd64 \
  --rosetta \
  --volume "$PWD:/github/workspace" \
  --workdir /github/workspace \
  --env GITHUB_WORKSPACE=/github/workspace \
  --env INPUT_SOURCE=./website \
  --env INPUT_DESTINATION=./_site \
  --env INPUT_TOKEN="$(gh auth token)" \
  --env GITHUB_REPOSITORY=axel58170/taxon-site \
  --env INPUT_BUILD_REVISION=local \
  --env GITHUB_API_URL=https://api.github.com \
  --env INPUT_VERBOSE=true \
  --env INPUT_FUTURE=false \
  ghcr.io/actions/jekyll-build-pages:v1.0.13
python3 scripts/validate_site.py _site
```

The validator requires the three public routes, stable support-page anchors,
valid internal links and assets, and accessible animated demonstrations with
reduced-motion fallbacks. `_site/` is generated output and should not be
committed.

The Pages custom domain is `taxon.axelgraff.fr`. Its DNS record is:

| Type | Name | Target |
| --- | --- | --- |
| CNAME | `taxon` | `axel58170.github.io` |

After GitHub validates DNS and provisions the certificate, enable
**Enforce HTTPS**.

## Deployment verification

After every deployment:

1. Confirm the Pages workflow succeeds on `main`.
2. Open `/`, `/privacy/`, and `/support/` over HTTPS without authentication.
3. Check navigation, the support email, media, and external links.
4. Confirm the custom domain serves a valid HTTPS certificate.
