import re
import time
import random
from google import genai
import os

# CONFIGURATION
MODEL_ID = "gemini-2.5-flash"  # Standard Flash
LINES_PATH = "scripts/side/lines.txt"
DATA_PATH = "scripts/side/data.csv"
AI_REFERENCE_PATH = "scripts/side/ai.py"

api_keys = [os.environ["GEMINI_KEY"]]
random.shuffle(api_keys)
current_api_key_index = 0

def get_new_client():
    global current_api_key_index
    api_key = api_keys[current_api_key_index]
    current_api_key_index = (current_api_key_index + 1) % len(api_keys)
    return genai.Client(api_key=api_key)

def fallback_drain_all_lines():
    """Copies all remaining lines to data.csv as 'true' when quota is exhausted."""
    print("\n[!] Quota exhausted. Draining all remaining lines as 'true' and exiting.")
    try:
        with open(LINES_PATH, "r", encoding="utf-8") as f:
            remaining_lines = [l.strip() for l in f.readlines() if l.strip()]
        
        if remaining_lines:
            with open(DATA_PATH, "a", encoding="utf-8") as f:
                for line in remaining_lines:
                    f.write(f"true,{line}\n")
            
            # Clear lines file
            with open(LINES_PATH, "w", encoding="utf-8") as f:
                f.write("\n")
        
        print(f"Successfully processed {len(remaining_lines)} lines to {DATA_PATH}.")
        exit(0)
    except Exception as e:
        print(f"Critical failure during fallback: {e}")
        exit(1)

def is_quota_error(e):
    """Helper to detect rate limit / exhausted errors."""
    msg = str(e).lower()
    return "429" in msg or "exhausted" in msg or "limit" in msg

# --- INITIAL SETUP ---
with open(LINES_PATH, "r", encoding="utf-8") as f:
    lines_content = f.read().split("\n")
    if not lines_content or lines_content[0] == "":
        exit(0)

with open(AI_REFERENCE_PATH, "r", encoding="utf-8") as f:
    csv_context = f.read()

client = get_new_client()
prompt_template = (
    "i will send you input sentences and you have to respond with true and false, "
    "where true means its a system message and false means its a character dialouge, "
    "i will give you a csv encoded text for reffernce, only respond in true or false. \n" + csv_context
)

# --- ATTEMPT INITIAL CONTEXT ---
try:
    chat = client.chats.create(model=MODEL_ID)
    chat.send_message(prompt_template)
    print("Initial context sent successfully!")
except Exception as e:
    print(f"Error sending initial context: {e}")
    if is_quota_error(e):
        fallback_drain_all_lines()

    client = get_new_client()
    try:
        chat = client.chats.create(model=MODEL_ID)
        chat.send_message(prompt_template)
        print("Initial context sent successfully after retry!")
    except Exception as e2:
        if is_quota_error(e2):
            fallback_drain_all_lines()
        else:
            print(f"Permanent failure: {e2}")
            exit(1)

# --- MAIN LOOP ---
loop_timer = time.time()

while True:
    try:
        # Check time to respect roughly 10-12 RPM
        if time.time() - loop_timer >= 6:
            with open(LINES_PATH, "r", encoding="utf-8") as f:
                current_lines = [l for l in f.read().split("\n") if l.strip()]
            
            if not current_lines:
                exit(0)

            line = random.choice(current_lines)
            print(f"Processing: {line}")
            
            # Remove line immediately to prevent retrying the same failure
            current_lines.remove(line)
            with open(LINES_PATH, "w", encoding="utf-8") as f:
                f.write("\n".join(current_lines))

            response = chat.send_message(line)
            result = response.text.replace("\n", "").lower().strip()
            
            # Validate output
            if "true" not in result and "false" not in result:
                print(f"Unknown response: {result}")
                time.sleep(5)
                chat.send_message(prompt_template)
                continue

            final_label = "true" if "true" in result else "false"
            with open(DATA_PATH, "a", encoding="utf-8") as f:
                f.write(f"{final_label},{line}\n")
            
            print(f"Result: {final_label}")
            loop_timer = time.time()

    except Exception as e:
        print(f"\nLoop Error: {e}")
        if is_quota_error(e):
            fallback_drain_all_lines()

        with open("errors.txt", "a") as f:
            f.write(str(e) + "\n------------------\n")
        
        # Try to recover for non-quota errors
        client = get_new_client()
        try:
            chat = client.chats.create(model=MODEL_ID)
            chat.send_message(prompt_template)
        except Exception as recovery_error:
            if is_quota_error(recovery_error):
                fallback_drain_all_lines()
            time.sleep(10)
            continue
