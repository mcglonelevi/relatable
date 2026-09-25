# Relatable

Relatable is a board game design studio at **relatable.gg**. Every Relatable game starts from something people already know: an alarm clock, a game of tic-tac-toe, a moment everyone has lived through. Then it adds a twist. Players should understand what a game is about before they read the rules.

**Tagline:** Instantly familiar. Endlessly fun.

The whole brand works the same way the games do. It should feel familiar at first glance, with one playful twist.

## Voice

We write like a friend explaining a game at the table.

- **Start from the familiar thing.** Name the everyday idea first, then the twist. "Everyone has hit snooze. Now it's a strategy."
- **Keep rules short.** If a game can't be explained in one sentence, the website doesn't try to. Say what it's about and link to the rules.
- **Be warm and a little funny.** A wink is fine, but a pile of jokes isn't.
- **Use plain words.** Say "players," "turns" and "cards," not "engagement mechanics."

| Do (example lines) | Don't |
| --- | --- |
| "Tic-tac-toe, but your opponent gets to move your pieces." | "A revolutionary reimagining of a classic abstract strategy experience." |
| "15 minutes. 2–4 players. Zero rulebook stress." | "Epic! Amazing! You'll LOVE it!!!" |
| "You already know how to play. Mostly." | Jargon that assumes the reader is already a hobby gamer. |

## Logo

The logo is two dice shaped as speech bubbles. It shows people talking about a game, or relating to each other. The red die shows three pips and the teal die shows two. The teal die sits in front, with a small cut-out gap where they overlap.

| File | Use it for |
| --- | --- |
| `relatable-logo-stacked-*` | Game boxes, posters, the About page, square spaces. |
| `relatable-logo-horizontal-*` | The website header, email signatures, banners, rulebook covers. |
| `relatable-icon.svg` | Social media avatars, the browser-tab icon, the app icon, stickers, dice stamps. |
| `relatable-wordmark-*` | Tight spaces where the dice already appear nearby. |

Each file comes in `-on-light` (ink text) and `-on-dark` (cream text). The dice look the same on both.

- **Clear space:** keep empty space around the logo equal to the width of one pip-column of the red die, about a quarter of its width. Nothing should intrude on it.
- **Minimum size:** the horizontal logo at 140px wide (35mm in print). The icon at 24px (8mm). Below those sizes, use the icon alone.
- **Backgrounds:** use `surface` (cream) or `ink` (night). The logo also works on `mustard-soft` or `teal-soft`. Never put it on a tomato or teal fill, or on a busy photo.
- **Don't:** recolor the dice, swap which die is in front, add pips, stretch or rotate the logo, add a drop shadow, or set "relatable" in a different font.

## Colour

The palette is a game table: cream table, ink type, and three game-piece colours.

- **Proportions:** about 60% `surface`, 20% `ink`, 10% `tomato`, 7% `teal`, 3% `mustard`. Tomato is the colour people will remember. Mustard is a spice.
- **Brand colours at full strength are for shapes.** `tomato` and `teal` at full value don't have enough contrast for text on cream. For words, use `tomato-text` and `teal-text`.
- **Text on fills:** use `on-tomato` (ink) on tomato, `on-teal-deep` (cream) on `teal-deep` and `on-mustard` (ink) on mustard. Never put white on tomato.
- **One lead colour per game.** Each game picks tomato, teal or mustard as its lead colour for its box, its page hero and its social posts. The other two stay as supporting colours.
- **Dark mode** swaps cream and ink. The dice, the pips and the fills stay the same.

## Type

One family: **Rubik** (SIL Open Font License, free for commercial use, including logos and packaging).

- **800 (ExtraBold)** for display and page titles, set tight (-0.02em). This is the wordmark's weight.
- **700 / 600** for section and card headings.
- **400** for reading text. **500** for buttons and UI.
- **Labels:** 13px semibold uppercase with wide tracking (`label`), like the tagline under the logo.
- Keep line length near 65 characters. Use sentence case for headings. Never set body copy in all caps.

## Shapes and motifs

- **Rounded squares.** Cards, panels and photos use `radius-lg`, the corner of a die. Nothing has a sharp corner.
- **Pips.** Circles from `radius-full` work as bullets, loading indicators, rating dots and background patterns. Use one to six pips, as on a die.
- **Speech-bubble tails.** A small tail on a card or quote marks a callout, a testimonial or "what players say". Use one per section at most.
- **The game-piece shadow.** `shadow-piece` is a hard 4px drop with no blur. It sits under buttons and game cards so they feel like pieces you could pick up.
- **Photography:** real hands, real tables and real game components, in daylight. Show people laughing mid-turn, not posed. Avoid stock photos of generic "friends playing games".
- **Icons:** rounded 2px-stroke line icons with round caps (Lucide or Phosphor, both free), coloured `ink` or `teal-text`. Don't use emoji in the interface.

## Accessibility

- Body text needs 4.5:1 contrast on its background in both themes. Every text token's note says where it passes.
- Keyboard focus uses `focus-ring`: a 2px gap in the surface colour, then a 2px teal-text ring.
- Colour is never the only signal. Errors get an icon and a message, and a game's lead colour always comes with its name.
- Respect reduced-motion settings. Dice can wobble on hover, but only if the visitor hasn't turned motion off.

## More in this system

- **Design brief:** the plan for the website and the other places the brand will appear, such as social media, packaging, rulebooks and conventions. See the *Design brief* section.
