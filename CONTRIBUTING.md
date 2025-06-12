# Contribution Guide

This guide provides detailed instructions on how to contribute to the ORV-Reader project. Whether you're fixing typos, adding images, or improving the front end, your contributions are welcome!

---

## Index
1. [Editing Files](#how-to-edit-files)
2. [What You Can Edit](#what-you-can-edit)
3. [Adding Images](#adding-images)
4. [Improving the Front End](#improving-the-front-end)
5. [Important Notes](#important-notes)

---

## How to Edit Files

1.  **Click the Pencil Icon:** Locate and click the pencil icon (✏️) at the top of the webpage.

2.  **GitHub Redirection:** You'll be taken to the text file on the GitHub website.

3.  **Sign In/Up:** Log in to your existing GitHub account or create a new one.

4.  **File View:** You'll see the content of the text file.

5.  **"Edit this file" Button:** Look for and click the button that allows you to edit the file (it might still be a pencil icon or text like "Edit this file").

6.  **Forking (If Necessary):** GitHub might create a copy ("fork") of the project in your account.

7.  **Make Edits:** Use the online text editor to modify the file content.

8.  **"Propose changes":** Scroll down and describe your changes in the provided fields (title and optional description).

9.  **Click "Propose changes":** Submit your edits.

10.  After clicking on "Propose Changes", a new page will open. Click on **Create pull request** which is a *green* colour button. Again on the next page click on **Create pull request**. Congrats! You have contributed to this site and improved it for everyone.

> [!NOTE]
> Make sure you are not creating new branch everything you make an edit, when prompted choose the `commit to main brach option` and periodically keep syncing your repository to keep it upto date.

---

### What You Can Edit
- Fix typos or grammatical errors.
- Correct system message types, constellation speech, or outer god dialogues.
- Add missing tags or improve formatting.

Refer to the [Formatting Guide](./formatting.md) for detailed instructions on using tags and formatting styles.

---

## Adding Images

You can contribute by adding illustrations and cover images to the chapters.

### Steps to Add Images
1. Upload the image to the `website/assets/images` folder with a unique name (e.g., `CH512-01.jpg`).
2. Edit the corresponding chapter file to include the image using the `<img>` tag. Refer to the [Formatting Guide](./formatting.md) for the correct syntax.

Example:
```
<img>[CH512-01.jpg][Illustration for Chapter 512]
```

---

## Improving the Front End

If you're up for a challenge, you can contribute to improving the front end of the website.

### Front-End Files
- All front-end files are located in the `/website` directory.
- The files for individual chapters are dynamically generated using GitHub Actions. To edit these, modify the corresponding `template.html` files:
  - `website/stories/orv/read/template.html`
  - `website/stories/cont/read/template.html`
  - `website/stories/side/read/template.html`

### Important Notes
- Do not copy-paste content between template files. Each template contains unique data tags that must remain intact.
- Test your changes locally before submitting a pull request.

---

## Important Notes

- Always follow the [Formatting Guide](./formatting.md) to ensure consistency.
- Avoid making unnecessary changes to dynamically generated files.
- If you're unsure about anything, feel free to open an issue on GitHub for clarification.
- Be respectful and patient during the review process.

Thank you for contributing to the ORV-Reader project!
