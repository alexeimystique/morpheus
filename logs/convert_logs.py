import json
import os
import argparse


def ndjson_to_txt(ndjson_path, txt_path=None):
    """Convert NDJSON log into a readable transcript."""
    if not os.path.exists(ndjson_path):
        raise FileNotFoundError(f"No such file: {ndjson_path}")

    lines = []
    with open(ndjson_path, "r", encoding="utf-8") as f:
        for raw in f:
            raw = raw.strip()
            if not raw:
                continue
            try:
                entry = json.loads(raw)
                role = entry.get("role", "unknown").upper()
                if role == "ASSISTANT":
                    role = "MORPHEUS"
                content = entry.get("content", "").strip()
                timestamp = entry.get("timestamp")
                if "NEW CHAT - Session start time:" in content or "END CHAT - Session end time:" in content:
                    lines.append(f"\n--- {content} ---\n")
                else:
                    lines.append(f"[{timestamp}] [{role}] {content}")
            except json.JSONDecodeError:
                continue

    if txt_path is None:
        txt_path = ndjson_path.replace(".ndjson", ".txt")

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Converted {ndjson_path} -> {txt_path} with {len(lines)} lines.")


def batch_convert_logs(folder):
    """Convert all .ndjson logs in a folder to .txt transcripts."""
    if folder is None:
        folder = os.getcwd()
    if not os.path.exists(folder):
        print(f"No such folder: {folder}")
        return

    files = [f for f in os.listdir(folder) if f.endswith(".ndjson")]
    if not files:
        print("No .ndjson files found.")
        return

    for f in files:
        path = os.path.join(folder, f)
        print(f"Converting {path}...")
        try:
            ndjson_to_txt(path)
        except Exception as e:
            print(f"Error converting {path}: {e}")

    print("Batch conversion complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Morpheus NDJSON logs to readable TXT.")
    parser.add_argument("json_file", nargs="?", help="Path to the NDJSON log file.")
    parser.add_argument("txt_file", nargs="?", help="Optional path for output TXT file.")
    args = parser.parse_args()

    if not args.json_file:
        print("This is used to convert NDJSON log files into easier to read TXT files.")
        # If no arguments are present, just ask.
        if input("Do you want to batch convert all NDJSON log files in a folder into TXT files? (y/n): ") == "y":
            batch_path = input("Path to logs (leave blank if this script is in the folder): ").strip() or None
            batch_convert_logs(batch_path)
        else:
            json_file = input("Enter the name of the the NDJSON log file: ").strip()
            txt_file = input("Enter the name of the output TXT file (leave blank for auto-naming): ").strip() or None
            ndjson_to_txt(json_file, txt_file)
    else:
        ndjson_to_txt(args.json_file, args.txt_file)
