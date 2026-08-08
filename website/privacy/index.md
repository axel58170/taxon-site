---
layout: default
title: Privacy Policy — Taxon Bridge
description: Taxon Bridge privacy policy.
document: true
current_nav: privacy
footer_link: support
---

<p class="eyebrow">Privacy</p>

# Taxon Bridge Privacy Policy

<p class="meta"><strong>Effective date:</strong> 24 July 2026</p>

Taxon Bridge is designed to look up biological names without an account, advertising, analytics, or user tracking. This policy explains the information processed when you use the app, Share Extension, or Shortcuts actions.

## Information you provide

When you search for a common or scientific name, Taxon Bridge processes the lookup text or web link and your configured output-language codes. Input can be entered in the app, shared through the iOS Share Sheet, or supplied to a Shortcut.

The Share Extension reads only text or a web URL that you explicitly share with it. It does not retain or modify the source item. For a supported Merlin Bird ID species-page URL, Taxon Bridge extracts the eBird species code from the URL.

## External naming services

Taxon Bridge sends lookup information over HTTPS to services needed to find a taxon and retrieve its names and other details:

- Catalogue of Life infrastructure at `api.checklistbank.org` normally receives the original lookup text first, along with scientific names or Catalogue of Life identifiers required to retrieve taxonomic and vernacular-name data.
- Wikidata at `www.wikidata.org` and `query.wikidata.org` receives the original lookup text when fallback discovery is needed. It also receives configured language codes, bounded candidate Q-IDs, scientific names, and Q-IDs needed for taxon verification, localized names, and Wikipedia links. For a supported Merlin species-page URL, Wikidata receives the extracted eBird species code in an exact `P3444` lookup.

Search text is transmitted in HTTPS query parameters and may therefore appear in those providers’ server logs. The providers also receive ordinary connection information such as your IP address, request time, and the app’s User-Agent. Taxon Bridge does not operate an intermediary server and does not receive those provider logs.

These independent services process requests under their own terms and privacy practices:

- [Catalogue of Life](https://www.catalogueoflife.org/)
- [Wikimedia privacy policy](https://foundation.wikimedia.org/wiki/Policy:Privacy_policy)

Taxon Bridge sends no app-created account identifier, advertising identifier, contact details, or precise location to these services.

## Information stored on your device

Taxon Bridge stores the following in the app’s shared iOS container so the main app and Share Extension can use the same configuration and recent results:

- your ordered language codes, scientific-name position, and preferred Wikipedia language;
- normalized lookup text and the ordered languages used for the lookup;
- lookup timestamps;
- matching or candidate taxa, including Q-IDs, scientific names, ranks, localized names and attribution, and Wikipedia links.

Cached results no older than 30 days may be used when a naming service is unavailable. Cache records remain on the device until you choose **Clear recent results**, remove the app, or iOS otherwise removes the app container. Clearing recent results does not reset your language preferences.

Taxon Bridge does not use iCloud or another cloud service to synchronize this information.

## Clipboard, Shortcuts, and external links

Taxon Bridge writes names to the iOS clipboard only when you choose a copy action. Clipboard handling and any access by other apps are controlled by iOS.

Inputs and outputs used with Siri or Shortcuts may also be processed by Apple under Apple’s privacy policies.

When you open Wikipedia, Catalogue of Life, citation, licence, or contribution links, iOS opens the destination in your browser. The destination receives ordinary web request information under its own privacy policy.

## Information Taxon Bridge does not collect

Taxon Bridge has:

- no account or sign-in;
- no advertising or analytics SDK;
- no tracking or sale of personal information;
- no push notifications or cloud backend;
- no access to contacts, photos, camera, microphone, location, health data, or the advertising identifier.

The app does not share information with unrelated third parties. Catalogue of Life and Wikimedia are used only as the external data sources necessary to perform requested lookups.

## Your choices

You can clear cached lookups in **Settings → Offline data → Clear recent results**. You can change or remove configured languages in Settings. Deleting Taxon Bridge removes its app container from the device according to normal iOS behavior.

Avoid entering confidential or personal information as a biological-name search.

## Changes and contact

This policy will be updated when the app’s data practices change. The effective date above identifies the current version.

For privacy questions or deletion assistance, email [taxon@axelgraff.fr](mailto:taxon@axelgraff.fr). Public bug reports may also be filed at [GitHub Issues](https://github.com/axel58170/taxon-site/issues), but do not include confidential or personal information in a public GitHub issue.
