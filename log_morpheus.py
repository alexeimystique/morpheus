import os
import json
import datetime


def _ensure_logs_dir():  # Ensures log files and folder are there
    os.makedirs("logs", exist_ok=True)


def load_logs(path):  # Loads NDJSON logs
    if not os.path.exists(path):
        open(path, "x")
        return "Empty file"
    elif os.path.getsize(path) == 0:
        return "Empty file"

    logs = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                logs.append(json.loads(line))
            except json.JSONDecodeError:
                print(f"[log_morpheus.py] Skipping bad line: {line}")
    return logs if logs else "Empty file"


# Just for generating start and end messages
def get_start_message():
    return {"role": "user", "content": "NEW CHAT - Session start time: " +
            datetime.datetime.now().strftime("%Y-%B-%d %H:%M:%S")}


def get_end_message():
    return {"role": "user", "content": "END CHAT - Session end time: " +
            datetime.datetime.now().strftime("%Y-%B-%d %H:%M:%S")}


def append_session_log(time, message, state="in_progress"):  # Appends a message to session log
    _ensure_logs_dir()
    path = f"logs/{time}.ndjson"

    if state == "start":
        # Marker line for session start
        start_marker = get_start_message()
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(start_marker, ensure_ascii=False) + "\n")
        return

    if state == "end":
        # Marker line for session end
        end_marker = get_end_message()
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(end_marker, ensure_ascii=False) + "\n")
        return

    # Normal case: append message in arg
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(message, ensure_ascii=False) + "\n")


def append_total_log(message, state="in_progress"):  # Appends a message to total_log.ndjson.
    _ensure_logs_dir()
    path = "logs/total_log.ndjson"

    if state == "start":
        message = get_start_message()
    if state == "end":
        message = get_end_message()

    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(message, ensure_ascii=False) + "\n")
