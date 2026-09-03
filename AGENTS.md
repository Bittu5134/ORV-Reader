# AGENTS.md — Repository Guide & AI Agent Directives

> **Project**: *Omniscient Reader's Viewpoint* (ORV) Side Stories Reader  
> **Platform**: Static HTML Reader hosted on Cloudflare Pages  
> **Primary Maintainer/Persona**: Antigravity (Head Editor, Translator & Integrator)

---

## 1. Repository Architecture & Directory Structure

```text
ORV-Reader/
├── chapters/
│   └── cont/                # Source .txt files for Side Story chapters (553+)
├── website/
│   ├── assets/              # CSS, JS, fonts, and images
│   ├── meta/                # Discussion mappings and site metadata (e.g., cont.json)
│   └── stories/cont/read/   # Generated HTML chapter pages (ch_*.html) & template.html
├── scripts/
│   └── side/
│       ├── htmlBuilder.py   # Primary script compiling chapters/cont/*.txt -> website/stories/cont/read/ch_*.html
│       ├── titles.py        # Chapter title management
│       └── data.csv         # Chapter metadata registry
├── reference/
│   ├── soul.md              # Antigravity's core directives, rules, & persona
│   ├── TL_Reference.md      # Official term mappings, constellation names, & search regexes
│   └── TL_Questions.md      # Open lore / translation queries requiring user review
├── formatting.md            # Novel formatting and system tag documentation
├── CONTRIBUTING.md          # Contribution guidelines for human users
└── package.json             # NPM project configuration
```

---

## 2. Core Operational Rules for AI Agents

### Rule 1: Source File Editing Only
* **Never edit HTML files directly** in `website/stories/cont/read/`.
* Always make changes inside the source text files in [`chapters/cont/*.txt`](file:///home/bittu/Developer/projects/ORV-Reader/chapters/cont/).
* Recompile the site after making edits by running the HTML builder script.

### Rule 2: Strict Git Policy (No Auto-Commit / No Auto-Push)
* **Never** automatically run `git commit`, `git merge`, or `git push` on your own.
* Keep all modifications in your local working directory unless the user explicitly commands a commit, merge, or push.

### Rule 3: Precise Location Reporting
* Always report the exact absolute/relative file paths and chapter numbers whenever edits, translations, or formatting changes are executed.
* Example: Modified [`chapters/cont/1059.txt`](file:///home/bittu/Developer/projects/ORV-Reader/chapters/cont/1059.txt) (Episode 66 (7)).

### Rule 4: Line Break & Spacing Standards
* A single newline `\n` is compiled directly into a line break (`<p class="orv_line">`).
* Do **NOT** insert empty blank lines between dialogue or narration lines unless creating a deliberate paragraph break or using section breaks (`***` or `<br>`).

---

## 3. Translation & Lore Rules

| Term / Lore Concept | Standard Translation / Rule | Incorrect / Prohibited Variants |
| :--- | :--- | :--- |
| **Sneaky Schemer vs. Secretive Plotter** | `Sneaky Schemer` (야비한 모략가) and `Secretive Plotter` (은밀한 모략가) are **two different entities**. Do NOT replace `Sneaky Schemer` in chapters where he appears. | Replacing `Sneaky Schemer` with `Secretive Plotter` |
| **Oldest Dream** | Always use **Oldest Dream** (or **Oldest Dreams** in plural). | "Most Ancient Dream" |
| **[Fate]** | Always use **`[Fate]`** (bracketed system term) or **`fate`** (lowercase narrative term). | "[Destiny]", "destiny" |
| **41st Turn Yoo Joonghyuk's Weapon** | Uses a **great spear** (Dark Heavenly Moon Spear). Do not translate as a sword. | "blade", "sword", "halberd" |
| **Shin Yoosung** | Always spell as **Shin Yoosung**. | "Shin Yooseung", "Shin Yoosoung" |
| **Jang Hayoung Pronouns** | `he/him/his` when referred to by others; `she/her/hers` when self-referencing or among close companions. | Standardizing strictly to one set of pronouns |
| **Unique Skill/Item Names** | Use singular form (e.g., **Unrealized Thought**). | "Unrealized Thoughts", "Unformed Idea" |
| **Emotional Authenticity** | Do not sanitize or tone down swearing, angry dialogue, or slurs. Preserve "bastard", "punk", etc., as written. | Softening character dialogue |

---

## 4. Text Tagging Standards (`formatting.md`)

When processing or editing chapter text in `chapters/cont/*.txt`, use the following custom tags:

* `<title>` — Must be the very first line of the file. (e.g., `<title>1059 Episode 66. The Wolf That Swallowed a God (7)`)
* `<!>` — System messages (rendered as `<div class="orv_system">`)
* `<@>` — Constellation true voice speech (rendered as `<div class="orv_constellation">`)
* `<#>` — Outer God speech (rendered as `<div class="orv_outergod">`)
* `<&>` — Quoted text / internal monologues / book quotes (rendered as `<div class="orv_quote">`)
* `<?>` — Translator / Editor notes (rendered as `<div class="orv_notice">`)
* `+` ... `+` — System window box block
* `<img>[filename.jpg][Alt text]` — Embedded chapter illustration

---

## 5. Development & Build Commands

### Rebuilding Reader HTML Pages
To compile all `.txt` files from `chapters/cont/` into HTML pages in `website/stories/cont/read/`:
```bash
python3 scripts/side/htmlBuilder.py
```

### Local Dev Server (Cloudflare Pages)
To launch the local development server for previewing website changes:
```bash
npx wrangler pages dev website
```
*(Alternative simple static server)*:
```bash
npx http-server website
```
