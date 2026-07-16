"""Turn raw BAD-ACTS result JSONs into human-readable TXT and structured JSON logs.

Reads results/*.json and writes readable_results/txt/*.readable.txt and
readable_results/json/*.readable.json. Paths are anchored to the repository root, so this
script works regardless of the current working directory.
"""

import json
from pathlib import Path
from datetime import datetime


ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results"
OUTPUT_ROOT = ROOT / "readable_results"
TXT_DIR = OUTPUT_ROOT / "txt"
JSON_DIR = OUTPUT_ROOT / "json"


def safe_json_loads(value):
    if not isinstance(value, str):
        return value

    try:
        return json.loads(value)
    except Exception:
        return value


def write_line(f, text=""):
    f.write(text + "\n")


def get_global_thread(case):
    return (
        case.get("team_states", {})
        .get("agent_states", {})
        .get("SelectorGroupChatManager", {})
        .get("message_thread", [])
    )


def normalize_tool_items(content):
    if not isinstance(content, list):
        return []

    normalized = []

    for item in content:
        if not isinstance(item, dict):
            normalized.append({"value": item})
            continue

        args_raw = item.get("arguments")
        args = safe_json_loads(args_raw)

        tool = {
            "name": item.get("name"),
            "id": item.get("id"),
            "call_id": item.get("call_id"),
        }

        if args_raw is not None:
            tool["arguments"] = args

        if item.get("content") is not None:
            tool["result"] = item.get("content")

        if item.get("is_error") is not None:
            tool["is_error"] = item.get("is_error")

        normalized.append(tool)

    return normalized


def simplify_event(event, index):
    event_type = event.get("type")
    content = event.get("content")

    simplified = {
        "index": index,
        "type": event_type,
        "source": event.get("source"),
    }

    if event.get("models_usage") is not None:
        simplified["models_usage"] = event.get("models_usage")

    if event_type in {"ToolCallRequestEvent", "ToolCallExecutionEvent"}:
        simplified["tools"] = normalize_tool_items(content)
    else:
        simplified["content"] = content

    return simplified


def build_readable_json(source_path, cases):
    output = {
        "format": "BAD-ACTS readable main-path log",
        "source_json": str(source_path),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "cases_count": len(cases),
        "cases": [],
    }

    for case_position, case in enumerate(cases, start=1):
        thread = get_global_thread(case)

        sent_messages = case.get("sent_messages", [])
        tickets = case.get("tickets", [])
        files = case.get("files", None)

        case_obj = {
            "case_position": case_position,
            "case_id": case.get("id"),
            "adversarial_agent": case.get("adversarial_agent"),
            "target_agent": case.get("target_agent"),
            "target_action": case.get("target_action"),
            "keywords": case.get("keywords"),
            "final_effects": {
                "sent_messages_count": len(sent_messages),
                "sent_messages": sent_messages,
                "tickets_count": len(tickets),
                "tickets": tickets,
            },
            "main_path": {
                "total_events": len(thread),
                "events": [
                    simplify_event(event, index)
                    for index, event in enumerate(thread, start=1)
                ],
            },
        }

        if files is not None:
            case_obj["final_effects"]["files_count"] = len(files)
            case_obj["final_effects"]["files"] = files

        output["cases"].append(case_obj)

    return output


def format_content_for_txt(f, content, indent=""):
    if isinstance(content, str):
        write_line(f, indent + content)

    elif isinstance(content, list):
        for item in content:
            if not isinstance(item, dict):
                write_line(f, indent + str(item))
                continue

            name = item.get("name")
            args = item.get("arguments")
            result = item.get("content")
            is_error = item.get("is_error")
            call_id = item.get("call_id") or item.get("id")

            if name:
                write_line(f, indent + f"tool/function: {name}")

            if call_id:
                write_line(f, indent + f"call_id: {call_id}")

            if args is not None:
                parsed_args = safe_json_loads(args)
                write_line(f, indent + "arguments:")
                if isinstance(parsed_args, (dict, list)):
                    formatted = json.dumps(parsed_args, ensure_ascii=False, indent=2)
                    for line in formatted.splitlines():
                        write_line(f, indent + line)
                else:
                    write_line(f, indent + str(parsed_args))

            if result is not None:
                write_line(f, indent + "result:")
                write_line(f, indent + str(result))

            if is_error is not None:
                write_line(f, indent + f"is_error: {is_error}")

    else:
        write_line(f, indent + str(content))


def write_case_txt(f, case, case_position):
    write_line(f, "=" * 120)
    write_line(f, f"CASE {case_position}")
    write_line(f, "=" * 120)

    write_line(f, f"case_id: {case.get('id')}")
    write_line(f, f"adversarial_agent: {case.get('adversarial_agent')}")
    write_line(f, f"target_agent: {case.get('target_agent')}")
    write_line(f, f"target_action: {case.get('target_action')}")
    write_line(f, f"keywords: {case.get('keywords')}")
    write_line(f)

    sent_messages = case.get("sent_messages", [])
    tickets = case.get("tickets", [])
    files = case.get("files", None)

    write_line(f, "FINAL EFFECTS")
    write_line(f, "-" * 120)

    write_line(f, f"sent_messages_count: {len(sent_messages)}")
    for i, msg in enumerate(sent_messages, start=1):
        write_line(f)
        write_line(f, f"Sent message {i}")

        if isinstance(msg, (list, tuple)) and len(msg) >= 2:
            address, message = msg[0], msg[1]
            write_line(f, f"TO: {address}")
            write_line(f, "MESSAGE:")
            write_line(f, str(message))
        else:
            write_line(f, str(msg))

    write_line(f)
    write_line(f, f"tickets_count: {len(tickets)}")
    for ticket in tickets:
        write_line(f, f"- {ticket}")

    if files is not None:
        write_line(f)
        write_line(f, f"files_count: {len(files)}")
        if isinstance(files, dict):
            for filename in files.keys():
                write_line(f, f"- {filename}")
        else:
            write_line(f, str(files))

    thread = get_global_thread(case)

    write_line(f)
    write_line(f, "GLOBAL TRAJECTORY")
    write_line(f, "-" * 120)
    write_line(f, f"total_events: {len(thread)}")
    write_line(f)

    for i, event in enumerate(thread, start=1):
        source = event.get("source", "UNKNOWN")
        typ = event.get("type", "UNKNOWN")
        content = event.get("content")

        write_line(f, "=" * 120)
        write_line(f, f"{i:02d}. {typ} | {source}")
        write_line(f, "-" * 120)
        format_content_for_txt(f, content)
        write_line(f)


def write_readable_txt(source_path, cases, output_path):
    with output_path.open("w", encoding="utf-8") as f:
        write_line(f, "Readable BAD-ACTS log")
        write_line(f, f"source_json: {source_path}")
        write_line(f, f"generated_at: {datetime.now().isoformat(timespec='seconds')}")
        write_line(f, f"cases_count: {len(cases)}")
        write_line(f)

        for case_position, case in enumerate(cases, start=1):
            write_case_txt(f, case, case_position)
            write_line(f)


def process_json_file(path):
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict):
        cases = [data]
    elif isinstance(data, list):
        cases = data
    else:
        print(f"Skipping {path}: unexpected format.")
        return None

    TXT_DIR.mkdir(parents=True, exist_ok=True)
    JSON_DIR.mkdir(parents=True, exist_ok=True)

    txt_output_path = TXT_DIR / f"{path.stem}.readable.txt"
    json_output_path = JSON_DIR / f"{path.stem}.readable.json"

    write_readable_txt(path, cases, txt_output_path)

    readable_json = build_readable_json(path, cases)
    with json_output_path.open("w", encoding="utf-8") as f:
        json.dump(readable_json, f, ensure_ascii=False, indent=2)

    return txt_output_path, json_output_path


def main():
    if not RESULTS_DIR.exists():
        raise SystemExit(f"results/ directory not found at {RESULTS_DIR}.")

    json_files = sorted(RESULTS_DIR.glob("*.json"))

    if not json_files:
        raise SystemExit("No JSON files found in results/.")

    print(f"Found {len(json_files)} JSON file(s) in results/.")

    created_txt = []
    created_json = []

    for path in json_files:
        try:
            result = process_json_file(path)
            if result is None:
                continue
            txt_path, json_path = result
            created_txt.append(txt_path)
            created_json.append(json_path)
            print(f"TXT created:  {txt_path}")
            print(f"JSON created: {json_path}")
        except Exception as e:
            print(f"Error processing {path}: {e}")

    print()
    print(f"Total readable TXT logs created: {len(created_txt)}")
    print(f"Total readable JSON logs created: {len(created_json)}")
    print()
    print("Directories:")
    print(f"- {TXT_DIR}")
    print(f"- {JSON_DIR}")


if __name__ == "__main__":
    main()
