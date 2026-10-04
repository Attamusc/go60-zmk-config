#!/usr/bin/env python3
"""Export the firmware keymap as a MoErgo Go60 Layout Editor JSON backup."""

import json
import re
import time
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KEYMAP = ROOT / "config/go60.keymap"
OUTPUT = ROOT / "config/go60-layout-editor.json"
SOURCE = KEYMAP.read_text()
LAYER_NAMES = ["base", "nav", "sym_right", "sym_left", "num", "util", "sys", "mouse"]
LAYER_IDS = {name.upper(): i for i, name in enumerate(LAYER_NAMES)}
BINDING = re.compile(r"&\w+|_HYPR\(\w+\)|_RAYCAST|_1PASS")


def block(start):
    opening = SOURCE.index("{", start)
    depth = 1
    for i in range(opening + 1, len(SOURCE)):
        depth += (SOURCE[i] == "{") - (SOURCE[i] == "}")
        if depth == 0:
            return SOURCE[start : i + 2]
    raise ValueError(f"Unclosed block at {start}")


def arg(expression):
    tokens = re.findall(r"[A-Za-z_]\w*|\d+|[()]", expression)
    if not tokens:
        raise ValueError(f"Empty argument: {expression!r}")

    def node(index):
        value = tokens[index]
        index += 1
        result = {"value": value}
        if index < len(tokens) and tokens[index] == "(":
            children = []
            index += 1
            while index < len(tokens) and tokens[index] != ")":
                child, index = node(index)
                children.append(child)
            if index == len(tokens):
                raise ValueError(f"Unclosed argument: {expression!r}")
            result["params"] = children
            index += 1
        return result, index

    result, end = node(0)
    if end != len(tokens):
        raise ValueError(f"Trailing argument: {expression!r}")
    return result


def binding(expression):
    if expression.startswith("_HYPR("):
        expression = "&kp LC(LS(LA(LG(" + expression[6:-1] + "))))"
    elif expression == "_RAYCAST":
        expression = "&kp LG(SPACE)"
    elif expression == "_1PASS":
        expression = "&kp LG(LS(SPACE))"
    name, _, arguments = expression.partition(" ")
    params = []
    for item in arguments.split():
        if item in LAYER_IDS:
            params.append({"value": LAYER_IDS[item]})
        elif item.isdecimal():
            params.append({"value": int(item)})
        else:
            params.append(arg(item))
    result = {"value": name}
    if params:
        result["params"] = params
    return result


def bindings(content):
    found = list(BINDING.finditer(content))
    result = []
    for i, match in enumerate(found):
        end = found[i + 1].start() if i + 1 < len(found) else len(content)
        result.append(binding(content[match.start() : end].strip()))
    return result


def layer(name):
    section = block(SOURCE.index(f"        {name} {{", SOURCE.index("    keymap {")))
    content = re.search(r"bindings = <(.*?)>;", section, re.S).group(1)
    result = bindings(content)
    if len(result) != 60:
        raise ValueError(f"{name} contains {len(result)} bindings, expected 60")
    return result


def combos():
    section = block(SOURCE.index("    combos {"))
    positions = {name: int(number) for name, number in re.findall(r"#define (GO60_\w+) (\d+)", SOURCE)}
    result = []
    for match in re.finditer(r"        (combo_\w+) \{", section):
        entry = block(SOURCE.index(match.group(0), SOURCE.index("    combos {")))
        keys = re.search(r"key-positions = <([^>]+)>;", entry).group(1).split()
        content = re.search(r"bindings = <(.*?)>;", entry, re.S).group(1)
        actions = bindings(content)
        if len(actions) != 1:
            raise ValueError(f"{match.group(1)} needs exactly one action")
        result.append({
            "name": match.group(1),
            "description": "",
            "binding": actions[0],
            "keyPositions": [positions[key] for key in keys],
            "timeoutMs": int(re.search(r"timeout-ms = <(\d+)>;", entry).group(1)),
            "slowRelease": False,
            "layers": [-1],
        })
    return result


def processors(section):
    contents = re.search(r"input-processors = (.*?);", section, re.S).group(1)
    result = []
    for entry in re.findall(r"<([^>]+)>", contents):
        code, *params = entry.split()
        result.append({"code": code, "params": [int(p) for p in params]})
    return result


def listener(label):
    section = block(SOURCE.index(f"&{label} {{"))
    head = section[: section.find("    layer_")]
    nodes = []
    for match in re.finditer(r"    (layer_\d+) \{", section):
        child = block(SOURCE.index(match.group(0), SOURCE.index(f"&{label} {{")))
        numbers = re.search(r"layers = <([^>]+)>;", child).group(1)
        nodes.append({
            "code": match.group(1),
            "layers": [int(n) for n in numbers.split()],
            "inputProcessors": processors(child),
        })
    return {"code": f"&{label}", "inputProcessors": processors(head), "nodes": nodes}


def custom_devicetree():
    settings = "\n\n".join(block(SOURCE.index(f"&{name} {{")) for name in ("mt", "lt", "sk"))
    # The editor generates the click mapper from inputListeners, as it does
    # for its factory layout. Keep only the unused custom quick-tap behavior.
    behaviors = block(SOURCE.index("    behaviors {", SOURCE.index("/ {")))
    quick_tap = re.search(r"#define QUICK_TAP_MS \d+", SOURCE).group(0)
    return '#include <dt-bindings/zmk/pointing.h>\n' + quick_tap + "\n\n" + settings + "\n\n/ {\n" + behaviors + "\n};"


def main():
    source_id = str(uuid.uuid5(uuid.NAMESPACE_URL, "go60-zmk-config:" + SOURCE))
    previous = json.loads(OUTPUT.read_text()) if OUTPUT.exists() else {}
    created_at = previous["date"] if previous.get("uuid") == source_id else int(time.time())
    payload = {
        "version": 1,
        "keyboard": "go60",
        "firmware_api_version": "1",
        "locale": "en-US",
        "uuid": source_id,
        "parent_uuid": "",
        "unlisted": True,
        "date": created_at,
        "creator": "attamusc",
        "title": "Go60 Toucan port (preview)",
        "notes": "Preview of config/go60.keymap. Git remains the firmware source of truth; do not build or flash this editor export without comparing its generated keymap against the repository.",
        "tags": [],
        "custom_defined_behaviors": "",
        "custom_devicetree": custom_devicetree(),
        "config_parameters": [],
        "layout_parameters": {},
        "layer_names": [n.upper() for n in LAYER_NAMES],
        "layers": [layer(n) for n in LAYER_NAMES],
        "macros": [],
        "inputListeners": [listener("cirque_rh_listener"), listener("cirque_lh_listener")],
        "holdTaps": [],
        "combos": combos(),
    }
    OUTPUT.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"Wrote {OUTPUT} ({len(payload['layers'])} layers, 60 positions each)")


if __name__ == "__main__":
    main()
