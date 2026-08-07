---
layout: default
title: Beta testing — Taxon Bridge
description: A practical guide for testing Taxon Bridge on iPhone through TestFlight.
document: true
footer_link: privacy
---

<p class="eyebrow">TestFlight</p>

# Beta testing guide

Thank you for testing Taxon Bridge. These checks focus on real iPhone behavior
that automated tests cannot reproduce completely. You do not need to complete
every section: report which sections you tried and anything that surprised you.

Before starting, install the current build from TestFlight and launch Taxon
Bridge once. In TestFlight, note the app version and build number so they can be
included in a report.

## Everyday lookup

1. Search for a common name you know and a scientific name such as
   `Pernis apivorus`.
2. If several taxa are offered, select the intended one and confirm the app does
   not choose silently.
3. Change the configured language order and scientific-name position. Repeat a
   search and confirm the result follows those settings.
4. Copy one name and then all available names, paste them elsewhere, and check
   the order and spelling.
5. Open an available Wikipedia link, return to Taxon Bridge, and start another
   search.
6. Relaunch the app and confirm settings and recent results persist.

## Bundled names, caching, and Airplane Mode

Taxon Bridge includes a small vocabulary that works without a connection. It
also stores successful recent lookups on the device. Run these steps in order
to test the two behaviors separately.

1. With networking available, open **Settings → Offline data**, choose
   **Clear recent results**, and confirm **Recent taxa** is empty.
2. Enable Airplane Mode and make sure Wi-Fi is off. Search for the bundled
   scientific name `Panthera leo`. Confirm the taxon and its available common
   names appear promptly. A Wikipedia link or image may be unavailable because
   those details normally come from the network.
3. Still offline, search for the non-bundled scientific name `Equus zebra`,
   provided you have not previously used it on this installation. Confirm Taxon
   Bridge reports an understandable connection problem instead of hanging or
   showing an unrelated result. If you have used that name, record and use a
   different non-bundled scientific name for the remaining steps.
4. Disable Airplane Mode and retry that exact query. Confirm it resolves and
   appears in **Recent taxa**.
5. Relaunch Taxon Bridge, enable Airplane Mode again, and repeat the query.
   Confirm the cached result and its name ordering remain available. If an image
   loaded online, check whether it remains available too.
6. Open the same result from **Recent taxa** while still offline.
7. Disable Airplane Mode and clear recent results again. Confirm the result is
   removed from **Recent taxa**, while `Panthera leo` continues to work in
   Airplane Mode.

iOS may independently retain recent web responses even after Taxon Bridge
clears its own cache. If a cleared query still works offline, report that
outcome; it does not necessarily mean clearing failed.

## Share Extension

1. In Safari or Notes, select only a biological name, choose **Share**, then
   choose **Taxon Bridge**.
2. Confirm the extension receives the selected text, resolves it, and displays
   names in the same configuration as the main app.
3. Try both a common name and a scientific name. If a result is ambiguous,
   confirm you can choose the intended taxon.
4. Copy a displayed name, paste it elsewhere, then close the extension and
   confirm you return to the source app.
5. Resolve a non-bundled name in the main app, enable Airplane Mode, and share
   that same text. Confirm the extension can use the shared cached result.
6. Still offline, share `Panthera leo`, then share a never-used non-bundled
   taxon. The bundled name should resolve; the uncached name should fail clearly
   rather than hang.
7. If you use Merlin Bird ID, share a public species page to Taxon Bridge and
   confirm the expected bird resolves.

Apple Books does not currently offer Taxon Bridge's Share Extension for selected
book text. Use the [Shortcut procedure on the Support page]({{ '/support/#apple-books-use-a-shortcut' | relative_url }})
for that scenario.

## Shortcuts

After launching Taxon Bridge once:

1. Run **Resolve Taxon** with `Pernis apivorus`.
2. Pass its result to **Get Taxon Name** with the language code `fr`.
3. Pass it to **Get Configured Taxon Names** and compare the order with the app.
4. Try an ambiguous name and confirm Shortcuts asks you to choose.
5. Request a language without an available common name and confirm the absence
   is clear.
6. Repeat one warmed lookup and one never-used lookup in Airplane Mode.

## Languages and accessibility

If possible, repeat a representative app and Share Extension lookup in the
interface languages you use. Check that text is understandable and does not
clip or overlap.

Also try light and dark appearance, the largest Dynamic Type size you normally
use, and VoiceOver. Check focus order, labels, hints, adjustable controls, and
copy or open actions. Important status should not be communicated by color
alone.

## Report a result

Send private reports to [taxon@axelgraff.fr](mailto:taxon@axelgraff.fr), or
file a non-sensitive report in [GitHub Issues](https://github.com/axel58170/taxon-site/issues).
Please include:

- Taxon Bridge version and build from TestFlight;
- iPhone model and iOS version;
- the section and steps tested;
- the exact taxon query or public species-page URL, when safe to share;
- expected and actual behavior;
- whether networking or Airplane Mode was active;
- interface language and relevant accessibility settings;
- a screenshot or screen recording when it contains no sensitive material.

Do not submit private information, personal identifiers, confidential text,
copyrighted reading passages, or screenshots containing sensitive content.
