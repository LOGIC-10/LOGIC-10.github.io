# Repository Guidelines

## Project Structure & Module Organization
- Jekyll site using the Minimal Mistakes theme. Key folders:
  - `_pages/` static pages, `_posts/` blog posts.
  - Collections: `_publications/`, `_talks/`, `_portfolio/`, `_teaching/`.
  - Theme plumbing: `_layouts/`, `_includes/`, `_sass/`, `_data/`.
  - Assets: `assets/` (JS/CSS), `images/` (media), `files/` (downloads).
  - Generators: `markdown_generator/` (Python scripts/notebooks for talks/publications).
  - Config: `_config.yml` (site), `_config.dev.yml` (overrides).

## Build, Test, and Development Commands
- Setup: `bundle install` (Ruby gems). If editing JS, also `npm install`.
- Local dev: `bundle exec jekyll liveserve` (auto-rebuild + live reload at `http://localhost:4000`).
- Production build: `JEKYLL_ENV=production bundle exec jekyll build -d _site`.
- JS bundling: `npm run build:js` (minify to `assets/js/main.min.js`), watch: `npm run watch:js`.
- Content generation (from repo root):
  - `cd markdown_generator && python publications.py`
  - `cd markdown_generator && python talks.py`

## Coding Style & Naming Conventions
- Markdown + YAML front matter; indent with 2 spaces; wrap strings that include `:` or quotes.
- Posts and collections: `YYYY-MM-DD-url-slug.md` (e.g., `_posts/2025-01-15-hello-world.md`).
- Use hyphenated, lowercase filenames and permalinks.
- Place custom styles in `_sass/` and JS in `assets/js/`; avoid inline CSS/JS.

## Testing Guidelines
- No formal test suite. A clean build is the gate:
  - Run `bundle exec jekyll build` and ensure no errors/warnings.
  - Manually check critical pages and navigation.
- Optional: run link checks with `htmlproofer` if available.

## Commit & Pull Request Guidelines
- Commits: concise, imperative, and scoped. Preferred prefixes: `add:`, `update:`, `fix:`, `chore:` (e.g., `update: research interest`).
- PRs: include a clear summary, linked issues, and screenshots for UI/layout changes.
- For code/theme changes, reference or create a closed issue labeled `code change` with a link to the commit/diff (see CONTRIBUTING.md).

## Security & Configuration Tips
- Keep secrets out of the repo; review `_config.yml` for PII (emails, IDs).
- For GitHub Pages, ensure `url` and `baseurl` are correct; use production builds for deployment.
- If dependency warnings mention `Gemfile.lock`, remove it and reinstall per README.

## Research Blog
- Location: add posts to `_research/` using `YYYY-MM-DD-slug.md`.
- Front matter:
  - `---\ntitle: "Post Title"\nexcerpt: "One-line summary"\ntags: [topic1, topic2]\n---`
- Index page: `/research/` lists all entries (see `_pages/research.html`).
- Permalinks: `/research/<slug>/` (set in `_config.yml`).
- Images: put under `images/research/<slug>/` and reference like `![caption](/images/research/<slug>/fig1.png)`.
- Comments/sharing are enabled by defaults; set `comments: false` per-post to disable.
