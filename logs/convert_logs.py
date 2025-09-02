import json
import os
import argparse

def convert_log_to_txt(json_file, txt_file=None):
    if txt_file is None:
        txt_file = os.path.splitext(json_file)[0] + ".txt"

    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {json_file} not found.")
        return
    except json.JSONDecodeError as e:
        print(f"Error: {json_file} is not a valid JSON. {e}")
        return

    if not isinstance(data, list):
        print(f"Error: Expected a list of messages in {json_file}, got {type(data).__name__}.")
        return

    try:
        with open(txt_file, "w", encoding="utf-8") as out:
            for entry in data:
                if not isinstance(entry, dict):
                    print(f"Skipping invalid entry: {entry}")
                    continue
                role = entry.get("role", "unknown").upper()
                if role == "ASSISTANT":
                    role = "MORPHEUS"
                content = entry.get("content", "").strip()
                if "NEW CHAT - Session start time:" in content or "END CHAT - Session end time:" in content:
                    out.write(f"{content}\n\n")
                else:
                    out.write(f"{role}: {content}\n\n")
    except Exception as e:
        print(f"Error writing {txt_file}: {e}")
        return

    print(f"Converted {json_file} -> {txt_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Morpheus JSON logs to readable TXT.")
    parser.add_argument("json_file", nargs="?", help="Path to the JSON log file.")
    parser.add_argument("txt_file", nargs="?", help="Optional path for output TXT file.")
    args = parser.parse_args()

    if not args.json_file:
        print("This is used to convert JSON log files into easier to read TXT files.")
        # No arguments: ask interactively
        json_file = input("Enter the name of the the JSON log file: ").strip()
        txt_file = input("Enter the name of the output TXT file (leave blank for auto-naming): ").strip() or None
        convert_log_to_txt(json_file, txt_file)
    else:
        convert_log_to_txt(args.json_file, args.txt_file)
