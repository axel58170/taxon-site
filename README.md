# Taxon Bridge website

This repository contains the public Taxon Bridge product, privacy, and support
website. Its content is written in Markdown under `website/`, built locally with
Jekyll, and published from the generated `gh-pages` branch. Shared HTML is kept
in layouts and includes, so ordinary text changes do not require editing page
markup.

- Live site: <https://taxon.axelgraff.fr/>
- Privacy policy: <https://taxon.axelgraff.fr/privacy/>
- Support: <https://taxon.axelgraff.fr/support/>
- Deployment notes: [docs/WEBSITE.md](docs/WEBSITE.md)
- Support-media guidance: [docs/SUPPORT_MEDIA.md](docs/SUPPORT_MEDIA.md)

Content and asset rights are described in [COPYRIGHT.md](COPYRIGHT.md).

For a content-only update, edit the relevant Markdown file in `website/`, run
`scripts/publish_site.sh --build-only`, and open a pull request. After the change
is reviewed and merged, an authorized maintainer runs
`scripts/publish_site.sh --publish` from the updated clean `main` branch. The
repository contains no GitHub Actions workflow; GitHub Pages may still report
its platform-managed deployment run after `gh-pages` is updated. See the
deployment notes for safeguards, setup, rollback, and verification.
