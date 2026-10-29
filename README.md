# findmymesh.com

Static site. `npm run build` pulls the MeshCore community-map snapshot (`site/src/fetch_nodes.mjs`),
then `site/src/gen.py` renders every page into `site/dist`.

- Groups: `site/groups.json` (verified listings). Guides/hardware/videos: `content/*.json`.
- Blog: one Markdown file per post in `content/blog/` (see `content/blog/README.md`). A post is
  published once its `date` is today or earlier (America/New_York). The Netlify scheduled function
  `netlify/functions/nightly.mjs` triggers a rebuild every morning, which is how scheduled posts go live
  and how the map numbers refresh.
- Gear I use: `content/tested.json`.
- Amazon photos/prices load in the browser from `/api/items`, proxied to the private product service.

Local build: `npm install && npm run build`, then `npm run crawl` to check links and layout.
