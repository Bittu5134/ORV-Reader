# How to Contribute

Welcome to the ORV-Reader project! This guide will help you make your first contribution. Don't worry if you've never used GitHub before—we'll walk you through everything step by step!

---

## What's Inside This Guide

1. [How to Edit Files](#how-to-edit-files)
2. [What You Can Edit](#what-you-can-edit)
3. [Adding Images](#adding-images)
4. [Important Notes](#important-notes)

---

## How to Edit Files

Don't worry if this is your first time using GitHub! Just follow these simple steps:

### Easy Step-by-Step Guide

1. **Find the Edit Button:** On the chapter page you want to edit, look for the pencil icon (✏️) at the top and click it.

2. **You'll Go to GitHub:** The website will take you to a page showing the chapter text file.

3. **Sign In (or Create an Account):** 
   - If you already have a GitHub account, sign in
   - If not, you can create a free account—it only takes a minute!

4. **Click Edit:** Look for another pencil icon or a button that says "Edit this file" and click it.

5. **GitHub Will Make a Copy:** GitHub will automatically create your own copy of the project (this is called a "fork"). Don't worry—this is normal and safe!

6. **Make Your Changes:** Now you can edit the text! Use the online editor to fix typos, add tags, or make other improvements.

7. **Describe Your Changes:** Scroll down to the bottom. You'll see boxes where you can:
   - Write a short title describing what you changed (e.g., "Fixed typo in Chapter 5")
   - Add more details if needed (optional)

8. **Click "Propose changes":** This green button saves your edits.

9. **Create a Pull Request:** 
   - A new page will open with another green button that says **"Create pull request"**
   - Click it once
   - Another page appears—click **"Create pull request"** one more time
   - That's it! You've just contributed! 🎉

> [!TIP]
> **Quick Tip:** When you make more edits in the future, GitHub might ask if you want to create a new branch. Choose the option to **"commit to main branch"** to keep things simple. Also, remember to sync your copy of the project regularly to get the latest updates!

---

## What You Can Edit

All chapter files are stored in text files that you can edit. Here are the most helpful ways you can contribute:

- **Fix Spelling and Grammar:** Spot a typo? Fix it! Every correction helps.
- **Fix Formatting:** Make sure system messages, constellation speech, and outer god dialogues use the right tags.
- **Improve the Story Text:** Add missing tags or improve how the text is formatted.

> [!IMPORTANT]
> **Need help with tags?** Check out the [Formatting Guide](./formatting.md) to learn how to use special tags like `<!>` for system messages, `<@>` for constellation speech, and more!

---

## Adding Images

Want to add artwork or cover images to chapters? That's awesome! Here's how:

### How to Add an Image

1. **Upload the Image:** 
   - Go to the `website/assets/images` folder
   - Upload your image with a clear name (example: `CH512-01.jpg`)

2. **Add the Image Tag:** 
   - Open the chapter text file you want to add the image to
   - Use the special `<img>` tag to insert it

3. **Check the Format:** 
   - Look at the [Formatting Guide](./formatting.md) to make sure you're using the right format

### Example

```
<img>[CH512-01.jpg][Illustration for Chapter 512]
```

This tells the website: "Show the image `CH512-01.jpg` with the description 'Illustration for Chapter 512'"

---

## Important Notes

- **Use the Formatting Guide:** Always check the [Formatting Guide](./formatting.md) to make sure you're using tags correctly.
- **Don't Edit HTML Files:** The website automatically creates HTML files from the text files. Only edit the `.txt` chapter files, not the `.html` files.
- **Need Help?** If you're confused about something, just ask! Open an issue on GitHub and we'll help you out.
- **Be Patient:** After you submit your changes, someone will review them. This might take a little time, so please be patient!

---

Thank you for helping make ORV-Reader better for everyone! Every contribution, no matter how small, makes a difference. 💜
