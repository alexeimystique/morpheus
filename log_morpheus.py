import os
import json
import datetime


def load_logs(path):  # Returns a list of all logs
    if os.path.exists(path) and os.path.getsize(path) != 0:
        with open(path, "r") as f:
            return json.load(f)
    else:
        return "Empty file"


def create_total_log():  # Creates total log that records all messages of all sessions
    open(f"logs/all_logs.json", "x")


def get_start_message():
    return {"role": "user", "content": "NEW CHAT - Session start time: " +
            datetime.datetime.now().strftime("%Y-%B-%d %H:%M:%S")}


def get_end_message():
    return {"role": "user", "content": "END CHAT - Session end time: " +
            datetime.datetime.now().strftime("%Y-%B-%d %H:%M:%S")}


def save_session_log(time, messages, state):  # Saves session log - also called to save the log after every message.
    if state == "start" and messages is None:  # Creates log
        open(f"logs/{time}.json", "x")
    elif state == "in_progress":
        with open(f"logs/{time}.json", "w") as f:
            json.dump(messages, f, indent=2)
    elif state == "end":
        messages.append(get_end_message())
        with open(f"logs/{time}.json", "w") as f:
            json.dump(messages, f, indent=2)


def save_total_log(chat_log, state):  # Saves total log - also called to save the log after every message.
    if state == "in_progress":
        with open(f"logs/total_log.json", "w") as f:
            json.dump(chat_log, f, indent=2)
    elif state == "end":
        chat_log.append(get_end_message())
        with open("logs/total_log.json", "w") as f:
            json.dump(chat_log, f, indent=2)
