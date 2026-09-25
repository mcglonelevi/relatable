# Design brief

What we're building, who it's for and how it should feel. Use it when you (or anyone you hire) start work on the website, social media, packaging or anything else with the Relatable name on it.

## The idea in one line

Every page should do what the games do: show something familiar first, then the twist.

## Who it's for

- **Casual players and families.** They want a game they can explain in a minute and play tonight. They're not hobby gamers and won't read long rules.
- **Gift buyers.** They need to see at a glance who a game is for, how many can play and how long it takes.
- **Stores, conventions and press.** They need clear game info, good photos and a way to get in touch.
- **Future backers.** If a game goes to crowdfunding, the site is where people check that Relatable is real and trustworthy.

## Website: relatable.gg

### Goals, in order

1. Explain each game in one glance: the familiar thing plus the twist.
2. Get visitors to take the next step: buy, back a campaign, or join the mailing list.
3. Show that Relatable is a small, real studio with a point of view.

### Pages

| Page | Job | Key content |
| --- | --- | --- |
| **Home** | Say what Relatable is in five seconds. | A hero showing the tagline and a featured game, a row of game cards, a short "Why relatable?" section and a mailing-list sign-up. |
| **Games** | Browse everything. | A game card for each game, with its lead colour, name, a one-line hook and stats (players · time · age). |
| **Game page** (one per game) | Make someone want to play. | The familiar thing, then the twist, then "how it plays" in 3 steps, photos, stats, a rules PDF, and buy/back/notify buttons. |
| **About** | Tell the studio story. | Who's behind it, why "relatable", how games get made (playtesting), and photos of real playtest tables. |
| **Contact / Press** | Make business easy. | An email address, a press kit (logos, box shots, one-sheets) and convention dates. |
| **Newsletter** | Build the list. | A single field and an honest promise ("A short note when a new game is ready"). |

### How a game page reads

Every game page follows this order:

1. **The familiar thing.** A big headline naming the everyday idea. *"You've hit snooze a thousand times."*
2. **The twist.** One sentence. *"Now hitting snooze is how you win."* [Replace with the game's real hook.]
3. **Stats bar:** [PLAYERS] · [MINUTES] min · Ages [AGE]+, using `label` and `caption` type on a pip-dotted strip.
4. **How it plays:** three numbered steps, each with a photo or illustration. This is the one place numbered markers belong, because it's a real sequence.
5. **Photos** of real people at a real table.
6. **Get it:** the main button (tomato), a secondary rules PDF link, and a notify-me sign-up if the game isn't out yet.

### Look and feel

- **Light theme by default:** a cream table with ink type. Offer dark mode through the system setting, since it's already defined in the tokens.
- **Hero:** big Rubik 800 headline, left-aligned, with the featured game's box or a photo on the right in a `radius-lg` frame with `shadow-piece`. Size it to its content, not the full screen height.
- **Game cards:** `surface-raised`, `radius-lg` and `shadow-piece`, with the game's lead colour as a top band or a big die-shaped block behind the box art. On hover, the card lifts 2px and the dice wobble slightly.
- **Buttons:** the primary is a tomato fill with ink text and `shadow-piece`, and it presses down on click. The secondary is teal-deep with cream text. Text links use `tomato-text`.
- **Section rhythm:** alternate `surface` and `surface-sunken` bands, with `space-20` between sections on desktop and `space-12` on phones.
- **Mobile first.** Most visitors arrive from social media on phones. Cards stack to one column, and the buy button stays reachable.

### Components to build

Header (horizontal logo, nav, a "Get the games" button), footer (icon, links, newsletter), button (primary, secondary, text), game card, stats bar, "how it plays" steps, speech-bubble quote, newsletter form, tag (lead-colour soft tints), photo frame.

### Technical notes

- Load Rubik from Google Fonts or self-host the WOFF2 files included in this system (weights 400–800).
- Use `relatable-icon.svg` as the browser-tab icon. Give it a cream rounded-square background for the Apple touch icon.
- For the social share image (1200×630), use the horizontal logo on cream with the featured game's lead-colour block.

## Other places the brand appears

### Social media

- **Avatar:** the icon on a cream circle.
- **Posts:** one big idea per post. Show the familiar thing, then the twist, in two frames or as a before-and-after. Use the game's lead colour as the background block and ink Rubik 800 headlines.
- **Recurring series ideas:** "You already know how to play" (a 15-second rules explainer), playtest photos, and "Guess the everyday thing" teasers before a new game is revealed.

### Game boxes and components

- The stacked logo sits on the box's top corner or side panel. The game's own title is the hero, and Relatable is the maker's mark.
- Each box uses its lead colour as the dominant field. The other two brand colours are accents.
- The back of the box follows the game page order: the familiar thing, the twist, stats, a photo.
- Rulebooks use Rubik, `label` headers, numbered steps and pip bullets. Keep the first page to "How to win" in one sentence.

### Conventions and events

- **Table banner:** the horizontal logo, the tagline and the featured game's lead colour. It should be readable from 3 metres away.
- **Stickers and handouts:** die-cut stickers of the icon, and a business card with the icon on the front and relatable.gg on the back.
- **Demo table:** a cream tablecloth with a tomato runner, so the table itself is the brand.

## What we still need

- The final names, hooks, stats and photos for each game. The placeholders in [brackets] mark where they go.
- Real box art or prototype photos for the game cards.
- A decision on the shop: a direct store, a crowdfunding page or retail links.
- The contact email and social media handles.
