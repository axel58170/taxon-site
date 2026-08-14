---
layout: default
title: Privacy Policy — Taxon Translate
description: How Taxon Translate handles lookup information and data stored on your device.
document: true
current_nav: privacy
footer_link: support
---

<p class="eyebrow">Privacy</p>

# Taxon Translate Privacy Policy

<p class="meta"><strong>Effective date:</strong> 13 August 2026</p>

## Privacy at a glance

Taxon Translate has no account, advertising, analytics, tracking, or developer server. Your settings and recent results are stored on your device.

For an online lookup, the app sends the information needed to find the matching taxon and its names directly to Catalogue of Life and Wikimedia services. Those services receive ordinary connection information and may retain it under their own privacy policies—normally up to 30 days on GBIF infrastructure and up to 90 days on Wikimedia services, subject to their published exceptions.

## What you share for a lookup

When you look up a common or scientific name, Taxon Translate uses the text or web link you provide and the languages you have selected. You can enter a lookup in the app, share it through the iOS Share Sheet, or supply it to a Shortcut.

The Share Extension reads only text or a web URL that you explicitly share with it. It does not change the item you shared. The lookup text or link and its result may be stored on your device as described below.

For a supported Merlin Bird ID species-page URL, Taxon Translate extracts the eBird species code from the URL. For a supported localized Wikipedia article URL, Taxon Translate extracts the article title and asks that Wikipedia site’s structured API for its linked Wikidata ID.

## Online services used for a lookup

For online lookups, Taxon Translate sends the information needed to find the matching taxon and its names directly to the services below. These requests use HTTPS.

- Catalogue of Life infrastructure at `api.checklistbank.org` normally receives the original lookup text first, along with scientific names or Catalogue of Life identifiers needed to retrieve classification and names. A supported Wikipedia article URL bypasses this text search.
- The localized Wikipedia host from a supported article URL receives the decoded article title in a structured metadata request. Taxon Translate reads only the linked Wikidata ID; it does not download or parse the article HTML.
- Wikidata at `www.wikidata.org` and `query.wikidata.org` receives the original lookup text when fallback search is needed. It also receives selected language codes, bounded candidate Q-IDs, scientific names, and Q-IDs needed to check identities and retrieve names and Wikipedia links. For a supported Merlin species-page URL, Wikidata receives the extracted eBird species code in an exact `P3444` lookup.
- After the app displays a taxon, Wikidata receives its Q-ID to find a representative image. Wikimedia Commons receives the media filename needed to return attribution and a display-sized thumbnail. The names remain visible if no image is requested or available.

The services receive the request data above and ordinary connection information such as your IP address, request time, and the app’s User-Agent. Search text is included in HTTPS query parameters and may appear in service logs. Taxon Translate has no intermediary server and cannot inspect or delete those logs.

Catalogue of Life’s API is provided on GBIF infrastructure. GBIF says technical information collected when its internet services are used is normally deleted after 30 days. Wikimedia says automatically collected personal information is normally deleted, aggregated, or de-identified within 90 days. Both providers describe exceptions in their policies, including circumstances in which information may be retained longer.

- [Catalogue of Life](https://www.catalogueoflife.org/)
- [GBIF privacy policy](https://www.gbif.org/terms/privacy-policy)
- [Wikimedia privacy policy](https://foundation.wikimedia.org/wiki/Policy:Privacy_policy)
- [Wikimedia data retention guidelines](https://foundation.wikimedia.org/wiki/Legal:Wikimedia_Foundation_Data_Retention_Guidelines/en)

Taxon Translate sends no app-created account identifier, advertising identifier, contact details, or precise location to these services.

## What stays on your device

Taxon Translate stores the following in its shared iOS container so the app and Share Extension can use the same settings and recent results:

- your ordered language codes, scientific-name position, and preferred Wikipedia language;
- normalized lookup text, canonicalized Wikipedia host-and-title URLs with query parameters and fragments removed, and the ordered languages used for each lookup;
- lookup timestamps;
- matching or candidate taxa, including Q-IDs, scientific names, ranks, names and their sources, and Wikipedia links;
- representative image bytes, source metadata, attribution, and retrieval timestamps.

Fresh lookup results may be reused for 30 days. Records remain on the device until you choose **Clear recent results**, delete Taxon Translate, or iOS otherwise removes its container. Clearing recent results does not reset your language settings.

Representative image metadata and display-sized image bytes are cached for 30 days in a cache limited to 64 MiB and 128 entries. An older image may remain available offline for up to 90 days. A missing-image result is stored for 24 hours to avoid repeated requests. **Clear recent results** also removes this image cache.

In addition to the shared lookup result described above, when the Share Extension displays a result it creates a separate handoff record so the app can open that taxon. This record contains only the selected Wikidata Q-ID and a timestamp. It stays on your device until the app next reads it. The app then removes the record and ignores it if it is more than one hour old.

iOS may separately retain HTTPS responses in its system URL cache and remove them automatically. Taxon Translate does not use iCloud or another cloud service to synchronize its data.

## Clipboard, Shortcuts, and external links

Taxon Translate writes names to the iOS clipboard only when you choose a copy action. Clipboard handling and access by other apps are controlled by iOS.

Inputs and outputs used with Siri or Shortcuts may also be processed by Apple under Apple’s privacy policies.

When you open Wikipedia, Catalogue of Life, citation, licence, contribution, or privacy-policy links, iOS opens the destination in your browser. The destination receives ordinary web request information under its own privacy policy.

## What Taxon Translate does not do

Taxon Translate has no account or sign-in, advertising or analytics SDK, tracking, sale of personal information, push notifications, cloud backend, or developer-operated server. It does not share information with unrelated third parties. Catalogue of Life and Wikimedia are used only for lookups you request.

Taxon Translate does not access your contacts, photos, camera, microphone, location, health data, or advertising identifier.

## Control your data

You can clear stored lookups and images in **Settings → Offline data → Clear recent results**. You can change or remove selected languages in Settings. Deleting Taxon Translate removes its app container from the device according to normal iOS behavior.

Avoid entering confidential or personal information as a biological-name search.

## Changes and contact

This policy will be updated when the app’s data practices change. The effective date above identifies the current version.

For privacy questions or deletion assistance, email [taxon@axelgraff.fr](mailto:taxon@axelgraff.fr). Public bug reports may also be filed at [GitHub Issues](https://github.com/axel58170/taxon-site/issues), but do not include confidential or personal information in a public GitHub issue.
