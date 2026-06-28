import re
import os
import sys
import json
import requests

# --- Configuration ---
INPUT_DIR = "chapters/cont"
CONT_JSON_PATH = "./website/meta/cont.json"
CONT_META_PATH = "./website/meta/cont_meta.json"

REPO_OWNER = "bittu5134"
REPO_NAME = "orv-reader"
CATEGORY_NAME = "General"  

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GRAPHQL_URL = "https://api.github.com/graphql"

if not GITHUB_TOKEN:
    print("❌ Build Failure: GITHUB_TOKEN environment variable is not set.")
    sys.exit(1)

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Content-Type": "application/json",
}


def run_graphql_query(query, variables=None):
    """Executes a GraphQL query/mutation, crashing the build on any upstream errors."""
    try:
        response = requests.post(
            GRAPHQL_URL,
            json={"query": query, "variables": variables or {}},
            headers=HEADERS,
            timeout=15,
        )
        response.raise_for_status()
        payload = response.json()

        if "errors" in payload:
            print(f"❌ GraphQL Error Response: {payload['errors']}")
            sys.exit(1)

        return payload.get("data", {})
    except Exception as e:
        print(f"❌ API Connection Exception: {e}")
        sys.exit(1)


def get_repo_and_category_ids():
    """Fetches the internal global GraphQL Node IDs required for creating discussions."""
    query = """
    query($owner: String!, $name: String!) {
      repository(owner: $owner, name: $name) {
        id
        discussionCategories(first: 10) {
          nodes {
            id
            name
          }
        }
      }
    }
    """
    data = run_graphql_query(query, {"owner": REPO_OWNER, "name": REPO_NAME})
    repo_node = data.get("repository", {})
    repo_id = repo_node.get("id")

    categories = repo_node.get("discussionCategories", {}).get("nodes", [])
    category_id = None
    for cat in categories:
        if cat["name"] == CATEGORY_NAME:
            category_id = cat["id"]
            break

    if not repo_id or not category_id:
        print(f"❌ Failed to resolve IDs for repo or category '{CATEGORY_NAME}'")
        sys.exit(1)

    return repo_id, category_id


def check_existing_discussion(title):
    """Searches if an exact discussion title match already exists inside the repository."""
    query = """
    query($searchQuery: String!) {
      search(query: $searchQuery, type: DISCUSSION, first: 10) {
        nodes {
          ... on Discussion {
            title
            number
          }
        }
      }
    }
    """
    # Clean/Escape keywords to narrow search tracking down cleanly
    cleaned_keywords = re.sub(r"[^\w\s]", "", title)
    search_query = f"repo:{REPO_OWNER}/{REPO_NAME} in:title {cleaned_keywords}"

    data = run_graphql_query(query, {"searchQuery": search_query})
    nodes = data.get("search", {}).get("nodes", [])

    for node in nodes:
        if node and node.get("title", "").strip() == title.strip():
            return int(node["number"])

    return None


def create_new_discussion(repo_id, category_id, title, body):
    """Creates a fresh GitHub Discussion thread and returns its numeric sequence ID."""
    mutation = """
    mutation($repoId: ID!, $catId: ID!, $title: String!, $body: String!) {
      createDiscussion(input: {repositoryId: $repoId, categoryId: $catId, title: $title, body: $body}) {
        discussion {
          number
        }
      }
    }
    """
    variables = {"repoId": repo_id, "catId": category_id, "title": title, "body": body}
    print(f'⏳ Creating a brand new discussion: "{title}"...')
    data = run_graphql_query(mutation, variables)

    disc_num = data.get("createDiscussion", {}).get("discussion", {}).get("number")
    if not disc_num:
        print(f"❌ Failed to extract created discussion sequence layout information.")
        sys.exit(1)

    return int(disc_num)


def main():
    # 1. Open the existing meta file first to evaluate what has already been indexed
    existing_map = {}
    if os.path.exists(CONT_JSON_PATH):
        try:
            with open(CONT_JSON_PATH, "r", encoding="utf-8") as f:
                old_data = json.load(f)
                # Map index -> existing data dict
                existing_map = {
                    item["index"]: item for item in old_data if "index" in item
                }
        except Exception as e:
            print(f"⚠️ Could not parse existing cont.json file: {e}. Starting fresh.")

    titles = []

    # 2. Iterate and scan filesystem directories
    if not os.path.exists(INPUT_DIR):
        print(f"❌ Build Failure: Input directory '{INPUT_DIR}' does not exist.")
        sys.exit(1)

    for file_index, file in enumerate(os.listdir(INPUT_DIR)):
        if not file.endswith(".txt"):
            continue

        with open(f"./{INPUT_DIR}/{file}", "r", encoding="utf-8") as f:
            textStr = f.read()
            text = textStr.split("\n")

        chapter_index = int(file.replace(".txt", "")) - 1
        chapter_title = text[0].replace("<title>", "").strip()

        titles.append(
            {
                "index": chapter_index,
                "title": chapter_title,
                "discussion": None,  # Initial placeholder value
            }
        )

    # Keep layout ordered cleanly by numeric chapter sequence values
    titles = sorted(titles, key=lambda d: d["index"])

    # 3. Only evaluate API states for entries that don't exist yet, or lack a proper discussion key
    repo_id, category_id = None, None

    for item in titles:
        t_name = item["title"]
        idx = item["index"]

        # Check if this index was already completely verified in previous runs
        if (
            idx in existing_map
            and existing_map[idx].get("discussion") is not None
        ):
            old_title = existing_map[idx].get("title", "")
            if old_title != t_name:
                print(
                    f'⏩ [{idx + 1}] Title updated: "{old_title}" -> "{t_name}". Reusing existing discussion ID.'
                )
            else:
                print(
                    f'⏩ [{idx + 1}] Skipping verification: "{t_name}" already exists in records.'
                )
            item["discussion"] = existing_map[idx]["discussion"]
            continue

        # Target item is confirmed brand new or incomplete! Run processing logic
        print(f'🔍 [{idx + 1}] Processing new entry entry block: "{t_name}"')

        # Check if discussion already exists live on GitHub first
        existing_id = check_existing_discussion(t_name)

        if existing_id:
            print(f"   ✨ Located matching thread live on GitHub: #{existing_id}")
            item["discussion"] = existing_id
        else:
            # Lazy load IDs only if a modification action becomes mandatory
            if not repo_id or not category_id:
                repo_id, category_id = get_repo_and_category_ids()

            body_content = f"https://orv.pages.dev/stories/cont/read/ch_{idx + 1}"
            new_id = create_new_discussion(repo_id, category_id, t_name, body_content)
            print(f"   ✅ Discussion created successfully! Saved ID: #{new_id}")
            item["discussion"] = new_id

    # 4. Save payloads safely to local disk profiles
    os.makedirs(os.path.dirname(CONT_JSON_PATH), exist_ok=True)
    with open(CONT_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(titles, f, indent=2, ensure_ascii=False)

    with open(CONT_META_PATH, "w", encoding="utf-8") as f:
        f.write(
            json.dumps(
                {
                    "title": "Omniscient Reader's Viewpoint Sequel (Ch 553+)",
                    "author": "Sing Shong",
                    "chapters": len(titles),
                    "status": "Ongoing",
                },
                indent=2,
                ensure_ascii=False,
            )
        )

    # 5. Build presentation strings for diagnostic feedback logs
    print("\n" + "=" * 20 + " GENERATED NAVIGATION CODES " + "=" * 20)
    for index, item in enumerate(titles):
        print(
            f"""<div class="chapter_item"><p><a href="#chapter{index}">{item["title"]}</a></p></div>"""
        )


if __name__ == "__main__":
    main()
