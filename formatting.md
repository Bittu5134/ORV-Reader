# Formatting Guide

This guide shows you how to format chapter text files. These special tags help make the story look great on the website!

> [!TIP]
> **New to contributing?** Read the [How to Contribute guide](CONTRIBUTING.md) first to learn how to edit files.

---

## Basic Rules

- Chapter files are simple `.txt` (text) files
- You don't need to create new files—they already exist in the `/chapters` folder
- Use the special tags shown below to format different types of text
- Tags are case-sensitive (use exact capitalization shown)
- The website automatically converts these tags into pretty formatted text

---

## How to Use Tags

### Chapter Title

**Tag:** `<title>`

**What it does:** Sets the chapter title that appears at the top of the page.

**When to use it:** This should always be the very first line in every chapter file.

**Example:**
```
<title>Chapter 1: The Beginning
```

---

### Cover Image

**Tag:** `<cover>`

**What it does:** Adds a cover image at the start of the chapter.

**How to use it:** Write `[image_name][description]` after the tag. Put this right after the title.

**Example:**
```
<cover>[cover.jpg][Cover Image]
```

---

### Empty Lines (Paragraph Breaks)

**How to use it:** Just leave a blank line in your text file.

**What it does:** Creates a space between paragraphs on the website.

**Tip:** Don't add too many blank lines—one is enough!

---

### System Messages

**Tag:** `<!>`

**What it does:** Shows game system messages (like skill activations or status updates).

**When to use it:** For messages that the characters see in their system interface.

**Example:**
```
<!>[Exclusive skill 'Way of the Wind Lv. 10' is activated to the limit!]
```

---

### System Window

**Tag:** `+`

**What it does:** Creates a system window box with information.

**How to use it:** Put `+` on a line before and after the content. Add `[Title Text]` on the first line inside for a window title.

**Example:**
```
+
[People Listed in the Bookmark Slots]
1. The Delusion Demon Kim Namwoon (Understanding 25).
2. Steel Sword Lee Hyunsung (Understanding 35).
3. Empty slot.
+
```

---

### Constellation Speech

**Tag:** `<@>`

**What it does:** Shows dialogue from constellations or other powerful entities (dokkaibe, transcendents, etc).

**When to use it:** When a constellation is speaking directly in their true voice.

**Example:**
```
<@>[These incarnations have gotten really lazy]
```

---

### Outer God Speech

**Tag:** `<#>`

**What it does:** Shows dialogue from outer gods.

**When to use it:** For speech from outergods like the Devourer of dreams, secretive plotter etc.

**Example:**
```
<#>【The void whispers in your mind.】
<#>【...】
```

---

### Quotes

**Tag:** `<&>`

**What it does:** Formats quoted text or special narration.

**How to use it:** Use `<br>` if you want to add an author name or note on a new line within the quote.

**Example:**
```
<&>「 To the Breaking the Sky Sword Namgung Minyoung, the First Murim was home. 」
<&>「...」
<&>「This is the power of Transcendence <br>- Yoo Jonghyuk」
```

---

### Notices (Translator Notes)

**Tag:** `<?>`

**What it does:** Adds helpful notes for readers (like explaining Korean words or cultural references).

**When to use it:** When you want to explain something that might confuse readers.

**Example:**
```
<?>Dokja can mean 'only child', 'reader', or 'individualist' in Korean.
```

---

### Images

**Tag:** `<img>`

**What it does:** Adds an illustration or image in the middle of a chapter.

**How to use it:** Write `[image_name][description]`. The image must already be uploaded to `website/assets/images/`.

**Example:**
```
<img>[Ch00-20 Cover.jpg][Example Image]
```

---

### Section Break

**Tag:** `***`

**What it does:** Creates a horizontal line to separate sections.

**When to use it:** At the end of a chapter or to show a major scene break.

**Tip:** Add blank lines before and after it!

**Example:**
```

***

```

---

## Quick Tips

- Always use tags exactly as shown (they're case-sensitive!)
- Don't use HTML code directly unless you really know what you're doing
- Keep formatting consistent with other chapters
- If you're not sure, look at how other chapters do it
- Your changes will appear on the website after they're approved

---

## Quick Reference Table

Here's a handy table to quickly find the tag you need:

| Tag | What It's For | Example |
|-----|---------------|---------|
| `<title>` | Chapter title | `<title>Chapter 1: The Beginning` |
| `<cover>` | Cover image | `<cover>[cover.jpg][Cover Image]` |
| `<!>` | System messages | `<!>[Skill activated!]` |
| `+` | System window | `+\n[Title]\nContent\n+` |
| `<@>` | Constellation speech | `<@>[The stars are watching you]` |
| `<#>` | Outer god speech | `<#>【The void whispers】` |
| `<&>` | Quotes | `<&>「Quote text」` |
| `<?>` | Notes for readers | `<?>Translation note here` |
| `<img>` | Images | `<img>[image.jpg][Alt text]` |
| `***` | Section break | `\n***\n` |
