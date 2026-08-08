# Support media

Use privacy-safe iPhone captures. Keep all instructions available as text so
the support page remains usable when media does not load.

## Decide whether a walkthrough helps

Add or replace a walkthrough only when motion explains a sequence that still
feels unclear in the written steps. Do not regenerate an accurate walkthrough
only because nearby copy changed.

Each walkthrough should cover one recognisable task from start to finish. Keep
setup, optional invocation methods, and troubleshooting in text rather than
combining them into the animation.

## Published stills

- `website/assets/support/language-order.webp`: language order and scientific
  name placement.
- `website/assets/support/share-selected-name-poster.webp`: reduced-motion
  fallback for the selected-text walkthrough.
- `website/assets/support/share-merlin-page-poster.webp`: reduced-motion
  fallback for the Merlin species-page walkthrough.

## Published walkthroughs

- `website/assets/support/share-selected-name.gif`: selecting a biological
  name, opening the Share Sheet, and reviewing the lookup result.
- `website/assets/support/share-merlin-page.gif`: sharing a public Merlin Bird
  ID species page and reviewing the lookup result.

The captures must obscure suggested contacts, account information, location,
notifications, browsing history, and other personal information. Keep clips
under 1.5 MB where legibility permits and maintain equivalent written steps and
meaningful alternative text beside every clip.

Third-party names, trademarks, interfaces, and media shown in demonstrations
remain the property of their respective owners. Keep the non-affiliation notice
beside the Merlin demonstration.

## Capture workflow

1. Write a short shot list from the approved written steps. Name the starting
   context, every tap that changes the next state, and the final result.
2. Prepare a privacy-safe device state before recording. Use public example
   content, disable notifications, and remove or obscure contacts, accounts,
   location, browsing history, and other personal information.
3. Record one clean portrait pass on an iPhone at native resolution. Pause
   briefly at the start, after important taps, and on the final result.
4. Trim and redact the recording before it enters the repository. Watch the
   complete redacted source at full size and frame by frame around transitions.
5. Generate a review GIF and reduced-motion poster outside the published asset
   directory:

   ```sh
   scripts/prepare_support_media.sh \
     /path/to/redacted-recording.mov \
     lookup-species \
     7.5 \
     /tmp/taxon-support-media
   ```

   The third argument is the poster timestamp in seconds. Choose a frame that
   communicates the result without requiring the animation.
6. Review both outputs at their rendered desktop and mobile sizes. Confirm that
   labels remain legible, taps are understandable, the sequence has no private
   frames, and the poster matches the final workflow.
7. Copy accepted outputs into `website/assets/support/`, update the figure's
   alternative text and caption, build the site, and perform a rendered-site
   review. Keep raw recordings and intermediate frames out of Git.

The preparation script targets 402 pixels wide, 6 frames per second, and a
1.5 MB GIF limit. If it exceeds the limit, shorten idle time first; reduce
dimensions or frame rate only when the sequence remains legible.

## Next useful walkthrough

A **Lookup Species** walkthrough would add information that the two existing
Share Sheet demonstrations do not cover. Its shot list should be:

1. Select a species name in Books and tap **Copy**.
2. Run **Lookup Species** using one representative invocation method.
3. Show the translations and scientific name.
4. Dismiss the result and return to Books.

Use the Shortcuts app for the published demonstration because it is available
on every supported iPhone. Mention Home Screen, Action button, and Back Tap in
text; showing all four methods would make the clip repetitive.
