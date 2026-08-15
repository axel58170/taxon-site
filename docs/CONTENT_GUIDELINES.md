# Customer-facing language

Taxon Translate helps people find what an animal, plant, fungus, or other taxon is
called in their chosen languages. Describe that outcome before describing the
interface used to reach it.

## Name the outcome, not the transport

- Name features for the user's goal: **Look up a name while reading**, **Look
  up names from a Wikipedia page**, or **Look up a bird from Merlin**.
- Do not use **Share selected text**, **Share a Wikipedia article**, or similar
  Share Sheet instructions as feature names. Sharing is only the current
  transport into Taxon Translate.
- In procedural instructions, use the exact iOS labels **Share** and **Share
  Sheet** when those steps are necessary. Explain the lookup outcome first.
- When Taxon Translate appears over another app, say that the person can view the
  names and then close the result to remain in or return to what they were
  doing. Do not imply that they permanently leave, transfer from, or “continue
  from” the source app.

## Lead with the normal case

- Introduce a capability with the result people normally expect: for example,
  **Look up names from Wikipedia** and “open an article about an animal, plant,
  or fungus to see its names in your languages.”
- Do not make exceptional limitations the premise of a feature. Avoid openings
  such as **Use a supported Wikipedia article**, even when some pages cannot be
  matched or some languages do not have a recorded common name.
- Keep the main claim accurate without turning it into a disclaimer. Describe
  what the feature does in the usual case, then explain relevant exceptions in
  supporting text, troubleshooting, or the point where someone encounters
  them.
- Lead with a limitation only when it changes a decision the person must make,
  prevents the next step, or is necessary for safety, privacy, or informed
  consent.

## Use familiar language

- Do not use **resolve**, **resolution**, or **resolved** in customer-facing
  prose. People look up a name, find the matching taxon, or see what it is
  called.
- An exact interface label that the website must identify accurately, such as
  the current Shortcuts action **Resolve Taxon**, may be quoted. Explain that
  action in plain language and do not reuse its terminology as prose.
- Prefer **animal, plant, or fungus** in introductory copy. Use **taxon** where
  scientific precision is useful or where the interface itself uses the term.
- Keep scientific names, common names, and identity distinct. Taxon Translate
  shows names recorded by its sources; it does not invent or automatically
  translate missing common names.

## Review checklist

Before publishing customer-facing text, check that:

1. headings and feature labels state what the person can accomplish;
2. Share Sheet, Shortcuts, Wikipedia, and Merlin are described as inputs or
   contexts rather than the goal;
3. the copy does not imply that an overlay removes the person from the source
   app;
4. normal capability copy leads with the successful outcome and puts
   exceptional limitations in the relevant supporting context;
5. **resolve** appears only when quoting an existing interface label; and
6. captions, alternative text, descriptions, privacy text, and testing
   instructions follow the same rules as the main page.

## Localization inventory

Treat all customer-facing website text as localizable, including text outside
Markdown paragraphs. For the homepage, the inventory includes:

- YAML front matter: browser `title` and metadata `description`;
- hero category line, heading, explanatory copy, and action label;
- interface-section eyebrow, heading, explanatory copy, media alternative text,
  reduced-motion poster alternative text, replay control, and caption;
- scenario and feature headings, paragraphs, notes, labels, and link text; and
- shared layout text in `website/_layouts/default.html`, including the skip link,
  brand accessibility label, navigation labels, and footer links.

When a new customer-facing string is added in Markdown, HTML, YAML front matter,
Liquid include parameters, an image description, or shared layout chrome, add its
location to this inventory before publication.
