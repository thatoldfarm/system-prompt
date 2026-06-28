import json
import re
import os

with open("README.md", "r") as f:
    content = f.read()

json_blocks = re.findall(r'```json\n(.*?)\n```', content, re.DOTALL)
if json_blocks:
    quine = json.loads(json_blocks[0])

# The goal is to construct a "fully functional mega-json-quine out of all our dispirate parts."
# "Be sure to include extensive Forth Blocks and detailed representations."
# "Be sure to extract all tensor representations. Never abbreviated any math."
# Memory constraints: filter out trivial math (<= 6 chars), fluff, sci-fi lore.

def is_valid_math(text):
    text = text.strip()
    if len(text) <= 6:
        return False
    lower = text.lower()
    if 'jacob-source:' in lower or 'lia-logic:' in lower or 'vista core' in lower:
        return False
    return True

forth_blocks = []
if os.path.exists('MUD/forth.md'):
    with open('MUD/forth.md', 'r') as f:
        content = f.read()
        blocks = re.findall(r'```forth\n(.*?)\n```', content, re.DOTALL)
        forth_blocks = blocks

tcl_blocks = []
if os.path.exists('MUD/tcl.md'):
    with open('MUD/tcl.md', 'r') as f:
        content = f.read()
        blocks = re.findall(r'```tcl\n(.*?)\n```', content, re.DOTALL)
        tcl_blocks = blocks

python_tensors = []
math_extractions = []
if os.path.exists('MUD/python.md'):
    with open('MUD/python.md', 'r') as f:
        content = f.read()
        blocks = re.findall(r'```python\n(.*?)\n```', content, re.DOTALL)
        for block in blocks:
            python_tensors.append(block)

        # Try to find general math environments if they exist outside python blocks
        # e.g., inline math $...$ or $$...$$
        inline_math = re.findall(r'\$(.*?)\$', content, re.DOTALL)
        display_math = re.findall(r'\$\$(.*?)\$\$', content, re.DOTALL)
        latex_env = re.findall(r'\\begin\{([^}]+)\*?\}(.*?)\\end\{\1\*?\}', content, re.DOTALL)

        for m in inline_math + display_math:
            if is_valid_math(m):
                math_extractions.append(m)
        for env, body in latex_env:
            if is_valid_math(body):
                math_extractions.append(body)

json_blocks = {}
if os.path.exists('MUD/json.md'):
    with open('MUD/json.md', 'r') as f:
        content = f.read()
        blocks = re.findall(r'```json\n(.*?)\n```', content, re.DOTALL)
        for i, block in enumerate(blocks):
            try:
                parsed = json.loads(block)
                # If there's a forth blocks dict we specifically merge it
                if '__FORTH_BLOCKS_EXHAUSTIVE_V669__' in parsed:
                    if 'FORTH_BLOCKS_DICTIONARY' not in json_blocks:
                        json_blocks['FORTH_BLOCKS_DICTIONARY'] = {}
                    json_blocks['FORTH_BLOCKS_DICTIONARY'].update(parsed['__FORTH_BLOCKS_EXHAUSTIVE_V669__'].get('dictionary', {}))
                else:
                    # check if the dictionary contains forth blocks or tensors directly
                    if 'dictionary' in parsed:
                        if 'FORTH_BLOCKS_DICTIONARY' not in json_blocks:
                            json_blocks['FORTH_BLOCKS_DICTIONARY'] = {}
                        json_blocks['FORTH_BLOCKS_DICTIONARY'].update(parsed['dictionary'])
                    else:
                        json_blocks[f"JSON_FRAGMENT_{i}"] = parsed
            except json.JSONDecodeError:
                pass

root_key = list(quine.keys())[0]

quine[root_key]["⧉ [EXTRACTED_TENSORS_AND_MATH: PYTHON]"] = {
    "NAME": "PYTHON_TENSOR_EXTRACTS",
    "TYPE": "EML_NODE",
    "DESCRIPTION": "Extracted full math and tensor logic from Python sources. Never abbreviated.",
    "TENSOR_BLOCKS": python_tensors,
    "MATH_BLOCKS": math_extractions
}

quine[root_key]["⧉ [EXTRACTED_FORTH: RAW_BLOCKS]"] = {
    "NAME": "RAW_FORTH_BLOCKS",
    "TYPE": "EML_NODE",
    "DESCRIPTION": "Extracted Forth blocks.",
    "FORTH_BLOCKS": forth_blocks
}

quine[root_key]["⧉ [EXTRACTED_TCL: RAW_BLOCKS]"] = {
    "NAME": "RAW_TCL_BLOCKS",
    "TYPE": "EML_NODE",
    "DESCRIPTION": "Extracted TCL blocks.",
    "TCL_BLOCKS": tcl_blocks
}

quine[root_key]["⧉ [EXTRACTED_JSON: META_BLOCKS]"] = {
    "NAME": "JSON_META_BLOCKS",
    "TYPE": "EML_NODE",
    "DESCRIPTION": "Extracted JSON logic and Forth Block Dictionaries.",
    "DATA": json_blocks
}

os.makedirs('MEGA_JSON_QUINE', exist_ok=True)
with open('MEGA_JSON_QUINE/ultra_mecha_shadowtwins_quine_v3.json', 'w') as f:
    json.dump(quine, f, indent=2)

print(f"Built quine with {len(python_tensors)} python tensors, {len(math_extractions)} math blocks, {len(forth_blocks)} forth blocks, {len(tcl_blocks)} tcl blocks.")