import re
import time
import random
from google import genai
import os

api_keys = [os.environ["GEMINI_KEY"]]

random.shuffle(api_keys)

current_api_key_index = 0

# with open("scripts/side/lines.txt", "r", encoding="utf-8") as f:
#    lines = f.read().split("\n")
#    if len(lines)== 0:
#        exit(code=0)

with open("scripts/side/lines.txt", "r", encoding="utf-8") as f:
    lines = f.read().split("\n")
    if lines[0] == "":
        with open("scripts/side/lines.txt", "w", encoding="utf-8") as f:
            f.write("\n")
        exit(code=0)

def get_new_client():
    global current_api_key_index
    api_key = api_keys[current_api_key_index]
    current_api_key_index = (current_api_key_index + 1) % len(api_keys)
    return genai.Client(api_key=api_key)


client = get_new_client()

with open("scripts/side/ai.py", "r", encoding="utf-8") as f:
    csv = f.read()

try:
    chat = client.chats.create(model="gemini-2.0-flash")
    response = chat.send_message(
        "i will send you input sentences and you have to respond with true and false, where true means its a system message and false means its a character dialouge, i will give you a csv encoded text for reffernce, only respond in true or false, the text from next line is for tuning only aslo ignore newlines, everything that i will send you is a sentence from a book, DO not reply with anything other than true or false! \n"
        + csv
    )
    print("Initial context sent successfully!")
except Exception as initial_error:
    print(f"Error sending initial context: {initial_error}")
    client = get_new_client()
    try:
        chat = client.chats.create(model="gemini-2.0-flash")
        response = chat.send_message(
            "i will send you input sentences and you have to respond with true and false, where true means its a system message and false means its a character dialouge, i will give you a csv encoded text for reffernce, only respond in true or false, the text from next line is for tuning only aslo ignore newlines, everything that i will send you is a sentence from a book, DO not reply with anything other than true or false! \n"
            + csv
        )
        print("Initial context sent successfully after error!")
    except Exception as second_initial_error:
        print(f"Failed to send initial context again: {second_initial_error}")
        exit(code=1)

lines = []
data = []
validChars = "abcdefghijklmnopqrstuvwxyz 0123456789'"
csv = open("scripts/side/ai.py", "r", encoding="utf-8").read()



loop = time.time()

while True:
    try:
        if time.time() - loop >= 5:
            with open("scripts/side/lines.txt", "r", encoding="utf-8") as f:
                lines = f.read().split("\n")
                if lines[0] == "":
                    with open("scripts/side/lines.txt", "w", encoding="utf-8") as f:
                        f.write("\n")
                    exit(code=0)
            line = random.choice(lines)
            print(f"Trying Line: {line}")
            lines.remove(line)
            with open("scripts/side/lines.txt", "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            response = chat.send_message(line)
            response = response.text.replace("\n", "").lower()
            print(f"{response} | {line}")
            if response != "true" and response != "false":
                response = "unknown"
                time.sleep(5)
                chat.send_message(
                    "i will send you input sentences and you have to respond with true and false, where true means its a system message and false means its a character dialouge, i will give you a csv encoded text for reffernce, only respond in true or false, the text from next line is for tuning only aslo ignore newlines, everything that i will send you is a sentence from a book, DO not reply with anything other than true or false! \n"
                    + csv
                )
                continue
            with open("scripts/side/data.csv", "a", encoding="utf-8") as f:
                f.write(f"{response},{line}\n")
            
            loop = time.time()
            time.sleep(1)
    except Exception as e:
        print(
            "\n--------------------------------------\n",
            str(e),
            "\n--------------------------------------\n",
        )
        with open("errors.txt", "a") as f:
            f.write(str(e) + "\n--------------------------------------\n")
        client = get_new_client()
        try:
            chat = client.chats.create(model="gemini-2.0-flash")
            response = chat.send_message(
                "i will send you input sentences and you have to respond with true and false, where true means its a system message and false means its a character dialouge, i will give you a csv encoded text for reffernce, only respond in true or false, the text from next line is for tuning only aslo ignore newlines, everything that i will send you is a sentence from a book, DO not reply with anything other than true or false! \n"
                + csv
            )

        except Exception as chat_recreation_error:
            print(f"Failed to recreate chat after error: {chat_recreation_error}")
            time.sleep(5)
            continue

        time.sleep(5)
