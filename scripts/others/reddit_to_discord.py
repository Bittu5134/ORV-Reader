import praw
import time
import os
import requests
import re
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path # Import Path for cleaner path handling

# --- Configuration ---
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = "OmniscientReaderDiscordBot/1.0 by u/RealNPC_"
SUBREDDIT_NAME = "OmniscientReader"
# DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1383081509287886898/yvNw5rxgq3gfMm7wJzP7XKCgbbdyLiyFM_UjISFfiP3BMGw4IvKKbcFJNjIqTVwXVXLU"

# Define the path for the processed IDs file relative to the script
# This ensures it's always found/created next to the script itself
SCRIPT_DIR = Path(__file__).parent
PROCESSED_IDS_FILE = SCRIPT_DIR / "processed_reddit_post_ids.json"

# --- Functions for loading/saving IDs with timestamps ---
def load_processed_ids(file_path):
    """Loads processed post IDs and their timestamps from a JSON file."""
    processed_data = {}
    if file_path.exists():
        try:
            with open(file_path, 'r') as f:
                loaded_data = json.load(f)
                for post_id, timestamp_str in loaded_data.items():
                    try:
                        processed_data[post_id] = datetime.fromisoformat(timestamp_str)
                    except ValueError:
                        print(f"Warning: Could not parse timestamp for ID {post_id}. Skipping.")
        except json.JSONDecodeError:
            print(f"Warning: Could not decode {file_path}. Starting with empty ID set.")
    return processed_data

def save_processed_ids(file_path, ids_dict):
    """Saves processed post IDs and their timestamps to a JSON file."""
    serializable_data = {
        post_id: dt_obj.isoformat()
        for post_id, dt_obj in ids_dict.items()
    }
    try:
        with open(file_path, 'w') as f:
            json.dump(serializable_data, f, indent=4)
        print(f"Saved {len(ids_dict)} processed IDs to {file_path}")
    except IOError as e:
        print(f"Error saving IDs to {file_path}: {e}")

def convert_reddit_spoiler_to_discord(text):
    """Converts Reddit's >!spoiler!< tag to Discord's ||spoiler|| tag."""
    if not isinstance(text, str):
        return text
    return re.sub(r'>!(.*?)!<', r'|| \1 ||', text, flags=re.DOTALL)

def get_submission_image_url(submission):
    """
    Attempts to get the best image URL for a submission thumbnail.
    Prioritizes preview image for image posts.
    """
    if submission.is_reddit_media_domain:
        if hasattr(submission, 'url') and submission.url.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            return submission.url
        elif hasattr(submission, 'preview') and 'images' in submission.preview and len(submission.preview['images']) > 0:
            return submission.preview['images'][0]['source']['url']
    elif hasattr(submission, 'thumbnail') and submission.thumbnail not in ("self", "default", "nsfw") and submission.thumbnail.startswith(('http', 'https')):
        return submission.thumbnail
    return None

def send_to_discord(submission):
    """Sends a rich embed message to the configured Discord webhook."""
    if not DISCORD_WEBHOOK_URL:
        print("Discord webhook URL not set. Cannot send message.")
        return

    embed_color = 3447003 # A pleasant blue (Hex #3498DB)

    embed_title = convert_reddit_spoiler_to_discord(submission.title)

    description_text = ""
    if submission.is_self:
        description_text = convert_reddit_spoiler_to_discord(submission.selftext)
    elif submission.link_flair_text:
        description_text = f"Link Flair: {submission.link_flair_text}"
    else:
        description_text = "Click the title to view the post!"

    if len(description_text) > 4000:
        description_text = description_text[:4000] + "..."

    content_warnings = []
    if submission.over_18:
        content_warnings.append("NSFW")
    if submission.spoiler:
        content_warnings.append("Spoilers")

    final_content_warning = ", ".join(content_warnings) if content_warnings else "None"

    embed = {
        "title": embed_title,
        "url": submission.url,
        "color": embed_color,
        "description": description_text,
        "fields": [
            {
                "name": "Post Author",
                "value": f"u/{submission.author.name}" if submission.author else "Deleted/Unknown",
                "inline": False
            },
            {
                "name": "Content Warning",
                "value": final_content_warning,
                "inline": False
            }
        ]
    }

    thumbnail_url = get_submission_image_url(submission)
    if thumbnail_url:
        embed["thumbnail"] = {"url": thumbnail_url}

    payload = {
        "embeds": [embed]
    }

    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        response.raise_for_status()
        print("Successfully sent embed message to Discord.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send embed message to Discord: {e}")

def main():
    # fetched_post_ids will now be a dictionary: {id: datetime_processed}
    processed_ids_data = load_processed_ids(PROCESSED_IDS_FILE)
    print(f"Loaded {len(processed_ids_data)} previously processed IDs.")

    new_posts_found_this_run = []

    try:
        reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT
        )

        print(f"Fetching new posts from r/{SUBREDDIT_NAME}...")
        subreddit = reddit.subreddit(SUBREDDIT_NAME)

        new_discord_posts_sent = False

        for submission in subreddit.new(limit=10):
            if submission.id not in processed_ids_data:
                print(f"Found new post: {submission.title} (ID: {submission.id})")
                send_to_discord(submission)
                new_posts_found_this_run.append(submission)
                new_discord_posts_sent = True
                time.sleep(1)
            else:
                print(f"Post {submission.id} already processed. Stopping check for older posts.")
                break

        if not new_discord_posts_sent:
            print("No new Reddit posts found or sent to Discord.")

    except praw.exceptions.APIException as e:
        print(f"Error fetching Reddit posts (PRAW API Exception): {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # --- Update and Clean processed IDs ---
        current_time = datetime.now(timezone.utc)

        for submission in new_posts_found_this_run:
            processed_ids_data[submission.id] = current_time

        cutoff_time = None
        if new_posts_found_this_run:
            oldest_new_post_timestamp = min(
                datetime.fromtimestamp(s.created_utc, tz=timezone.utc)
                for s in new_posts_found_this_run
            )
            cutoff_time = oldest_new_post_timestamp - timedelta(hours=12)
            print(f"Oldest new post timestamp: {oldest_new_post_timestamp.isoformat()}")
            print(f"Cleaning IDs older than: {cutoff_time.isoformat()}")
        else:
            print("No new posts fetched this run, skipping cleanup based on oldest new post.")

        if cutoff_time:
            ids_to_keep = {
                post_id: timestamp_dt
                for post_id, timestamp_dt in processed_ids_data.items()
                if timestamp_dt >= cutoff_time
            }
            removed_count = len(processed_ids_data) - len(ids_to_keep)
            processed_ids_data = ids_to_keep
            if removed_count > 0:
                print(f"Removed {removed_count} old processed IDs.")

        save_processed_ids(PROCESSED_IDS_FILE, processed_ids_data)
        print("Reddit to Discord Bot finished.")

if __name__ == "__main__":
    main()
