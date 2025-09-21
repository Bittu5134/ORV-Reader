# Formatting Guide for Contributors

This guide outlines the formatting rules for creating content in the [`/chapters/*`](/chapters) directory. The [`htmlBuilder.py`](/scripts/side/htmlBuilder.py) script processes these files and converts them into HTML for the website.

---

## General Rules
- Each file should be a `.txt` file.
- Files are automatically added; manual addition is not required.
- Use the specified tags and formatting styles for consistency.
- Avoid leaving unformatted content; use the appropriate tags for each type of text.
- Please read the [How to Contribute Guide](CONTRIBUTING.md) before proceeding here.

---

## Supported Tags and Their Usage

### Title
- Use `<title>` to define the title of the chapter.
- This should be the very first line in the file.
- Example:
  ```
  <title>Chapter 1: The Beginning
  ```

### Cover Images
- Use `<cover>` with the format `[image_path][alt_text]` for cover images.
- Place this tag immediately after the `<title>` tag.
- Example:
  ```
  <cover>[cover.jpg][Cover Image]
  ```

### Empty Lines
- Leave an empty line in the text file to insert a `<br>` tag in the HTML.
- Avoid adding unnecessary empty lines; the website automatically adjusts spacing.

### System Messages
- Use `<!>` for system messages.
- These appear as messages shown to the incarnations.
- Example:
  ```
  <!>[Exclusive skill 'Way of the Wind Lv. 10' is activated to the limit!]
  ```

### System Window
- Use `+` before and after text for system messages.
- adding a line inside `[...]` turns it into the title of the window
- These appear as windows shown to the incarnations.
- Example:
```
+
[People Listed in the Bookmark Slots]
1. The Delusion Demon Kim Namwoon (Understanding 25).
2. Steel Sword Lee Hyunsung (Understanding 35).
3. Empty slot.
+
```

### Constellation Speech
- Use `<@>` for constellation speech.
- These are dialogues spoken by constellations.
- Example:
  ```
  <@>[The stars are watching you].

  ```

### Outer God Speech
- Use `<#>` for outer god speech.
- These are dialogues spoken by outer gods, including nameless ones or powerful entities like the Dream Eater.
- Example:
  ```
  <#>【The void whispers in your mind.】
  <#>【...】
  ```

### Quotes
- Use `<&>` for quotes.
- For quotes with additional context (e.g., author names), use `<br>` for line breaks.
- Example:
  ```
  <&>「 To the Breaking the Sky Sword Namgung Minyoung, the First Murim was home. 」
  <&>「...」
  <&>「This is the power of Transcendence <br>- Yoo Jonghyuk」
  ```

### Notices
- Use `<?>` for notices.
- These provide side notes or translator notes for readers.
- Example:
  ```
  <?>Dokja can mean 'only child', 'reader', or 'individualist' in Korean.
  ```

### Images
- Use `<img>` with the format `[image_path][alt_text]` for images.
- `image_path` should match the file name in the [`website/assets/images/`](/website/assets/images) directory.
- Example:
  ```
  <img>[Ch00-20 Cover.jpg][Example Image]
  ```

### Horizontal Rules
- Use `***` for horizontal ruler.
- its recommended to add blank lines before and after it.
- These signify section breaks and should be used at the end of chapters.
- Example:
  ```
  
  ***
  
  ```

---

## Notes
- Ensure all tags are properly closed where applicable.
- Avoid using unsupported tags or raw HTML unless explicitly required.
- Do not add unnecessary empty lines.
