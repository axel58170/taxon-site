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

<p class="meta"><strong>Effective date:</strong> 6 October 2026</p>

## Privacy at a glance

Taxon Translate has no account, advertising, analytics, tracking, or developer
server. Your settings, recent results, favourites, and lists are stored on your
device.

For an online lookup, the app sends the information needed to find the matching
taxon and its names directly to Catalogue of Life and Wikimedia services. Those
services receive ordinary connection information and may retain it under their
own privacy policies—normally up to 30 days on GBIF infrastructure and up to 90
days on Wikimedia services, subject to their published exceptions.

## What you share for a lookup

When you look up a common or scientific name, Taxon Translate uses the text or web
link you provide and the languages you have selected. You can enter a lookup in
the app, share it through the iOS Share Sheet, or supply it to a Shortcut.

The Share Extension reads text, a web URL, or one image that you explicitly share
with it. It does not change the item you shared. Image text is recognized locally;
only names you select or correct, and possible singular spellings of those names,
are sent to lookup services. The selected lookup
text or link and its result may be stored on your device as described below.

A name found in the bundled vocabulary can be shown without sending the original
lookup text online. Displaying further names, Wikipedia links, or an image can
still request information from the services below.

For a supported Merlin Bird ID species-page URL, Taxon Translate extracts the
eBird species code from the URL and first checks its bundled mappings. If no
local match is available, the original URL can enter the online lookup pipeline.
For a supported localized Wikipedia article URL, Taxon Translate extracts the article title and asks that Wikipedia site's
structured API for its linked Wikidata ID.

## Online services used for a lookup

For online lookups, Taxon Translate sends the information needed to find the
matching taxon and its names directly to the services below. These requests use
HTTPS.

- Catalogue of Life infrastructure at `api.checklistbank.org` normally
  receives the original lookup text first, along with scientific names or
  Catalogue of Life identifiers needed to retrieve classification and names.
  A supported Wikipedia article URL bypasses this text search.
- The localized Wikipedia host from a supported article URL receives the
  decoded article title in a structured metadata request. Taxon Translate reads
  only the linked Wikidata ID; it does not download or parse the article HTML.
- Wikidata at `www.wikidata.org` and `query.wikidata.org` receives the original
  lookup text when fallback search is needed. It also receives selected
  language codes, bounded candidate Q-IDs, scientific names, and Q-IDs needed
  to check identities and retrieve names and Wikipedia links. It may also receive
  Catalogue of Life or Avibase identifiers and a scientific name to find a
  compatible Wikidata item for links and images. When a Merlin species-page URL
  needs online fallback, Wikidata receives the extracted eBird species code
  in an exact `P3444` lookup.
- After the app displays a taxon, Wikidata receives its Q-ID to find a
  representative image. Wikimedia Commons receives the media filename needed
  to return attribution and a display-sized thumbnail. The names remain visible
  if no image is requested or available.

When an eBird checklist lookup is enabled in the installed build, sharing a
checklist URL sends its checklist identifier to `api.ebird.org`, with a
build-configured API credential. Taxon reads the returned species codes and
matches them against its bundled vocabulary. It does not save the checklist
response, observer details, counts, or locations in its own data stores. Without
a configured credential, this lookup stops before making an eBird request.
The eBird service controls its own request logs; the retention periods below
refer to GBIF and Wikimedia only.

The services receive the request data above and ordinary connection
information such as your IP address, request time, and the app's User-Agent.
Search text is included in HTTPS query parameters and may appear in service
logs. Taxon Translate has no intermediary server and cannot inspect or delete
those logs.

Catalogue of Life's API is provided on GBIF infrastructure. GBIF says technical
information collected when its internet services are used is normally deleted
after 30 days. Wikimedia says automatically collected personal information is
normally deleted, aggregated, or de-identified within 90 days. Both providers
describe exceptions in their policies, including circumstances in which
information may be retained longer.

- [Catalogue of Life](https://www.catalogueoflife.org/)
- [GBIF privacy policy](https://www.gbif.org/terms/privacy-policy)
- [Wikimedia privacy policy](https://foundation.wikimedia.org/wiki/Policy:Privacy_policy)
- [Wikimedia data retention guidelines](https://foundation.wikimedia.org/wiki/Legal:Wikimedia_Foundation_Data_Retention_Guidelines/en)

Taxon Translate sends no app-created account identifier, advertising identifier,
contact details, or precise location to these services.

## What stays on your device

Taxon Translate stores the following in its shared iOS container so the app and
Share Extension can use the same settings and recent results:

- your ordered language codes, scientific-name position, and preferred
  Wikipedia language;
- normalized lookup text, canonicalized Wikipedia host-and-title URLs with
  query parameters and fragments removed, and the ordered languages used for
  each lookup;
- lookup timestamps;
- matching or candidate taxa, including optional Q-IDs, versioned taxon
  identifiers, scientific names, ranks, names and their sources, and Wikipedia
  links;
- exact mappings from a versioned taxon identifier to the compatible media
  identifier used for Wikipedia links and representative images;
- representative image bytes, source metadata, attribution, and retrieval
  timestamps;
- favourites and list titles, local list identifiers, taxon membership, wanted
  or seen status, and first and most recent seen dates when you mark an item seen.

Fresh lookup results and taxon-to-media mappings may be reused for 30 days.
Expired lookup records are removed during cache maintenance; they can remain
on the device until that maintenance runs or you clear the cache.
**Clear recent results** removes lookup records, taxon-to-media mappings, and
representative images. It does not reset your language settings or remove your
favourites and lists. List data has no automatic expiry and stays until you
change or remove its entries, delete Taxon Translate, or iOS otherwise removes
its container.

Fresh representative image metadata and display-sized image bytes are reused
for 30 days in a cache limited to 64 MiB and 128 entries. An older image may remain
available offline for up to 90 days from retrieval. A missing-image result is
reused for 5 minutes to avoid repeated requests. Cache maintenance removes
expired records; reaching the cache limits may remove them sooner.

In addition to the shared lookup result described above, when the Share
Extension displays a result it creates a separate handoff record so the app can
open that taxon. This record contains an event identifier, the selected
versioned taxon identifier and/or Wikidata Q-ID, and a timestamp. It stays in the shared app container until another handoff replaces it or the app
data is cleared. The app records a one-way fingerprint when it reads the
handoff, so the identity data is not duplicated and the handoff is not used
again. The app also ignores it if it is more than one hour old.

iOS may separately retain HTTPS responses in its system URL cache and remove
them automatically. Taxon Translate does not use iCloud or another cloud service
to synchronize its data.

## Clipboard, Shortcuts, and external links

Taxon Translate writes names to the iOS clipboard only when you choose a copy
action. Clipboard handling and access by other apps are controlled by iOS.

Inputs and outputs used with Siri or Shortcuts may also be processed by Apple
under Apple's privacy policies.

When you open Wikipedia, Catalogue of Life, citation, licence, contribution,
or privacy-policy links, iOS opens the destination in your browser. An explicit
Merlin action opens its species link through iOS in Merlin or your browser. The
destination receives ordinary web request information under its own privacy
policy.

## What Taxon Translate does not do

Taxon Translate has no account or sign-in, advertising or analytics SDK, tracking,
sale of personal information, push notifications, cloud backend, or
developer-operated server. It does not share information with unrelated third
parties. Catalogue of Life and Wikimedia are used only for lookups you request.

## Photos and text reading

Taxon Translate accesses the camera only after you choose **Take photo**, and the
photo library only through the system photo picker after you choose **Choose
photo**. The selected image is used transiently to identify the pictured organism;
Taxon does not save it. On supported devices, Apple's Foundation Models first
try to identify it on your device. When the local model is unavailable, lacks
the required image capabilities, or returns no identification, Taxon can send
the normalized image to Apple Private Cloud Compute if that service is enabled
and available. An ordinary local processing error does not trigger this cloud
fallback. Availability depends on the device, Apple Intelligence, and the
installed build's permissions. The same recognition service may receive an
image through Apple's Visual Intelligence interface.

Apple says Private Cloud Compute uses request data only to answer the request
and does not retain it after returning the response. See Apple's
[Private Cloud Compute privacy requirements](https://security.apple.com/documentation/private-cloud-compute/corerequirements).
Taxon does not send the image to its own server or another classifier. Up to
three suggested scientific names are checked through the ordinary lookup
services; these names and resulting taxa can enter the ordinary lookup cache.
There is no separate stored photo or recognition history.

When you choose **Read text from photo** or share a screenshot to Taxon,
Apple Vision reads the image text entirely on your device. You review and may
correct the text, then choose up to eight names for lookup. The image and full
recognized text stay in memory only for this flow; they are not saved or uploaded.
The names you explicitly choose use the ordinary lookup services and caches
described above. If a selected phrase has no match, Taxon may also send up to
two inferred singular spellings of that phrase to the same lookup services.
Any matching taxa remain choices for you to confirm. OCR does not use Foundation
Models or Private Cloud Compute.

Taxon Translate does not access your contacts, microphone, location, health data,
or advertising identifier. It does not request location metadata from your photo
library; identifying an organism uses the normalized image pixels.

## Control your data

You can clear stored lookups and images in **Settings → Offline data → Clear
recent results**. You can change or remove selected languages in Settings.
Deleting Taxon Translate removes its app container from the device according to
normal iOS behavior.

Avoid entering confidential or personal information as a biological-name
search.

## Changes and contact

This policy will be updated when the app's data practices change. The effective
date above identifies the current version.

For privacy questions or deletion assistance, email
[taxon@axelgraff.fr](mailto:taxon@axelgraff.fr). Public bug reports may also be
filed at [taxon-site issue tracker](https://github.com/axel58170/taxon-site/issues), but do not include
confidential or personal information in a public GitHub issue.
