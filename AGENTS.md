# AGENTS.md — Static Site Development Guidelines for GitHub Pages (Astro SSG)

This file serves as the operational guide and technical standard for AI coding agents operating on this static website codebase targeted for **GitHub Pages** deployment using **Astro**.

---

## 1. Core Architecture & Stack

- **Target Platform:** GitHub Pages (Static Web Hosting).
- **Core Framework:** **Astro (SSG)** — Zero client-side JS by default, Islands Architecture.
- **Content Engine:** Markdown (`.md`) / MDX (`.mdx`) with **Type-Safe Content Collections** and Zod schema validation in `src/content/config.ts`.
- **Styling & Aesthetics:** Vanilla CSS with CSS Custom Properties (`:root` tokens). Primary design reference is `minimal_ref.html` (Minimalist terminal/CTF aesthetic, `Fira Code` monospace typography, dark `#111` background, `#d4d4d4` text, category badges, terminal search prompt).
- **Architecture Principle:** Reusable `.astro` components, type-safe content collections, and modular design patterns. Avoid duplicated HTML blocks; use component-based props and Astro template loops for repeating structures (e.g. event rows, writeup items, challenge tags, member lists).
- **Build Mode:** Astro Static Site Generation (`npm run build` compiling static HTML/CSS to `./dist`).
- **Deployment Source:** GitHub Actions workflow building Astro and uploading `./dist` to GitHub Pages.

---

## 2. GitHub Pages Deployment Rules & Conventions

### 2.1 `.nojekyll` Configuration
- Ensure a `.nojekyll` file exists in the `public/` directory so it is copied into `./dist` upon build to bypass default GitHub Pages Jekyll processing.
- This prevents GitHub Pages from ignoring directories or files starting with underscores (`_astro`, etc.).

### 2.2 Pathing & URL Handling (Crucial)
- **Base Tag / Base Path Helper:** Configure `site` and `base` in `astro.config.mjs` if hosted under a repository subpath (e.g., `https://<username>.github.io/<repo-name>/`).
- **Use Astro URL Helpers:** Use `import.meta.env.BASE_URL` or relative URL paths for linking static assets in `public/` and pages.
- **Subpath Compatibility:** Ensure all link refs (`<a href="...">`) and image paths handle base path routing correctly.

### 2.3 Custom Domain (`CNAME`)
- If a custom domain is configured, ensure `CNAME` is kept in `public/CNAME` so Astro copies it to the deployment root (`dist/`) during build.

### 2.4 GitHub Actions Deployment Workflow
When configuring automated deployment via GitHub Actions for Astro, use official actions:
```yaml
name: Deploy Astro Site to GitHub Pages

on:
  push:
    branches: ["main"]

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: true

jobs:
  build-and-deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'

      - name: Install Dependencies
        run: npm ci

      - name: Build Astro Site
        run: npm run build

      - name: Setup Pages
        uses: actions/configure-pages@v5

      - name: Upload Artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: './dist'

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

---

## 3. Code Standards & Structural Integrity

### 3.1 Markup & Astro Component Rules
- **Semantic HTML5:** Always structure layout markup using `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`.
- **Single `<h1>`:** Maintain exactly one `<h1>` per rendered page for document hierarchy and SEO.
- **SEO & Meta Head Components:** Use a centralized `<BaseHead.astro>` component for every page containing:
  - `<meta charset="UTF-8" />`
  - `<meta name="viewport" content="width=device-width, initial-scale=1.0" />`
  - `<title>` with descriptive page title.
  - `<meta name="description" content="..." />`
  - Open Graph meta tags (`og:title`, `og:description`, `og:image`, `og:url`).
- **Accessibility (a11y):**
  - All `<img>` tags must have meaningful `alt` attributes (`alt=""` only for decorative icons).
  - Interactive elements must be focusable and keyboard accessible.
  - Contrast ratios must adhere to WCAG AA standards.

### 3.2 Type-Safe Content Collections (Markdown & MDX)
- **Strict Schema Enforcement:** All Markdown content must live in `src/content/<collection_name>/` and have a defined Zod schema in `src/content/config.ts`.
- **Frontmatter Standards:** Ensure required fields (e.g. `title`, `pubDate`, `tags`, `description`) are validated. Build MUST fail if frontmatter is invalid or missing required keys.
- **Code Syntax Highlighting:** Use Astro's built-in Shiki/Prism markdown configuration for code blocks in writeups.

### 3.3 CSS Architecture & Aesthetics
- **Design Tokens:** Define CSS Custom Properties (`:root`) in `src/styles/global.css` for color palettes, typography, spacing, and transitions.
- **Responsive Layouts:** Use CSS Grid and Flexbox with mobile-first media queries (`@media (min-width: ...)`). Avoid fixed pixel widths on containers.
- **Aesthetic Foundation:** Maintain the monospace terminal style (`Fira Code`), dark background (`#111`), category badges (`.tag.web`, `.tag.pwn`), and crisp borders inspired by `minimal_ref.html`.
- **Scoped Styles:** Prefer Astro scoped `<style>` tags for component-specific rules and `global.css` for design system tokens.

### 3.4 Reusable Component Architecture
- **Avoid Code Duplication:** Deconstruct UI elements into modular `.astro` components inside `src/components/`:
  - **`Header.astro` / `Footer.astro`**: Main shell navigation & prompt header (`~/0xflag $`).
  - **`Row.astro`**: Reusable item/writeup row with date, title, tags, and expandable metadata.
  - **`TagBadge.astro`**: Standardized category badge tokens (`.tag.web`, `.tag.pwn`, etc.).
  - **`SearchPrompt.astro`**: Interactive client-side terminal filtering prompt.
  - **`TeamMember.astro`**: Uniform member layout component.

---

## 4. Agent Execution & Verification Workflow

When executing tasks on this codebase, AI agents MUST follow this sequence:

1. **Understand & Research:**
   - Inspect existing components and content schemas (`view_file`, `list_dir`, `grep_search`).
   - Respect established design patterns, colors, and font declarations.

2. **Edit Safely:**
   - Modify targeted components or content files cleanly. Ensure TypeScript schemas in `src/content/config.ts` are updated if new frontmatter fields are added.

3. **Verify Locally:**
   - Run the local Astro development server or build check:
     ```bash
     npm run dev
     # and verify build output
     npm run build && npx astro preview
     ```
   - Check page rendering, console logs, build outputs, broken links, and mobile responsiveness.

4. **Sanity Check Deployment Assets:**
   - Confirm `public/.nojekyll` is present.
   - Confirm build output in `./dist` compiles cleanly without frontmatter or TypeScript errors.

---

## 5. Git Commit & Repository Hygiene

- **Atomic Commits:** Make descriptive, self-contained git commits.
- **Clean Workspace:** Never commit transient log files, temporary scratch scripts, or OS clutter (`.DS_Store`, `node_modules/`, `.astro/`).
- **No Hardcoded Credentials:** Never store secret keys or personal access tokens in client code, content files, or workflow files.

