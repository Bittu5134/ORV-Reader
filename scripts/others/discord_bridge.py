import os
import json
import requests
import re
import sys
from better_profanity import profanity


def main():
    # --- ONLINE PROFANITY LIST SETUP ---
    PROFANITY_URL = "https://raw.githubusercontent.com/Bittu5134/ORV-Reader/refs/heads/main/scripts/others/filtered_profanity.txt"
    WHITELIST = {"word1", "word2"}
    CUSTOM_TRIGGERS = ["spoiler", "spoil", "bittu", "realnpc", "bittu5134", "@bittu5134"]

    try:
        response = requests.get(PROFANITY_URL, timeout=10)
        if response.status_code == 200:
            external_words = response.text.splitlines()
            filtered_list = [
                w.strip().lower()
                for w in external_words
                if w.strip().lower() not in WHITELIST
            ]
            final_list = list(set(filtered_list + CUSTOM_TRIGGERS))

            profanity.load_censor_words(final_list)
        else:
            profanity.load_censor_words(CUSTOM_TRIGGERS)
    except Exception as e:
        profanity.load_censor_words(CUSTOM_TRIGGERS)

    # --- PRODUCTION CONFIG ---
    try:
        webhook_url = os.environ["DISCORD_MAIN"]
        github_token = os.environ["GITHUB_TOKEN"]
        event_path = os.environ["GITHUB_EVENT_PATH"]
        with open(event_path, "r") as f:
            data = json.load(f)
    except KeyError as e:
        print(f"Error: Missing environment variable {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: Event file not found.")
        sys.exit(1)

    # 2. Extract Variables
    try:
        comment = data["comment"]
        discussion = data["discussion"]
        raw_body = comment["body"]
        node_id = comment["node_id"]
    except KeyError as e:
        print(f"Error parsing JSON data: {e}")
        sys.exit(1)

    # ==============================================================================
    # PATH A: GitHub Sanitization (Fixes broken tags in the GitHub Web UI)
    # ==============================================================================

    # Allowlist of real HTML tags
    ALLOWED_TAGS = {
        "br", "b", "i", "strong", "em", "code", "pre", "a", "img",
        "p", "div", "span", "details", "summary", "spoiler",
        "ul", "ol", "li"
    }

    def escape_pseudo_tags(match):
        full_match = match.group(0)
        tag_content = match.group(1)

        # Extract tag name (remove attributes, handle closing tags)
        tag_name = tag_content.split()[0].lstrip("/").lower()

        # If it's a real HTML tag → leave it unchanged
        if tag_name in ALLOWED_TAGS:
            return full_match

        # Otherwise → escape it
        return f"\\<{tag_content}\\>"

    # Match ANY <something> but not HTML comments
    regex_pattern = r"<(?!!--)([^>]+)>"

    sanitized_github_body = re.sub(regex_pattern, escape_pseudo_tags, raw_body)

    # Only patch if changes are needed
    if sanitized_github_body != raw_body:
        print("Detected pseudo-tags. Patching GitHub comment...")

        query = """
        mutation($id: ID!, $body: String!) {
          updateDiscussionComment(input: {commentId: $id, body: $body}) {
            comment { body }
          }
        }
        """
        variables = {"id": node_id, "body": sanitized_github_body}
        headers = {
            "Authorization": f"Bearer {github_token}",
            "Content-Type": "application/json",
        }

        response = requests.post(
            "https://api.github.com/graphql",
            json={"query": query, "variables": variables},
            headers=headers,
        )

        if response.status_code != 200:
            print(f"Failed to patch GitHub comment: {response.text}")
        else:
            print("Successfully patched GitHub comment.")

    # ==============================================================================
    # PATH B: Discord Formatting (Prepares clean text for the Embed)
    # ==============================================================================

    # 1. Remove invisible HTML comments
    discord_body = re.sub(r"<!--.*?-->", "", raw_body, flags=re.DOTALL)

    # 2. Fix Quotes: ">Text" -> "> Text"
    discord_body = re.sub(r"^>(?=[^\s])", "> ", discord_body, flags=re.MULTILINE)

    # 3. Fix Headers: "# Header" -> "**Header**"
    discord_body = re.sub(r"^#+\s+(.*?)$", r"**\1**", discord_body, flags=re.MULTILINE)

    # 4. Check Triggers (Spoilers / Profanity)
    # Note: triggers list is now handled inside profanity lib via add_censor_words
    ping_str = None

    if profanity.contains_profanity(discord_body):
        ping_str = "||<@818428347151024199>||"

    # 5. Extract Image (Markdown or HTML)
    img_match = re.search(
        r"!\[.*?\]\((https?://.*?)\)|<img\s+[^>]*src=\"([^\"]+)\"", discord_body
    )
    image_url = img_match.group(1) or img_match.group(2) if img_match else None

    # 6. Build Embed
    embed = {
        "title": discussion["title"],
        "url": comment["html_url"],
        "color": 0x32B37,
        "author": {
            "name": comment["user"]["login"],
            "url": comment["user"]["html_url"],
            "icon_url": comment["user"]["avatar_url"],
        },
        "description": discord_body,
    }

    # Attach Image
    if image_url:
        embed["image"] = {"url": image_url}


    # 7. Send to Discord
    payload = {"embeds": [embed]}
    if ping_str:
        payload["content"] = ping_str

    try:
        resp = requests.post(webhook_url, json=payload)
        resp.raise_for_status()
        print("Successfully posted to Discord.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Discord webhook: {e}")


if __name__ == "__main__":
    main()
