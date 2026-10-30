# The Story of the World

A beginner-friendly, chronological history of the world, from the Big Bang to the mid-2020s.
It is a static site with no build step: open `history/` from any static server, such as the site root on Netlify.

- **170 articles** across 9 eras. Each article has a summary, a full explanation, a "why it matters" box, the key people, linked ideas and connected events.
- **37 "key ideas" explainers**, covering terms like democracy, empire, nationalism, capitalism, communism, fascism, the world religions and philosophy, for readers starting from zero.
- **A storyteller's version of every article**, written in the wry, eloquent, morally sharp voice of Alan Shore (*Boston Legal*), without the courtroom framing. It's the default, and readers can switch to the plain version with the "Just the facts" toggle; their choice is remembered.
- Search, category filters, era jump links, reading progress (saved in the browser) and light and dark themes.

## Adding an article

Articles live in `data/NN-<era>.js`. Add an object to the `H.add([...])` list:

| key | meaning |
|-----|---------|
| `id` | unique slug, used in URLs (`#/a/<id>`) |
| `y` | sort year (negative = BCE; decimals allowed to order events within a year) |
| `d` | date as displayed |
| `r` | region |
| `c` | categories: war, empire, revolution, idea, movement, migration, science, economy, disaster, origins |
| `t`, `s` | title and one-line summary |
| `b` | body text; separate paragraphs with a blank line |
| `m` | "why it matters" |
| `p` | key people |
| `l` | ids of connected articles |
| `k` | ids of key ideas from `data/concepts.js` |

The era is worked out from `y` using `data/eras.js`, so the file an article lives in only matters for organisation.

## Storyteller versions

`data/stories/*.js` hold the narrated versions as `H.story({ '<article id>': \`...\` })`. Each key must match an article id. Separate paragraphs with a blank line. An article without a story simply shows the plain text with no toggle.
