# Repository Guidelines

This is Qinyu Luo’s Astro personal website. `master` stores source; `gh-pages` stores the verified static publication.

- Use Node 24 or newer, Python 3.10+, and `pip install -r requirements-dev.txt`.
- Install dependencies with `npm ci`, then run `npm run build` and `npm run verify`.
- Preview using `npm run preview` (127.0.0.1:4174, dist only).
- Content lives in `src/data/`, pages in `src/pages/`, components in `src/components/`, styles in `src/styles/site.css`.
- Home and Research share publication order, search, and pagination. Keep all Scholar records represented once in the canonical illustrated works.
- Keep reports, slides, posters, and images readable inside the site; do not restore CV downloads.
- Preserve public source credits and manuscript version notes.
- Do not commit credentials, machine-local paths, previews, scratch work, node_modules, or dist on the source branch.
- Production publication needs explicit user authorization. Publish only the verified dist tree, with .nojekyll, to gh-pages; preserve source and rollback history.
