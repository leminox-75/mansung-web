# Design System Strategy: The Industrial Conservatory

## 1. Overview & Creative North Star
The Creative North Star for this design system is **"The Architectural Editorial."**

Unlike standard industrial websites that feel cold and utilitarian, this system treats greenhouse engineering as a form of high-end architecture. We merge the precision of industrial manufacturing with the organic soul of nature. The "Editorial" aspect is achieved through an intentional departure from symmetrical grids. By using expansive negative space (e.g., `spacing-24`), overlapping image treatments, and dramatic typography shifts, we position the brand as a premium authority—a curator of light and growth rather than just a material supplier.

## 2. Colors
Our palette is rooted in the deep, structural greens of high-performance greenhouses, balanced by the breathable tones of sand and morning mist.

### The "No-Line" Rule
To maintain a premium, architectural feel, **1px solid borders are strictly prohibited for sectioning.** Boundaries must be defined solely by background color shifts. For example, a section using `surface-container-low` (#f4f4f0) should sit directly against a `surface` (#faf9f5) background. This creates a soft, modern transition that feels like light hitting different planes of a building.

### Surface Hierarchy & Nesting
Treat the UI as a series of stacked architectural materials. Use the `surface-container` tiers to define depth:
* **Base:** `surface` (#faf9f5) for the primary page background.
* **Secondary Sections:** `surface-container-low` (#f4f4f0) for large informational blocks.
* **Interactive Cards:** `surface-container-lowest` (#ffffff) to make items appear "lifted" by light.
* **In-Page Modules:** `surface-container-high` (#e8e8e4) for recessed utility areas or sidebars.

### Glass & Gradient Rule
Floating elements (like navigation bars or hovering image captions) should utilize a "Glassmorphism" effect. Use `surface` (#faf9f5) at 70% opacity with a `backdrop-blur` of 12px. For primary CTAs, apply a subtle linear gradient from `primary` (#173124) to `primary-container` (#2D4739) at a 135-degree angle to provide a velvet-like depth.

## 3. Typography
The typography system is a dialogue between legacy and innovation.

* **Display & Headlines (Newsreader):** Use these for storytelling. The serif conveys the "Legacy and Trust" of a factory that has stood the test of time. *Editorial Tip:* Use `display-lg` for hero statements but pair it with wide letter-spacing (-0.02em) to maintain a modern edge.
* **Body & Titles (Manrope):** A clean, geometric sans-serif that represents industrial precision.
* **The Contrast Principle:** Always pair a `headline-lg` (Newsreader) with a `label-md` (Manrope) in all-caps for sub-headers. This high-contrast pairing is the hallmark of premium editorial design.

## 4. Elevation & Depth
We eschew traditional drop shadows in favor of **Tonal Layering.**

* **Ambient Shadows:** If a floating effect is required (e.g., a modal or a primary product card), shadows must be extra-diffused. Use a blur of 32px with an 8% opacity of `on-surface` (#1a1c1a). The shadow should feel like a soft glow, not a hard edge.
* **The Ghost Border Fallback:** For accessibility in form fields, use a "Ghost Border." Apply the `outline-variant` (#c2c8c2) at 20% opacity. It should be just visible enough to define a boundary without breaking the soft aesthetic.
* **Roundedness:** To soften the "industrial" feel, use a consistent `lg` (1rem) radius for primary cards and `xl` (1.5rem) for hero imagery containers.

## 5. Components

### Buttons
* **Primary:** Background `primary` (#173124), text `on-primary` (#ffffff), radius `full`. No border.
* **Secondary:** Background `surface-container-highest` (#e2e3df), text `primary`.
* **Tertiary:** Text `primary` with a 2px underline in `surface-tint` (#496455).

### Cards & Lists
* **Rule:** Forbid the use of divider lines.
* **Implementation:** Separate list items using `spacing-4` (1.4rem). Use a background shift to `surface-container-low` on hover to define the interactive area. Product cards should feature large images with a "Scale-up" transition (1.02x) on hover.

### Form Inputs
* **Style:** `surface-container-lowest` (#ffffff) background with a `Ghost Border` (outline-variant at 20%).
* **Focus State:** Shift the border to 100% opacity of `primary` (#173124) to indicate active precision.

### Greenhouse Spec Chips
* **Context:** Unique to this factory, use chips to show material specs (e.g., "UV-Resistant," "Reinforced Steel").
* **Style:** `secondary-container` (#cbe7c8) background with `on-secondary-container` (#506950) text. Use `sm` (0.25rem) radius for a more "technical" look.

## 6. Do's and Don'ts

### Do
* **Do** use asymmetrical layouts. Place a large image on the left and a small text block offset to the right.
* **Do** use `spacing-16` or `spacing-20` between major sections to let the "Nature" aspect of the brand breathe.
* **Do** use high-quality photography that captures the interplay of light and structure.

### Don't
* **Don't** use 100% black text. Always use `on-surface` (#1a1c1a) for better readability and a softer, more premium feel.
* **Don't** use "Standard" 1px dividers. If you must separate content, use a 4px tall bar in `primary-fixed` (#ccead6).
* **Don't** clutter the screen. If a piece of information isn't vital, move it to a "Technical Specs" drawer or secondary page.