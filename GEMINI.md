# Gemini Context File

This file documents the context, structure, and conventions of the `lucaslowe.com` Hugo project.

## Project Overview
- **Type:** Static Site (Hugo).
- **Theme:** `hugo-bearblog` (submodule).
- **URL:** `https://lucaslowe.com`.
- **Author:** Lucas Lowe.
- **Topics:** Software Engineering, Mobile/Web Dev, Cybersecurity, Retro Tech.

## Directory Structure
- **`content/`**: Markdown content.
  - **`_index.md`**: Homepage/About Me content.
  - **`blog/`**: Blog posts.
  - **`projects/`**: Project portfolio items (Note: Folder is named `projects`, not `portfolio`).
- **`layouts/`**: Custom layout overrides.
  - **`partials/custom_style.html`**: CSS variable overrides and custom styles.
  - **`partials/custom_head.html`**: Custom HTML head elements.
- **`themes/hugo-bearblog`**: The active theme.
- **`hugo.toml`**: Main configuration file.

## Development Workflow
- **Run Local Server:** `hugo server -D` (includes drafts).
- **Build Production:** `hugo`.

## Conventions
- **Frontmatter:** Mixed usage observed.
  - `_index.md` uses TOML (`+++`).
  - Project posts use YAML (`---`).
- **Styling:**
  - CSS variables are defined in `layouts/partials/custom_style.html`.
  - Dark mode support via `@media (prefers-color-scheme: dark)`.

## Key Configuration (`hugo.toml`)
- **BaseURL:** `https://lucaslowe.com`
- **Permalinks:**
  - Blog: `/:slug/`
  - Tags: `/blog/:slug`
- **Params:**
  - `favicon`: `images/favicon.png`
  - `disableKinds`: `["taxonomy"]` (Tag/Category pages might be disabled/hidden unless configured).

## Common Tasks
- **Add New Project:** Create new directory in `content/projects/<project-slug>/` and add `post.md`.
- **Add New Blog Post:** Create new markdown file in `content/blog/`.
- **Update Styles:** Edit `layouts/partials/custom_style.html`.
