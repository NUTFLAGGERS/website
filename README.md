# NUTFLAGGERS Website

Static site for NUTFLAGGERS CTF team built with [Astro](https://astro.build) (SSG) and styled with minimal terminal aesthetics.

---

## 🚀 Quick Start Guide

### 1. Prerequisites

Ensure you have the following installed on your system:
- **Node.js** (v18.0.0 or higher, v20 recommended)
- **npm** (v9.0.0 or higher)

Verify your Node.js installation:
```bash
node -v
npm -v
```

---

### 2. Installation

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/nutflaggers/website.git
   cd website
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

---

### 3. Running Locally (Development Mode)

Start the Astro local development server with hot-module reloading (HMR):

```bash
npm run dev
```

Once started, open your browser and navigate to:
```text
http://localhost:4321
```

*Note: You can also use `npm start` as an alias for `npm run dev`.*

---

### 4. Creating New Writeups & Posts

You can easily generate a new writeup using the built-in interactive CLI tool:

```bash
npm run new-writeup
```

Follow the prompts to specify:
- Post / Writeup Title
- Publication Date
- CTF Event Name
- Author Handle
- Rank & Points
- Tags (e.g. `web`, `pwn`, `crypto`)
- Description

This auto-generates a pre-formatted Markdown template under `src/content/writeups/<slug>.md`.

---

### 5. Building & Previewing for Production

To test the static production build locally:

1. **Build the static site**:
   ```bash
   npm run build
   ```
   *This compiles all pages and assets into the `./dist` directory.*

2. **Preview the production build locally**:
   ```bash
   npm run preview
   ```
   Navigate to `http://localhost:4321` (or the URL provided in the console) to test the compiled output.

---

## 📁 Project Structure

```text
├── public/                 # Static assets (favicon, CNAME, .nojekyll)
├── scripts/
│   └── new-writeup.js      # Interactive post generator script
├── src/
│   ├── components/         # Reusable Astro components (Header, Footer, TagBadge, etc.)
│   ├── content/            # Markdown content collections (writeups, events)
│   │   └── config.ts       # Type-safe Zod content schemas
│   ├── layouts/            # Base HTML page layouts
│   ├── pages/              # Route pages (index, writeups, events, about, projects, resources)
│   └── styles/             # Global CSS design tokens & baseline styles
├── astro.config.mjs        # Astro SSG configuration
├── package.json            # Scripts & dependencies
└── tsconfig.json           # TypeScript configuration
```

---

## 🛠 Available NPM Scripts

| Command | Action |
| :--- | :--- |
| `npm run dev` | Starts the Astro development server at `http://localhost:4321` |
| `npm run build` | Builds the static website to `./dist` for deployment |
| `npm run preview` | Previews the compiled `./dist` build locally |
| `npm run new-writeup` | Interactive CLI helper to scaffold a new writeup post |
