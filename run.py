import ollama
import time
import datetime
import log_morpheus


print("\n"
"░▒▓██████████████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓███████▓▒░\n"
"░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░\n"        
"░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░\n"        
"░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓███████▓▒░░▒▓████████▓▒░▒▓██████▓▒░ ░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░\n"
"░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░\n"
"░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░\n"
"░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░░▒▓██████▓▒░░▒▓███████▓▒░\n")

# Models tried:
# gpt-oss:20b (takes long, but pretty good);
# gemma3:12b (relatively similar as gpt-oss but slightly quicker; gets faster as you speak to it);
# gemma3:4b (fast, but bad. regurgitates the set phrases)
# llama3.2:3b (fast, but bad.)
# llama3 (llama3:8b/llama3:latest) (fine, but seems slow.)

# If ollama yells at you for not having enough memory, restart.
# gemma3:12b can definitely run on 16GB of RAM, albeit... slow.

model_name = 'gemma3:12b'
print(f"Running on {model_name}.")

config = {}
with open("config.cfg", "r", encoding='utf-8') as file:
    for line in file:
        parameter = line.split(" = ")
        config.update({parameter[0]: parameter[1].replace("\n","")})

if config["debug_message"] == "1":
    print("Configuration file initialized.")

with open("system_prompt.txt", "r", encoding='utf-8') as file:
    system_prompt = file.read()

if config["debug_message"] == "1":
    print("System prompt initialized.")

if log_morpheus.load_logs("logs/total_log.json") != "Empty file":
    previous_chats = log_morpheus.load_logs("logs/total_log.json")
    # Initialize conversation - load system prompts and previous chats
    messages = [
                   {"role": "system", "content": system_prompt},
                   {"role": "user", "content": " "},
               ] + previous_chats
else:
    previous_chats = []
    messages = [
                   {"role": "system", "content": system_prompt},
                   {"role": "user", "content": " "},
               ]

if config["response_time"] == "1":
    start_time = time.time()

if config["debug_message"] == "1":
    print("System prompt read.")
print("Loading... this could take a few minutes.")

# This is to get a first response.
# However, it is very slow for the next response(s) if you do this first, then use the code for the follow-up questions.
# Better to just start a new chat with a preassigned message from the user ("Hello.")

# response = ollama.chat(model=model_name, messages=messages)
# if config["response_time"] == "1":
#     end_time = time.time() - start_time
#     print(f"Response time: {int(round(end_time))}s")
# print("MORPHEUS:", response.message.content)

session_start_time = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")

log_morpheus.save_session_log(session_start_time, None,"start")
session_log_messages = []

start_message = log_morpheus.get_start_message()

messages.append(start_message)
previous_chats.append(start_message)
session_log_messages.append(start_message)

print(messages)

# First response from Morpheus
response = ollama.chat(model=model_name, messages=messages)
answer = response.message.content

if config["response_time"] == "1":
    end_time = time.time() - start_time
    print(f"Response time: {int(round(end_time))}s")
print("MORPHEUS:", answer)

first_response = {"role": "assistant", "content": answer}
messages.append(first_response)
previous_chats.append(first_response)
session_log_messages.append(first_response)
log_morpheus.save_session_log(session_start_time, session_log_messages, "in_progress")
log_morpheus.save_total_log(previous_chats, "in_progress")

# Continue the session
while True:
    user_input = input("USER: ")

    if not user_input:
        messages.append(log_morpheus.get_end_message())
        previous_chats.append(log_morpheus.get_end_message())
        session_log_messages.append(log_morpheus.get_end_message())
        log_morpheus.save_session_log(session_start_time, session_log_messages, "end")
        log_morpheus.save_total_log(previous_chats, "end")
        break  # exit loop - exit program

    user_message = {"role": "user", "content": user_input}
    messages.append(user_message)
    previous_chats.append(user_message)
    session_log_messages.append(user_message)
    log_morpheus.save_session_log(session_start_time, session_log_messages, "in_progress")
    log_morpheus.save_total_log(previous_chats, "in_progress")

    if config["response_time"] == "1":
        start_time = time.time()
    if config["thinking_message"] == "1":
        print("Thinking...")

    response = ollama.chat(model=model_name, messages=messages)
    answer = response.message.content

    if config["response_time"] == "1":
        end_time = time.time() - start_time
        print(f"Response time: {int(round(end_time))}s")

    print("MORPHEUS:", answer)
    reply = {"role": "assistant", "content": answer}

    messages.append(reply)
    previous_chats.append(reply)
    session_log_messages.append(reply)
    log_morpheus.save_session_log(session_start_time, session_log_messages, "in_progress")
    log_morpheus.save_total_log(previous_chats, "in_progress")
