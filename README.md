# Taxon Bridge website

This repository contains the public Taxon Bridge product, privacy, and support
website. Its content is written in Markdown under `website/`, built with Jekyll,
and deployed through GitHub Pages. Shared HTML is kept in layouts and includes,
so ordinary text changes do not require editing page markup.

- Live site: <https://taxon.axelgraff.fr/>
- Privacy policy: <https://taxon.axelgraff.fr/privacy/>
- Support: <https://taxon.axelgraff.fr/support/>
- Deployment notes: [docs/WEBSITE.md](docs/WEBSITE.md)
- Support-media guidance: [docs/SUPPORT_MEDIA.md](docs/SUPPORT_MEDIA.md)

Content and asset rights are described in [COPYRIGHT.md](COPYRIGHT.md).

For a content-only update, edit the relevant Markdown file in `website/` and
open a pull request. The Pages workflow builds and validates every website pull
request; deployment happens only from `main` or a manual workflow run. See the
deployment notes for the local build and validation commands.
