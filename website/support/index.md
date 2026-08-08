---
layout: default
title: Support — Taxon Bridge
description: Taxon Bridge support and troubleshooting.
document: true
current_nav: support
footer_link: privacy
---

<p class="eyebrow">Help</p>

# Support and troubleshooting

- **Private support:** Email [taxon@axelgraff.fr](mailto:taxon@axelgraff.fr).
- **Public bug reports:** File an issue at [GitHub Issues](https://github.com/axel58170/taxon-site/issues).
- **TestFlight participants:** Follow the [beta testing guide]({{ '/beta-testing/' | relative_url }}).

  <p class="note">Do not include private information, personal identifiers, confidential text, or screenshots containing sensitive content in a public issue.</p>

## Before you start

If you come across an unfamiliar name while reading, select it and use the Share Sheet to send it to Taxon Bridge. Taxon Bridge shows the names in an overlay. Close the overlay to continue reading exactly where you left off.

If you want to see the image and other details, close the overlay and open Taxon Bridge within the next hour. The app will open the same taxon.

### 1. Choose your languages

Open Taxon Bridge once, then open **Settings → Languages**. Choose the languages whose common names you want to see and place them in your preferred order.

{% include static-figure.html image="/assets/support/language-order.webp" alt="Taxon Bridge language settings showing English, French, and Dutch in the selected order." caption="Choose the common-name languages you want to see and arrange them in your preferred order." %}

### 2. Add Taxon Bridge to the Share Sheet

1. In an iPhone app that lets you share selected text—for example, Safari or Notes—select the name of an animal, plant, or fungus and choose **Share**.
2. If Taxon Bridge is not visible, scroll through the Share Sheet and choose **More**.
3. Add Taxon Bridge to the preferred actions and move it near the front if desired.

You can now look up selected names, birds on Merlin Bird ID species pages, and animals, plants, or fungi on Wikipedia article pages.

### 3. Add Taxon Bridge to Shortcuts

Open Shortcuts and choose **Add Action → Apps → Taxon Bridge**. The available actions can be combined with other Shortcut actions:

- **Resolve Taxon** accepts a common or scientific name and finds the matching animal, plant, or fungus. If several matches are possible, it asks you to choose.
- **Get Taxon Name** takes that result and returns its common name in one language. Enter a language code such as `fr`, `nl`, or `en-GB`.
- **Get Configured Taxon Names** takes that result and shows the common names in your configured languages, plus the scientific name. Choose **Open in Taxon Bridge** to continue in the full app, or dismiss the result to return to what you were doing.

The actions also return values for the next action in the Shortcut. Add **Copy to Clipboard** if you want to paste the names elsewhere.

## Using Taxon Bridge

### Look up a name while reading

1. In an iPhone app that lets you share selected text—for example, Safari or Notes—select the name of an animal, plant, or fungus.
2. Choose **Share** from the selection menu.
3. Choose **Taxon Bridge** in the system Share Sheet.
4. Review the sourced names in your configured languages and the scientific name.

{% include motion-figure.html class="support-media" animation="/assets/support/share-selected-name.gif" animation_alt="Animated walkthrough showing Hazelaar selected on a Wikipedia page in Safari, the text-selection actions, the Share Sheet with Taxon Bridge, and the multilingual result. Tap indicators mark the menu arrow, Share, and Taxon Bridge." poster="/assets/support/share-selected-name-poster.webp" poster_alt="The iPhone Share Sheet showing Taxon Bridge as an option for Hazelaar selected on a Wikipedia page." caption="Select a name while reading, reveal Share if necessary, choose Taxon Bridge, and review the configured names." %}

### Look up a bird from a Merlin page

1. Open a public species page in Merlin Bird ID or on the Merlin website.
2. Choose **Share**, then choose **Taxon Bridge** in the system Share Sheet.
3. Review the sourced names in your configured languages and the scientific name.

{% include motion-figure.html class="support-media" animation="/assets/support/share-merlin-page.gif" animation_alt="Animated walkthrough showing a European Goldfinch in Merlin Bird ID, the Share Sheet with Taxon Bridge, and the multilingual result. Tap indicators mark Share and Taxon Bridge." poster="/assets/support/share-merlin-page-poster.webp" poster_alt="The iPhone Share Sheet showing Taxon Bridge as an option for a European Goldfinch shared from Merlin Bird ID." caption="Share a bird from Merlin Bird ID to Taxon Bridge. Taxon Bridge is not affiliated with or endorsed by Merlin Bird ID, eBird, or the Cornell Lab of Ornithology." %}

### Look up a taxon from a Wikipedia article {#share-wikipedia-article}

From a Wikipedia article about an animal, plant, or fungus, Taxon Bridge can find the linked taxon and show its names in your languages. You do not need to select or copy the article title.

1. Open the article in Wikipedia or Safari.
2. Choose **Share**, then choose **Taxon Bridge** in the system Share Sheet.
3. Review the sourced names in your configured languages and the scientific name.

This also provides a way to look up names after Apple Visual Intelligence identifies an organism. Open the Visual Intelligence result in Wikipedia, choose **Share**, and then choose **Taxon Bridge**. Visual Intelligence does not currently offer Taxon Bridge directly, so its Wikipedia result is the available route into the lookup.

Taxon Bridge accepts localized article URLs such as `https://en.wikipedia.org/wiki/Acer_campestre`. It uses the article's structured Wikipedia identity rather than guessing from its title or parsing the page text. Pages without a linked biological taxon return no result.

### Look up a copied species with a Shortcut {#apple-books-use-a-shortcut}

The **Lookup Species** Shortcut lets you look up a species you have copied to the clipboard. This works in Books and anywhere else you can copy text.

Select the species name and tap **Copy**. Then run **Lookup Species**.

You can run it from the Shortcuts app, add it to your Home Screen, assign it to the Action button, or use Back Tap.

<a class="text-link" href="https://www.icloud.com/shortcuts/3dcca758ad0d40aaa2f4c8d2ef2ec471">Add the Lookup Species Shortcut</a>

Apple Books does not currently show third-party Share or Action extensions, including Taxon Bridge, for selected book text—even when the book allows sharing. This limitation is controlled by Books; an [Apple Frameworks Engineer describes its predefined recipient list](https://developer.apple.com/forums/thread/762784).

## Troubleshooting

### Which languages are supported? {#which-languages-can-i-add}

Taxon Bridge lets you add many languages in **Settings → Languages** by entering a language name or an ISO 639 standard language code. However, not every language in the world is supported.

The available names come from Catalogue of Life and Wikidata. Taxon Bridge displays the common names recorded in these sources and cannot create or translate missing names.

### Why does a selectable language have few or no names? {#why-does-a-selectable-language-have-few-or-no-names}

A language may be available for selection even when the source databases contain few meaningful entries for it. Coverage varies widely by language and taxon: some languages have extensive common-name data, while others have only a handful of names or none at all.

If a name has not been recorded in Catalogue of Life or Wikidata, Taxon Bridge displays “Not available.” See [One of my languages says “Not available”](#name-not-available) for more information.

### The result is not what I expected

- Try a longer or more specific name. If you know the scientific name, use it.
- If Taxon Bridge shows several possibilities, review them and choose the one that matches what you are reading about.
- Confirm the device has an internet connection when looking up a name for the first time.
- If Catalogue of Life or Wikidata is temporarily busy or unavailable, wait a few minutes and try again. These are the online services Taxon Bridge uses to find and verify names.
- If the problem continues, report the name you entered, the result you expected, the app language, version, and build without including personal information.

### One of my languages says “Not available” {#name-not-available}

Taxon Bridge does not invent or automatically translate names. It shows common names recorded by Catalogue of Life and Wikidata. The same animal, plant, or fungus may not have a recorded common name in every language, so the app shows **Not available** while still showing the scientific name.

If you know a commonly used name that is missing, first check the taxon's record in [Catalogue of Life](https://www.catalogueoflife.org/). If the name is missing there, [contact Catalogue of Life](https://www.catalogueoflife.org/howto/contribute) so its source record can be corrected. Contact Taxon Bridge support only if the name is already recorded in Catalogue of Life but the app still shows **Not available**. Include the scientific name, language, expected common name, and a link to the Catalogue of Life record.

### Taxon Bridge cannot find the bird from a Merlin page

- Confirm the shared URL begins with `https://merlinbirds.org/species/`.
- Confirm networking is available.
- Open Taxon Bridge once, then try the Share action again.
- Report the public species-page URL and app build if the problem persists.

### Taxon Bridge cannot find a taxon from a Wikipedia article

- Confirm the shared page is an article on a localized Wikipedia host, such as `en.wikipedia.org` or `fr.wikipedia.org`.
- Confirm networking is available for the first lookup.
- Some Wikipedia pages do not have a linked Wikidata taxon; Taxon Bridge will not guess from the article title.
- Open Taxon Bridge once, then try the Share action again.
- Report the public article URL and app build if the problem persists.

### Offline results

Successful recent lookups can remain available for up to 30 days. Looking up a name that is not stored on the device requires an internet connection. Use **Settings → Offline data → Clear recent results** to delete the lookup cache.

### Privacy and deletion

The in-app policy is under **Settings → Privacy Policy**. Clear recent lookup data under **Settings → Offline data**, or delete Taxon Bridge to remove its app container according to normal iOS behavior.
