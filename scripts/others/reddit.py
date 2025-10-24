import json
import os
import praw
import re
from datetime import datetime

# Retrieve credentials from environment variables
client_id = os.environ.get("REDDIT_CLIENT_ID")
client_secret = os.environ.get("REDDIT_CLIENT_SECRET")
user_agent = "by u/RealNPC_"
username = "RealNPC_"
password = os.environ.get("REDDIT_PASSWORD")
subreddit_name = os.environ.get("SUBREDDIT")
json_file_path = "./website/meta/cont.json"

def create_reddit_post(title, selftext):
    if not all([client_id, client_secret, user_agent, username, password, subreddit_name]):
        print("Error: One or more Reddit API credentials or the subreddit name are not set as environment variables.")
        return None

    try:
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
            username=username,
            password=password,
        )

        subreddit = reddit.subreddit(subreddit_name)

        # Fetch flair templates and find the one matching "Side Stories"
        flair_id = None
        for flair in subreddit.flair.link_templates:
            if flair['text'].lower() == "side stories":
                flair_id = flair['id']
                break

        if flair_id:
            submission = subreddit.submit(title, selftext=selftext, spoiler=True, flair_id=flair_id)
            print(f"Successfully created spoiler post with flair: {submission.url}")
        else:
            submission = subreddit.submit(title, selftext=selftext, spoiler=True)
            print(f"Successfully created spoiler post (no matching flair found): {submission.url}")
        
        return submission

    except praw.exceptions.RedditAPIException as e:
        print(f"Error creating post: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
        

def unpin_previous_sticky(reddit, subreddit_name):
    try:
        subreddit = reddit.subreddit(subreddit_name)
        search_results = subreddit.search('title:"Side Stories"', sort='new', limit=5)
        print(search_results)
        for post in search_results:
            if isinstance(post, praw.models.Submission):
                if post.author and post.author.name.lower() == username.lower() and post.stickied:
                    if re.match(r"^Side Stories \d{3}", post.title):
                        post.mod.sticky(state=False)
                        print(f"Unpinned previous sticky post: '{post.title}'")
                        return True
        print("No matching stickied post found to unpin.")
        return False
    except praw.exceptions.RedditAPIException as e:
        print(f"Error searching for or unpinning post: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while searching/unpinning: {e}")
        return False


def pin_reddit_post(submission):
    if not submission:
        print("No submission object provided, cannot pin.")
        return

    try:
        subreddit = submission.subreddit
        submission.mod.sticky(state=True, bottom=False)
        print(f"Post '{submission.title}' pinned as the first sticky in r/{subreddit.display_name}")

    except praw.exceptions.RedditAPIException as e:
        print(f"Error pinning post: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while pinning: {e}")

def extract_title_from_json(json_file_path):
    global chapter_number
    try:
        with open(json_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not data or not isinstance(data, list):
                print("Error: Invalid JSON format.")
                return None

            highest_index_entry = max(data, key=lambda item: item.get('index', -1), default=None)

            if highest_index_entry and "index" in highest_index_entry and "title" in highest_index_entry:
                chapter_number = highest_index_entry["index"] + 1
                full_title = highest_index_entry["title"]

                episode_match = re.match(r"(\d+)\s*Episode\s*(\d+)\s*(.*)", full_title)

                if episode_match:
                    episode_number = episode_match.group(2)
                    remaining_title = episode_match.group(3).strip()
                    formatted_title = f"Side Stories {chapter_number} • Episode {episode_number} ‒ {remaining_title} ‒ [Release Discussion]"
                    return formatted_title
                else:
                    print("Warning: Unexpected title format in JSON.")
                    return None
            else:
                print("Error: Could not find 'index' or 'title' in the JSON data.")
                return None
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_file_path}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while reading JSON: {e}")
        return None

if __name__ == "__main__":
    extracted_title = extract_title_from_json(json_file_path)
    current_date = datetime.now().strftime("%d-%m-%Y")

    if not all([client_id, client_secret, user_agent, username, password, subreddit_name]):
        print("Error: Reddit API credentials or subreddit name not fully set. Cannot proceed.")
    elif extracted_title:
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
            username=username,
            password=password,
        )
        unpin_previous_sticky(reddit, subreddit_name)

        selftext = f"""___

**Author:** Sing Shong \\
**Release Date:** {current_date}

Discussion thread for the latest chapter of ORV Side Stories.

___

**Read the chapter**

* [Munipa](https://link.munpia.com/n/104753)
* [Naver](http://naver.me/5eOtt9rN)
* [ORV-Reader](https://orv.pages.dev/stories/cont/read/ch_{chapter_number}) (Low Quality MTL)

___

All Discussions: [Github](https://github.com/Bittu5134/ORV-Reader/discussions) \\
Previous Posts: [Reddit](https://www.reddit.com/r/OmniscientReader/search/?q=author%3Arealnpc_+title%3Adiscussion&type=posts&sort=new) \\
Chapter Comments: [ORV-Reader](https://orv.pages.dev/stories/cont/read/ch_{chapter_number}#comments)

___

- Please support the Authors by purchasing chapters on Munipa or Naver.
- Contact u/jdcomplex and show her proof of purchase to get access to a superior TL of the side stories.
- If for some reason you can't buy the chapters then consider writing Reviews for ORV on Goodreads and/or other places.
- Spreading word about a Story is another good way to show your appreciation for the Authors.

___"""
        new_submission = create_reddit_post(extracted_title, selftext)
        if new_submission:
            pass
            # pin_reddit_post(new_submission)
    else:
        print("Could not extract a valid title. Not creating or pinning Reddit post.")
