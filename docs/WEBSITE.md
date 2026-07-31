# Website publication

The Taxon Bridge product, privacy, and support site is served by GitHub Pages
from the static files in `website/`.

## Public URLs

- Product and marketing: <https://taxon.axelgraff.fr/>
- Privacy policy: <https://taxon.axelgraff.fr/privacy/>
- Support: <https://taxon.axelgraff.fr/support/>

The GitHub project-site fallback is
<https://axel58170.github.io/taxon-site/>.

## Deployment

`.github/workflows/pages.yml` publishes `website/` whenever a website or
deployment-workflow change reaches `main`. Configure GitHub Pages to use
**GitHub Actions** as its source.

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
