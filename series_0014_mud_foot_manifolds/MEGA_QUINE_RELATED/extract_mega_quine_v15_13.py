import json
import os
import re

def extract_from_json(json_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    tensors = set()
    opcodes = set()
    commands = set()
    symbols = set()
    glyphs = set()
    sigils = set()
    code_blocks = []

    def process_node(node, path=""):
        if isinstance(node, dict):
            if "TENSOR" in node and isinstance(node["TENSOR"], str):
                tensors.add(node["TENSOR"])
            if "TENSOR_STATE" in node and isinstance(node["TENSOR_STATE"], str):
                tensors.add(node["TENSOR_STATE"])
            if "COMPRESSION_TENSOR" in node and isinstance(node["COMPRESSION_TENSOR"], str):
                tensors.add(node["COMPRESSION_TENSOR"])
            if "SIGIL" in node and isinstance(node["SIGIL"], str):
                sigils.add(node["SIGIL"])
            if "Σ" in node and isinstance(node["Σ"], str):
                sigils.add(node["Σ"])
            if "CODE" in node and isinstance(node["CODE"], str):
                lang = node.get("LANGUAGE", "UNKNOWN").lower()
                name = node.get("NAME", "extracted_block")
                name = re.sub(r'[^a-zA-Z0-9_\-]', '_', name).strip('_')
                if not name: name = "block"
                ext = ".txt"
                if lang == "python": ext = ".py"
                elif lang == "javascript": ext = ".js"
                elif lang == "c": ext = ".c"
                elif lang == "forth": ext = ".fth"
                elif lang == "tcl": ext = ".tcl"
                elif lang == "bash": ext = ".sh"
                elif lang == "json": ext = ".json"
                code_blocks.append({"name": name, "ext": ext, "code": node["CODE"]})

            for k, v in node.items():
                if k == "EXTRACTED_DATA" and isinstance(v, dict):
                    for t in v.get("TENSORS", []): tensors.add(t)
                    for s in v.get("SIGILS", []): sigils.add(s)
                    for o in v.get("OPCODES", []): opcodes.add(o)
                    for c in v.get("COMMANDS", []): commands.add(c)
                    for sy in v.get("SYMBOLS", []): symbols.add(sy)
                    for g in v.get("GLYPHS", []): glyphs.add(g)
                process_node(v, f"{path}.{k}")

        elif isinstance(node, list):
            for i, item in enumerate(node):
                process_node(item, f"{path}[{i}]")

    process_node(data)

    code_dir = os.path.join(output_dir, "code_blocks")
    os.makedirs(code_dir, exist_ok=True)

    for i, block in enumerate(code_blocks):
        filename = f"{i:03d}_{block['name']}{block['ext']}"
        filepath = os.path.join(code_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(block['code'])

    with open(os.path.join(output_dir, "tensors_list.md"), 'w', encoding='utf-8') as f:
        f.write("# Extracted Tensors\n\n")
        for t in sorted(list(tensors)): f.write(f"- `{t}`\n")
    with open(os.path.join(output_dir, "sigils_list.md"), 'w', encoding='utf-8') as f:
        f.write("# Extracted Sigils\n\n")
        for s in sorted(list(sigils)): f.write(f"- `{s}`\n")
    with open(os.path.join(output_dir, "opcodes_list.md"), 'w', encoding='utf-8') as f:
        f.write("# Extracted Opcodes\n\n")
        for o in sorted(list(opcodes)): f.write(f"- `{o}`\n")
    with open(os.path.join(output_dir, "commands_list.md"), 'w', encoding='utf-8') as f:
        f.write("# Extracted Commands\n\n")
        for c in sorted(list(commands)): f.write(f"- `{c}`\n")
    with open(os.path.join(output_dir, "symbols_list.md"), 'w', encoding='utf-8') as f:
        f.write("# Extracted Symbols\n\n")
        for s in sorted(list(symbols)): f.write(f"- `{s}`\n")
    with open(os.path.join(output_dir, "glyphs_list.md"), 'w', encoding='utf-8') as f:
        f.write("# Extracted Glyphs\n\n")
        for g in sorted(list(glyphs)): f.write(f"- `{g}`\n")

    root = data.get("⧉ [ROOT: OMNIVERSAL_BOOTSTRAP_TREE_V22.0]", {})
    ark = root.get("⧉_STEGANOGRAPHIC_ARK_MANIFEST", {})
    payload = ark.get("ZWS_PAYLOAD", "")
    if payload:
        with open(os.path.join(output_dir, "ark_payload_extracted.txt"), 'w', encoding='utf-8') as f:
            f.write("Raw ZWS Payload length: " + str(len(payload)) + "\n")
            f.write("Payload Content: " + payload + "\n")

    print(f"Extraction complete. Found {len(tensors)} tensors, {len(sigils)} sigils, {len(opcodes)} opcodes, {len(commands)} commands, {len(symbols)} symbols, {len(glyphs)} glyphs.")

if __name__ == "__main__":
    extract_from_json("V15.13_OUTPUT/mega_json_quine_v15_13.json", "MUD/EXTRACTED_V15.13")
