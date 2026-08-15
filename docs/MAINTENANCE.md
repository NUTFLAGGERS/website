# NUTFLAGGERS Website — Maintenance Guide

This guide covers everything you need to know to maintain, update, and extend the NUTFLAGGERS CTF team website. No deep web development knowledge required — all content is managed through simple text files.

---

## Table of Contents

1. [Overview & Architecture](#1-overview--architecture)
2. [Local Development Setup](#2-local-development-setup)
3. [How Content Works (The Big Picture)](#3-how-content-works-the-big-picture)
4. [Managing Team Members](#4-managing-team-members)
5. [Posting Writeups](#5-posting-writeups)
6. [Managing Events (CTFs)](#6-managing-events-ctfs)
7. [Adding Resources](#7-adding-resources)
8. [Managing Projects](#8-managing-projects)
9. [Tag Reference](#9-tag-reference)
10. [Deployment (GitHub Pages)](#10-deployment-github-pages)
11. [Site-Level Configuration](#11-site-level-configuration)
12. [File Structure Reference](#12-file-structure-reference)
13. [Troubleshooting](#13-troubleshooting)

---

## 1. Overview & Architecture

The website is built with **Astro** (a static site generator) and deployed to **GitHub Pages** at `https://nutflaggers.github.io/website/`.

**Key principles:**
- **No database** — everything is Markdown (`.md`) or JSON (`.json`) files in the `src/content/` folder.
- **No manual HTML editing** — adding content = creating/editing a file in `src/content/`.
- **Reviewer-gated deployment** — pushing to `main` triggers a GitHub Actions build, but the actual publish step requires a **required reviewer** to approve before it goes live.
- **Type-safe** — all frontmatter fields are validated at build time. If a required field is missing or wrong type, the build will fail with a clear error message.

---

## 2. Local Development Setup

Run this once when you first clone the repo:

```bash
# Install dependencies
npm install

# Start the dev server (hot-reloads on save)
npm run dev
```

Then open `http://localhost:4321/` in your browser. Changes to any content file will instantly appear without restarting.

To verify the production build is error-free:

```bash
npm run build
```

> [!IMPORTANT]
> Always run `npm run build` before pushing significant changes. It catches frontmatter validation errors that the dev server might not surface clearly.

---

## 3. How Content Works (The Big Picture)

All editable content lives in **`src/content/`**:

```
src/content/
├── team/        → Team member profiles (.json)
├── writeups/    → CTF writeup blog posts (.md)
├── events/      → CTF competition entries (.md)
├── resources/   → Curated tools & learning links (.md)
└── projects/    → Open-source projects (.md)
```

Each file has a **frontmatter block** at the top (between `---` markers) containing structured metadata. Below the frontmatter is optional freeform Markdown body text.

**The schema for every collection is enforced** in [`src/content/config.ts`](./../src/content/config.ts). If you add a field not in the schema, it's silently ignored. If you omit a required field, the build fails.

---

## 4. Managing Team Members

**Location:** `src/content/team/`  
**File format:** `.json`  
**Naming convention:** `<number>-<handle>.json` — the number controls display order (lower = shown first).

### Adding a New Member

Create a new file: `src/content/team/6-newmember.json`

```json
{
  "handle": "realname (nickname)",
  "role": "member",
  "categories": ["members"],
  "skills": ["web", "misc"],
  "socials": {
    "github": "https://github.com/<username>",
    "twitter": "https://twitter.com/<username>"
  }
}
```

### Full Field Reference

| Field | Required | Type | Description |
|---|---|---|---|
| `handle` | ✅ | string | Display name shown on the About page. Format: `"real? (nickname)"` |
| `role` | ✅ | string | Role/title, e.g. `"captain"`, `"member"`, `"co-captain, infra lead"` |
| `categories` | ❌ | string[] | Which sections they appear under on the About page. `"exco"` always sorts first. |
| `skills` | ❌ | string[] | CTF skill categories. Shown as a tooltip when hovering their name. Use lowercase tag names. |
| `socials` | ❌ | object | Key = platform label (e.g. `"github"`), value = full URL. Leave value as `""` if URL isn't set yet. |

### Categories Explained

The **About page** groups members by category. Each member can appear in **multiple** groups. To create a new group, just add a new string to `categories` — it will automatically create a new section on the page.

**Existing categories:**
- `"exco"` — Executive committee (always listed first)
- `"infra team"` — Infrastructure team

```json
// Member appears in BOTH exco and infra team sections
"categories": ["exco", "infra team"]
```

### Supported Social Platforms

Any key name works — the key is used as the link label. Common ones:

```json
"socials": {
  "github": "https://github.com/<username>",
  "twitter": "https://twitter.com/<username>",
  "website": "https://<yoursite>.com",
  "linkedin": "https://linkedin.com/in/<username>"
}
```

### Removing a Member

Simply delete their `.json` file.

### Changing Display Order

Rename the files. The number prefix controls order — `1-member.json` appears before `2-member.json`. Re-number other files if needed.

---

## 5. Posting Writeups

**Location:** `src/content/writeups/`  
**File format:** `.md` (Markdown)  
**Naming convention:** `<slug>.md` — the filename becomes the URL. E.g. `heap_overflow_pwn.md` → `/writeups/heap_overflow_pwn/`

### Minimal Writeup

```markdown
---
title: "Challenge Name — CTF 2026"
pubDate: "2026-08-15"
tags: ["pwn"]
---

Write your writeup content here using standard Markdown.
```

### Full Writeup with All Fields

```markdown
---
title: "Heap Overflow — PwnCTF 2026"
pubDate: "2026-08-15"
updatedDate: "2026-08-16"
event: "PwnCTF 2026"
author: "handle"
description: "Exploiting a heap overflow in a custom allocator to achieve RCE."
score: "500 pts"
place: "3rd place"
tags: ["pwn", "rev"]
---

# Challenge Title

Your writeup content...

## Vulnerability Analysis

```python
# Code blocks with syntax highlighting
exploit_payload = b"A" * 64
```
```

### Frontmatter Field Reference

| Field | Required | Type | Description |
|---|---|---|---|
| `title` | ✅ | string | Title of the challenge / writeup |
| `pubDate` | ✅ | string | Publication date in `"YYYY-MM-DD"` format |
| `updatedDate` | ❌ | string | Date last updated, same format |
| `event` | ❌ | string | CTF event name, e.g. `"PwnCTF 2026"` |
| `author` | ❌ | string | Author handle |
| `description` | ❌ | string | Short summary shown in listings |
| `score` | ❌ | string | Points value, e.g. `"500 pts"` |
| `place` | ❌ | string | Team placement, e.g. `"1st place"` |
| `tags` | ❌ | string[] | Categories — see [Tag Reference](#9-tag-reference) |

### Markdown Features Available

- Full Markdown syntax (headings, lists, bold, italics, links)
- **Fenced code blocks** with syntax highlighting (powered by Shiki, `github-dark-dimmed` theme)
- Block quotes (`> ...`)
- Tables

### Linking a Writeup to an Event

To make a writeup clickable from an event entry, set the `writeupSlug` in the **event file's** challenges list to match the writeup's filename (without `.md`):

```yaml
# In src/content/events/pwnctf_2026.md
challenges:
  - name: "Heap Overflow"
    category: "pwn"
    points: "500 pts"
    writeupSlug: "heap_overflow_pwn"   # ← matches heap_overflow_pwn.md
```

### Homepage Display

The **3 most recent writeups** (by `pubDate`) appear on the homepage. All writeups appear on the `/writeups/` page.

---

## 6. Managing Events (CTFs)

**Location:** `src/content/events/`  
**File format:** `.md`  
**Naming convention:** `<ctf_name>_<year>.md` (use underscores, no spaces)

### Upcoming CTF (no results yet)

```markdown
---
title: "CTF Name 2026"
date: "2026-10-01"
startDate: "2026-10-01"
location: "Online / International"
description: "Upcoming competition"
featured: true
tags: ["web", "pwn", "crypto"]
challenges: []
---

Brief description of the CTF.
```

### Past CTF (with results)

```markdown
---
title: "CTF Name 2026"
date: "2026-08-01"
startDate: "2026-08-01"
location: "Online"
description: "1st place · 5000 pts"
featured: true
score: "5000 pts"
place: "1st place"
tags: ["web", "pwn", "crypto", "rev"]
challenges:
  - name: "Challenge One"
    category: "web"
    points: "500 pts"
    writeupSlug: "challenge_one_ctfname_2026"
  - name: "Challenge Two (No writeup)"
    category: "pwn"
    points: "300 pts"
---

Brief post-competition notes.
```

### Field Reference

| Field | Required | Type | Description |
|---|---|---|---|
| `title` | ✅ | string | CTF competition name |
| `date` | ✅ | string | Event date `"YYYY-MM-DD"` — used for sorting |
| `startDate` | ❌ | string | Start date (same as `date` unless multi-day) |
| `location` | ❌ | string | E.g. `"Online"`, `"Singapore"` |
| `description` | ❌ | string | Short summary shown in the listing |
| `featured` | ❌ | boolean | `true` → appears in "featured events" on homepage |
| `score` | ❌ | string | Team total score |
| `place` | ❌ | string | Team placement |
| `tags` | ❌ | string[] | Challenge categories present in this CTF |
| `challenges` | ❌ | object[] | List of challenges solved (see below) |
| `url` | ❌ | string | External link to CTF page (optional) |

### Challenge Object Fields

```yaml
challenges:
  - name: "Challenge display name"   # required
    category: "web"                  # required — used for tag badge
    points: "500 pts"                # required
    writeupSlug: "my_writeup_file"   # optional — links to writeup page
```

> [!NOTE]
> Omit `writeupSlug` if no writeup exists yet. You can add it later when the writeup is posted.

### How Events Appear on the Site

- **Upcoming events** (date ≥ `2026-08-01`) → sorted soonest-first on the homepage
- **Featured events** (`featured: true`) → sorted newest-first on the homepage  
- **All events** → `/events/` page (sorted descending by date)

> [!NOTE]
> The "today" reference date used to classify upcoming vs past events is currently hardcoded in `src/pages/index.astro` at `const todayRef = '2026-08-01'`. Update this string periodically to keep the homepage current, or ask AI to update it.

---

## 7. Adding Resources

**Location:** `src/content/resources/`  
**File format:** `.md`  
**Naming convention:** `<resource-name>.md` (use hyphens)

### Resource Entry

```markdown
---
title: "Resource Name"
category: "web"
description: "One sentence description of what this resource is."
url: "https://resource-url.com"
tags: ["web", "learning"]
featured: false
---

Optional longer description or notes about the resource.
```

### Field Reference

| Field | Required | Type | Description |
|---|---|---|---|
| `title` | ✅ | string | Display name of the resource |
| `category` | ✅ | string | Primary category — shown as the "date" column in listings |
| `description` | ✅ | string | Short description shown in listings |
| `url` | ✅ | string | External URL for the resource |
| `tags` | ❌ | string[] | Additional category tags |
| `featured` | ❌ | boolean | `true` → appears on homepage (up to 3 featured shown) |

### Common Categories

Use lowercase, consistent names:
- `"web"` — web exploitation tools/platforms
- `"pwn"` — binary exploitation
- `"crypto"` — cryptography
- `"rev"` — reverse engineering
- `"forensics"` — forensics tools
- `"misc"` — general CTF/security resources
- `"osint"` — OSINT tools

### Homepage Display

Up to **3 resources** with `featured: true` appear on the homepage. The full list is on `/resources/`. Featured resources sort first, then alphabetically by category, then by title.

---

## 8. Managing Projects

**Location:** `src/content/projects/`  
**File format:** `.md`  
**Naming convention:** `<project-name>.md`

### Project Entry

```markdown
---
title: "Project Name"
date: "2026-08-01"
tag: "tool"
description: "One sentence description of the project."
featured: true
githubUrl: "https://github.com/NUTFLAGGERS/<repo-name>"
url: "https://<live-url>.com"
---

Optional longer project description or usage notes.
```

### Field Reference

| Field | Required | Type | Description |
|---|---|---|---|
| `title` | ✅ | string | Project name |
| `date` | ✅ | string | Creation/release date `"YYYY-MM-DD"` |
| `tag` | ✅ | string | Single tag/category label |
| `description` | ✅ | string | Short description shown in listings |
| `featured` | ❌ | boolean | `true` → appears in "featured projects" on homepage |
| `githubUrl` | ❌ | string | GitHub repo URL (preferred) |
| `url` | ❌ | string | Fallback URL if no GitHub |

> [!NOTE]
> If both `githubUrl` and `url` are set, `githubUrl` takes priority for the link. The listing will append `· github` to the description when a GitHub URL is present.

### Homepage Display

Up to **2 projects** with `featured: true` appear on the homepage (featured first, then newest). All projects appear on `/projects/`.

---

## 9. Tag Reference

Tags are used across writeups, events, and resources. They render as color-coded badge pills.

| Tag | Color | Use For |
|---|---|---|
| `web` | Blue | Web exploitation |
| `pwn` | Red | Binary exploitation |
| `rev` | Orange/yellow | Reverse engineering |
| `crypto` | Purple | Cryptography |
| `forensics` | Pink | Digital forensics |
| `misc` | Green | Miscellaneous |
| `osint` | Light blue | OSINT challenges |
| `bot` | Green | Bot challenges |

**Adding a new tag color:** Edit [`src/styles/global.css`](./../src/styles/global.css) and add a new `.tag.<name>` rule following the existing pattern:

```css
.tag.mynewtag { color: #HEXCOLOR; border-color: #HEXCOLOR30; background: #HEXCOLOR0a; }
```

Tags not in this list still render, just with the default grey styling.

---

## 10. Deployment (GitHub Pages)

### How Deployment Works

The workflow in [`.github/workflows/deploy.yml`](./../.github/workflows/deploy.yml) runs in **two separate jobs** every time a push lands on `main`:

| Job | What it does |
|---|---|
| `build` | Checks out code, installs deps, runs `npm run build`, uploads `./dist` as an artifact |
| `deploy` | Takes the built artifact and publishes it to GitHub Pages |

The `deploy` job targets the **`github-pages` environment**, which has **required reviewers** configured. This means:

> [!IMPORTANT]
> Even after a successful build, **the site will not go live until a required reviewer approves the deployment** in the GitHub Actions UI. Reviewers will receive a notification and must click **"Review deployments" → Approve** before the deploy job runs.

### Pushing Changes

```bash
git add .
git commit -m "feat: add writeup for HeapCTF 2026 heap overflow"
git push origin main
```

Then go to the **Actions** tab of the repository → click the running workflow → wait for the build to pass → a reviewer approves the pending `deploy` job.

**Typical time from push to live:** build (~1 min) + reviewer approval + deploy (~30 sec).

### Who Can Approve Deployments

Required reviewers are configured in the **`github-pages` environment settings** under `Settings → Environments → github-pages → Required reviewers`. Only listed users/teams can approve.

### CODEOWNERS (Pull Request Reviews)

The [`.github/CODEOWNERS`](./../.github/CODEOWNERS) file enforces that certain files require a review from `@NUTFLAGGERS/infra-team` before a pull request can be merged:

- All files (`*`) → infra-team
- `astro.config.mjs`, `package.json` → infra-team
- `src/components/`, `src/layouts/`, `src/styles/` → infra-team
- `src/content/writeups/` → infra-team

Content-only changes (events, team, resources, projects) do **not** require a CODEOWNERS review, but still go through the deployment reviewer gate.

### Manual Build & Preview (Local)

```bash
npm run build          # builds to ./dist
npx astro preview      # serves dist/ locally for final check
```

> [!IMPORTANT]
> The live site URL is `https://nutflaggers.github.io/website/`. Note the `/website/` subpath — this is configured in `astro.config.mjs` and handled automatically. Do not hardcode absolute paths in content files.

---

## 11. Site-Level Configuration

### Global Site Config

[`astro.config.mjs`](./../astro.config.mjs) — touches this rarely:

```js
export default defineConfig({
  output: 'static',
  site: 'https://nutflaggers.github.io',
  base: isProd ? '/website/' : '/',   // ← repo subpath
  markdown: {
    shikiConfig: {
      theme: 'github-dark-dimmed',    // ← code block theme
    }
  }
});
```

### Design Tokens (Colors, Fonts)

[`src/styles/global.css`](./../src/styles/global.css) — CSS custom properties that control the entire site's color palette:

```css
:root {
  --bg: #111111;         /* page background */
  --fg: #d4d4d4;         /* body text */
  --dim: #666666;        /* muted/secondary text */
  --link: #7ec8a0;       /* links, accents */
  --section-header: #e3bb88;  /* section titles */
  --tag: #555555;        /* default tag badge */
  --border: #1e1e1e;     /* subtle borders */
  --border-focus: #333333;    /* focused borders */
}
```

### About Page — "Find Us" Social Links

Hardcoded in [`src/pages/about.astro`](./../src/pages/about.astro), lines 51–57. Edit these URLs directly:

```html
<a href="https://discord.gg/<invite-code>" ...>discord</a>
<a href="https://github.com/NUTFLAGGERS" ...>github</a>
<a href="https://ctftime.org/team/<team-id>" ...>ctftime</a>
<a href="https://twitter.com/<handle>" ...>twitter</a>
<a href="mailto:<email@domain.com>">email</a>
```

### About Page — Team Description

Also in [`src/pages/about.astro`](./../src/pages/about.astro), line 25:

```html
<p class="about-text">
  We are NUTFLAGGERS — a student CTF team. We compete, ...
</p>
```

### Homepage "About Us" Blurb

In [`src/pages/index.astro`](./../src/pages/index.astro), around line 201:

```html
<p class="about-text">
  We are NUTFLAGGERS — ...
</p>
```

---

## 12. File Structure Reference

```
website/
├── src/
│   ├── content/                  ← ALL EDITABLE CONTENT HERE
│   │   ├── config.ts             ← Schema validation (don't edit unless adding new fields)
│   │   ├── team/                 ← Team member profiles (.json)
│   │   │   ├── 1-oliver.json
│   │   │   └── ...
│   │   ├── writeups/             ← CTF writeup posts (.md)
│   │   │   └── example_post.md
│   │   ├── events/               ← CTF competition entries (.md)
│   │   │   ├── example_ctf.md
│   │   │   └── example_upcoming_ctf.md
│   │   ├── resources/            ← Curated tools & links (.md)
│   │   │   ├── cryptohack.md
│   │   │   └── ...
│   │   └── projects/             ← Open-source projects (.md)
│   │       └── example_project.md
│   │
│   ├── components/               ← Reusable UI components (rarely need to edit)
│   │   ├── BaseHead.astro        ← SEO meta tags
│   │   ├── Header.astro          ← Site header & nav
│   │   ├── Footer.astro          ← Site footer
│   │   ├── Row.astro             ← Content list row (used everywhere)
│   │   ├── SearchPrompt.astro    ← Terminal-style search filter
│   │   ├── TagBadge.astro        ← Colored category badge
│   │   └── TeamMember.astro      ← Team member display row
│   │
│   ├── layouts/
│   │   └── BaseLayout.astro      ← Page shell (header + footer wrapping)
│   │
│   ├── pages/                    ← Page routes (rarely need to edit)
│   │   ├── index.astro           ← Homepage
│   │   ├── about.astro           ← /about/
│   │   ├── events.astro          ← /events/
│   │   ├── resources.astro       ← /resources/
│   │   ├── projects.astro        ← /projects/
│   │   ├── 404.astro             ← 404 page
│   │   └── writeups/
│   │       ├── index.astro       ← /writeups/ listing
│   │       └── [...slug].astro   ← /writeups/<slug>/ individual post
│   │
│   └── styles/
│       └── global.css            ← Design tokens & global styles
│
├── public/
│   ├── .nojekyll                 ← Required for GitHub Pages (don't delete)
│   └── favicon.svg               ← Site favicon
│
├── astro.config.mjs              ← Astro build configuration
├── package.json                  ← Project dependencies
└── .github/
    └── workflows/                ← GitHub Actions CI/CD pipeline
```

---

## 13. Troubleshooting

### Build fails with "required field missing"

**Cause:** A required frontmatter field is absent or misspelled in a content file.  
**Fix:** Check the error output — it tells you exactly which file and field. Compare with the [Field Reference](#field-reference) for that collection or look at an existing working file.

### Content doesn't appear on site

1. Check the file is in the correct `src/content/<collection>/` directory.
2. Ensure the file extension is `.md` (not `.txt`, no extra spaces).
3. Run `npm run build` — the error output is more descriptive than the dev server.
4. For writeups, check the `pubDate` field uses `"YYYY-MM-DD"` format.

### Writeup page returns 404

- The URL is `/writeups/<filename-without-extension>/`
- Ensure the filename has no spaces (use underscores: `heap_overflow.md`)

### Event doesn't appear as "upcoming"

- The `todayRef` date in `src/pages/index.astro` controls the cutoff. If your event date is before this string, it's treated as past.
- Update `todayRef` to today's date to fix display.

### Team member appears in wrong section / wrong order

- Check `categories` array in their `.json` — it must match the group name exactly (lowercase).
- Rename the number prefix to change order: `6-handle.json` → `3-handle.json`.

### Deployment fails on GitHub Actions

- Go to the **Actions** tab of the repository and open the failing workflow run for the full error log.
- Usually caused by a build error (invalid frontmatter). Fix locally with `npm run build` first.
- If the build passes but deploy is stuck with a yellow clock icon — it's **waiting for reviewer approval**, not broken. A required reviewer needs to approve it in the Actions UI.

### Social link doesn't work for a team member

- Ensure the value starts with `https://` (not just `github.com/...`).
- Empty string `""` disables the link click but still shows the label.

---

> [!TIP]
> When in doubt, copy an existing file that works and modify it. The example files in each collection (`example_post.md`, `example_ctf.md`, etc.) are good starting points.
