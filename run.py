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


def run():
    # Models tried:
    # gpt-oss:20b (takes long, but pretty good);
    # gemma3:12b (relatively similar as gpt-oss but slightly quicker; gets faster as you speak to it);
    # gemma3:4b (fast, but bad. regurgitates the set phrases)
    # llama3.2:3b (fast, but bad.)
    # llama3 (llama3:8b/llama3:latest) (fine, but seems slow.)

    # If ollama yells at you for not having enough memory, restart your computer.
    # gemma3:12b can definitely run on 16GB of RAM, albeit... slow.

    config = {}
    with open("config.cfg", "r", encoding='utf-8') as file:
        for line in file:
            parameter = line.split(" = ")
            config.update({parameter[0]: parameter[1].replace("\n", "")})
    response_time = config.get("response_time") == "1"
    thinking_message = config.get("thinking_message") == "1"
    debug = config.get("debug_message") == "1"
    is_logging = config.get("logging") == "1"

    model_name = config["model_name"]
    print(f"Running on {model_name}.")

    if debug:
        print("Configuration file initialized.")

    with open("system_prompt.txt", "r", encoding='utf-8') as file:
        system_prompt = file.read()

    if debug:
        print("System prompt initialized.")

    if log_morpheus.load_logs("logs/total_log.ndjson") != "Empty file" and is_logging:
        previous_chats = log_morpheus.load_logs("logs/total_log.ndjson")
        # Initialize conversation - load system prompts and previous chats
        messages = [
                       {"role": "system", "content": system_prompt},
                       {"role": "user", "content": " "},
                   ] + previous_chats
    else:
        messages = [
                       {"role": "system", "content": system_prompt},
                       {"role": "user", "content": " "},
                   ]

    if response_time:
        start_time = time.time()

    if debug:
        print("System prompt read.")
    print("Loading... this could take a few minutes depending on your hardware.")

    # This is to get a first response.
    # However, it is very slow for the next response(s) if you do this first,
    # then use the code for the follow-up questions.
    # Better to just start a new chat with a preassigned message from the user ("Hello.")

    # response = ollama.chat(model=model_name, messages=messages)
    # if config["response_time"] == "1":
    #     end_time = time.time() - start_time
    #     print(f"Response time: {int(round(end_time))}s")
    # print("MORPHEUS:", response.message.content)

    session_start_time = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")

    start_message = log_morpheus.get_start_message()

    messages.append(start_message)

    if is_logging:
        log_morpheus.append_total_log(None, "start")
        log_morpheus.append_session_log(session_start_time, None, "start")

    # First response from Morpheus
    response = ollama.chat(model=model_name, messages=messages)
    answer = response.message.content

    if response_time:
        end_time = time.time() - start_time
        print(f"Response time: {int(round(end_time))}s")
    print("MORPHEUS:", answer)

    clock_now = datetime.datetime.now().strftime("%H:%M:%S")
    first_response = {"role": "assistant", "content": answer, "timestamp": clock_now}
    messages.append(first_response)
    if is_logging:
        log_morpheus.append_session_log(session_start_time, messages[-1])
        log_morpheus.append_total_log(messages[-1])

    # Continue the session
    while True:
        user_input = input("USER: ")

        if not user_input:
            messages.append(log_morpheus.get_end_message())  # Technically unnecessary if logging is disabled.
            if is_logging:
                log_morpheus.append_session_log(session_start_time, None, "end")
                log_morpheus.append_total_log(None, "end")
            break  # exit loop - exit program

        clock_now = datetime.datetime.now().strftime("%H:%M:%S")
        user_message = {"role": "user", "content": user_input,  "timestamp": clock_now}
        messages.append(user_message)
        if is_logging:
            log_morpheus.append_session_log(session_start_time, messages[-1])
            log_morpheus.append_total_log(messages[-1])

        if response_time:
            start_time = time.time()
        if thinking_message:
            print("Thinking...")

        response = ollama.chat(model=model_name, messages=messages)
        answer = response.message.content

        if response_time:
            end_time = time.time() - start_time
            print(f"Response time: {int(round(end_time))}s")

        clock_now = datetime.datetime.now().strftime("%H:%M:%S")
        print("MORPHEUS:", answer)
        reply = {"role": "assistant", "content": answer, "timestamp": clock_now}

        messages.append(reply)
        if is_logging:
            log_morpheus.append_session_log(session_start_time, messages[-1])
            log_morpheus.append_total_log(messages[-1])


def edit_config():
    config_dict = {}
    with open("config.cfg", "r", encoding='utf-8') as file:
        for line in file:
            parameter = line.split(" = ")
            print(parameter)
            config_dict.update({parameter[0]: parameter[1].replace("\n", "")})
    for par, value in config_dict.items():
        print(par + " = " + value)

    edit_par = input("Choose parameter to edit: ")
    edit_value = input("Choose new value: ")
    if edit_par == "" or edit_value == "":
        print("Canceled editing config.")
        return
    config_dict.update({edit_par: edit_value})

    config_str = ""
    for par, value in config_dict.items():
        config_str += par + " = " + value + "\n"
    with open("config.cfg", "w", encoding='utf-8') as file:
        file.write(config_str)
    print("Saved to config file.")


def menu():
    print("Welcome to Morpheus. Choose a command:\n"
          "start - Start Morpheus\n"
          "config - Edit configurations\n"
          "quit - Quit\n")
    while True:
        command = input(">: ")
        if command == "start":
            run()
        elif command == "config":
            edit_config()
        elif command == "quit":
            break


menu()
