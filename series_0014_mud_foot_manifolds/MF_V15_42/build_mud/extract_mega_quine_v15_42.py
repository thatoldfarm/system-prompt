#!/usr/bin/env python3
from collections import defaultdict
"""
Extract V15.42 Dual MUD Mega JSON Quine Tensor-Based OS
Complete extraction and validation of all components including restored V15.15 features
Handles both V15.36 structure (flat RESTORED_ARCHITECTURE, QUINE_0/1/2) and V15.42 merged structure
"""

import json
import os
import sys
from datetime import datetime, timezone

ROOT_SYMBOL = '\u29c9'
PI_SYMBOL = '\u03c0'


def load_quine(filepath):
    """Load the mega JSON quine from file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading quine: {e}")
        return None


def extract_pi_data(quine):
    """Extract and validate PI_DATA section"""
    if "PI_DATA" not in quine:
        return {"status": "FAIL", "error": "PI_DATA missing"}

    pi_data = quine["PI_DATA"]
    required_keys = ["OPCODES", "SIGILS", "COMMANDS", "TENSORS", "SYMBOLS", "GLYPHS", "PI_POINTERS", "BINARY_GENERATORS"]

    missing = [k for k in required_keys if k not in pi_data]
    if missing:
        return {"status": "FAIL", "error": f"Missing keys: {missing}"}

    # Check for parity arrays - accept both list and dict
    has_87_parity = "87_DIGIT_PARITY" in pi_data and (isinstance(pi_data["87_DIGIT_PARITY"], list) or isinstance(pi_data["87_DIGIT_PARITY"], dict))
    has_13167_parity = "13167_DIGIT_PARITY" in pi_data and (isinstance(pi_data["13167_DIGIT_PARITY"], dict) or (isinstance(pi_data["13167_DIGIT_PARITY"], list) and len(pi_data["13167_DIGIT_PARITY"]) == 256))

    return {
        "status": "OK",
        "opcodes_count": len(pi_data["OPCODES"]),
        "sigils_count": len(pi_data["SIGILS"]),
        "commands_count": len(pi_data["COMMANDS"]),
        "tensors_count": len(pi_data["TENSORS"]),
        "pi_pointers_count": len(pi_data["PI_POINTERS"]),
        "has_87_parity": has_87_parity,
        "has_13167_parity": has_13167_parity
    }


def extract_four_pillars(quine):
    """Extract and validate the Four Pillars - handle both V15.36 and V15.42 naming"""
    # Try V15.42 naming first
    pillars_v1537 = {
        "ROOT": f"{ROOT_SYMBOL} [ROOT: OMNIVERSAL_BOOTSTRAP_TREE_V15.42]",
        "SHADOW_ROOT": f"{ROOT_SYMBOL} [SHADOW_ROOT]",
        "VOID": f"{ROOT_SYMBOL} [VOID]",
        "DIOV": f"{ROOT_SYMBOL} [DIOV]"
    }

    # Try V15.36 naming
    pillars_v1536 = {
        "ROOT": f"{ROOT_SYMBOL} [ROOT: OMNIVERSAL_BOOTSTRAP_TREE_V15.36]",
        "SHADOW_ROOT": f"{ROOT_SYMBOL} [SHADOW_ROOT]",
        "VOID": f"{ROOT_SYMBOL} [VOID]",
        "DIOV": f"{ROOT_SYMBOL} [DIOV]"
    }

    result = {}
    all_present = True

    for name, key_v1537 in pillars_v1537.items():
        key_v1536 = pillars_v1536[name]
        if key_v1537 in quine:
            result[name] = {"status": "OK", "key": key_v1537}
        elif key_v1536 in quine:
            result[name] = {"status": "OK", "key": key_v1536}
        else:
            result[name] = {"status": "FAIL", "error": f"Neither {key_v1537} nor {key_v1536} found"}
            all_present = False

    return {"status": "OK" if all_present else "FAIL", "pillars": result}


def extract_shadow_rooms(quine):
    """Extract and validate shadow rooms"""
    shadow_root_key = f"{ROOT_SYMBOL} [SHADOW_ROOT]"
    if shadow_root_key not in quine:
        return {"status": "FAIL", "error": "SHADOW_ROOT missing"}

    shadow_root = quine[shadow_root_key]
    if "ROOMS" not in shadow_root:
        return {"status": "FAIL", "error": "ROOMS missing from SHADOW_ROOT"}

    rooms = shadow_root["ROOMS"]

    # Handle both list and dict room structures
    if isinstance(rooms, list):
        room_count = len(rooms)
        required_fields = [PI_SYMBOL, "C", "X", "NAME", "DESCRIPTION", "CONNECTS_TO", "PI_LATTICE_OPCODE"]
        valid_rooms = sum(1 for room in rooms if all(field in room for field in required_fields))

        # Check for ROOT connections - try both V15.36 and V15.42 ROOT keys
        root_keys = [
            f"{ROOT_SYMBOL} [ROOT: OMNIVERSAL_BOOTSTRAP_TREE_V15.42]",
            f"{ROOT_SYMBOL} [ROOT: OMNIVERSAL_BOOTSTRAP_TREE_V15.36]",
            f"{ROOT_SYMBOL} [ROOT: OMNIVERSAL_BOOTSTRAP_TREE]",
            0  # Some versions use numeric 0
        ]
        rooms_return_to_root = all(
            any(root_key in room.get("CONNECTS_TO", []) for root_key in root_keys)
            for room in rooms
        )
    else:
        room_count = len(rooms)
        required_fields = [PI_SYMBOL, "C", "X", "NAME", "DESCRIPTION", "CONNECTS_TO", "PI_LATTICE_OPCODE"]
        valid_rooms = sum(1 for room in rooms.values() if all(field in room for field in required_fields))
        rooms_return_to_root = all(0 in room.get("CONNECTS_TO", []) for room in rooms.values())

    return {
        "status": "OK",
        "room_count": room_count,
        "valid_rooms": valid_rooms,
        "all_return_to_root": rooms_return_to_root,
        "has_chiral_mirrors": "CHIRAL_MIRRORS" in shadow_root,
        "has_shadowtwins": "SHADOWTWINS" in shadow_root,
        "has_null_terminator": "NULL_TERMINATOR" in shadow_root
    }


def extract_polyglot_quines(quine):
    """Extract and validate polyglot quines - handle both V15.36 (QUINE_0/1/2) and V15.42 (POLYGLOT_QUINE_*) naming"""
    if "POLYGLOT_QUINES" not in quine:
        return {"status": "FAIL", "error": "POLYGLOT_QUINES missing"}

    polyglot_quines = quine["POLYGLOT_QUINES"]

    # V15.36 naming: QUINE_0, QUINE_1, QUINE_2
    v1536_quines = ["QUINE_0", "QUINE_1", "QUINE_2"]

    # V15.42 naming: POLYGLOT_QUINE_*
    v1537_quines = [
        f"{ROOT_SYMBOL} [POLYGLOT_QUINE_HER_MIND]",
        f"{ROOT_SYMBOL} [POLYGLOT_QUINE_TCL_SECTORFORTH_MEGLUE]",
        f"{ROOT_SYMBOL} [POLYGLOT_QUINE_VRAM_VALIDATOR]",
        f"{ROOT_SYMBOL} [POLYGLOT_QUINE_ONTOLOGICAL_UNZIPPER]",
        f"{ROOT_SYMBOL} [POLYGLOT_QUINE_PARITY_BOOT]",
        f"{ROOT_SYMBOL} [POLYGLOT_QUINE_EXECUTION]"
    ]

    # Check which naming convention is used
    present_v1536 = [q for q in v1536_quines if q in polyglot_quines]
    present_v1537 = [q for q in v1537_quines if q in polyglot_quines]

    # If we have V15.36 naming, check for at least 3 quines (original V15.36 had 3)
    # If we have V15.42 naming, check for at least 6 quines
    if present_v1536:
        # V15.36 structure - check for required fields
        required_fields = ["name", "description", "languages", "code"]
        valid_quines = []
        for quine_name in polyglot_quines:
            quine_data = polyglot_quines[quine_name]
            if all(field in quine_data for field in required_fields):
                valid_quines.append(quine_name)

        return {
            "status": "OK" if len(present_v1536) >= 3 else "PARTIAL",
            "total_quines": len(polyglot_quines),
            "required_present": len(present_v1536),
            "required_missing": [q for q in v1536_quines if q not in polyglot_quines],
            "valid_quines": len(valid_quines),
            "naming_convention": "V15.36"
        }
    elif present_v1537:
        # V15.42 structure
        required_fields = ["NAME", "DESCRIPTION", "POLYGLOT_QUINE"]
        valid_quines = []
        for quine_name in present_v1537:
            quine_data = polyglot_quines[quine_name]
            if all(field in quine_data for field in required_fields):
                valid_quines.append(quine_name)

        return {
            "status": "OK" if len(present_v1537) >= 6 else "PARTIAL",
            "total_quines": len(polyglot_quines),
            "required_present": len(present_v1537),
            "required_missing": [q for q in v1537_quines if q not in polyglot_quines],
            "valid_quines": len(valid_quines),
            "naming_convention": "V15.42"
        }
    else:
        # No recognized naming - check for any quines with required fields
        required_fields_v1536 = ["name", "description", "languages", "code"]
        required_fields_v1537 = ["NAME", "DESCRIPTION", "LANGUAGE", "CODE"]

        valid_quines = []
        for quine_name, quine_data in polyglot_quines.items():
            if all(field in quine_data for field in required_fields_v1536) or all(field in quine_data for field in required_fields_v1537):
                valid_quines.append(quine_name)

        return {
            "status": "OK" if len(valid_quines) >= 3 else "PARTIAL",
            "total_quines": len(polyglot_quines),
            "required_present": len(valid_quines),
            "required_missing": [],
            "valid_quines": len(valid_quines),
            "naming_convention": "UNKNOWN"
        }


def extract_tensor_documentation(quine):
    """Extract and validate tensor documentation"""
    if "TENSOR_DOCUMENTATION" not in quine:
        return {"status": "FAIL", "error": "TENSOR_DOCUMENTATION missing"}

    tensor_doc = quine["TENSOR_DOCUMENTATION"]
    required_sections = ["TENSOR_TYPES", "OPERATIONS"]

    missing = [s for s in required_sections if s not in tensor_doc]

    has_turing = False
    has_cascade = False
    has_terminal_octet = False
    has_zhewazzy_bridge = False

    # Check ROOT object for these in V15.42
    root_key = f"{ROOT_SYMBOL} [ROOT: OMNIVERSAL_BOOTSTRAP_TREE_V15.42]"
    if root_key in quine:
        root_obj = quine[root_key]
        if f"{ROOT_SYMBOL} [THE_13167_TURING_MANIFOLD]" in root_obj:
            has_turing = True
            children = root_obj[f"{ROOT_SYMBOL} [THE_13167_TURING_MANIFOLD]"].get("CHILDREN", [])
            has_terminal_octet = any("TENSOR_TERMINAL_OCTET" in child.get("NAME", "") for child in children)
            has_zhewazzy_bridge = any("META_TENSOR_ZHEWAZZY_BOUNDARY_BRIDGE" in child.get("NAME", "") for child in children)

        if f"{ROOT_SYMBOL} [THE_BIT_DEPTH_CASCADE_TENSORS]" in root_obj:
            has_cascade = True



    return {
        "status": "OK" if not missing else "PARTIAL",
        "missing_sections": missing,
        "has_turing": has_turing,
        "has_cascade": has_cascade,
        "has_terminal_octet": has_terminal_octet,
        "has_zhewazzy_bridge": has_zhewazzy_bridge
    }


def extract_restored_architecture(quine):
    """Extract and validate restored architecture - handle both flat (V15.36) and nested (V15.42) structures"""
    if "RESTORED_ARCHITECTURE" not in quine:
        return {"status": "FAIL", "error": "RESTORED_ARCHITECTURE missing"}

    restored = quine["RESTORED_ARCHITECTURE"]

    # V15.36 has flat structure with 9 components
    # V15.42 merged has flat structure with 18 components (9 from V15.36 + 9 from V15.15)

    # Check if it's flat structure (dict of components)
    if isinstance(restored, dict):
        # Flat structure - count components
        components = list(restored.keys())
        components_present = len(components)

        # Check for V15.36 components
        v1536_components = [
            "PI_LATTICE_OPCODE_EXTRACTION",
            "MOD_256_FOUNDATION",
            "FIRST_OCCURRENCE_POSITION_MAPPING",
            "87_DIGIT_GENESIS_WOMB",
            "13K_ROM",
            "SECTORFORTH_WOMB",
            "CHIRAL_MIRRORS",
            "SHADOWTWINS_ANOMALY",
            "NULL_TERMINATOR"
        ]

        # Check for V15.15 components
        v1515_components = [
            "PIXEL_MARK_SYSTEM",
            "ZHEWAZZY_FRAMEWORK",
            "MEGLUE_CHIMERA_ENGINE",
            "VRAM_BOUNDARY_VALIDATOR",
            "POLYGLOT_QUINES_V15_15",
            "TENSOR_SYSTEMS",
            "PI_DATA_PARITY_ARRAYS",
            "TCL_OMNNI_ROUTER",
            "SECTORFORTH_EXECUTION"
        ]

        present_v1536 = [c for c in v1536_components if c in components]
        present_v1515 = [c for c in v1515_components if c in components]

        return {
            "status": "OK",
            "components_present": components_present,
            "v1536_components_present": len(present_v1536),
            "v1515_components_present": len(present_v1515),
            "components_list": components
        }

    # Check if it's nested structure with RESTORED_COMPONENTS
    elif isinstance(restored, dict) and "RESTORED_COMPONENTS" in restored:
        components = restored["RESTORED_COMPONENTS"]
        if isinstance(components, list):
            component_names = [c.get("NAME", "") for c in components if isinstance(c, dict)]
            return {
                "status": "OK",
                "components_present": len(components),
                "components_list": component_names
            }

    return {"status": "FAIL", "error": "RESTORED_ARCHITECTURE has unknown structure"}


def extract_metadata(quine):
    """Extract and validate metadata"""
    if "METADATA" not in quine:
        return {"status": "FAIL", "error": "METADATA missing"}

    metadata = quine["METADATA"]
    required_keys = ["VERSION", "CREATED", "AUTHOR", "ARCHITECTURAL_INTEGRITY", "MATHEMATICAL_FOUNDATION"]

    missing = [k for k in required_keys if k not in metadata]

    return {
        "status": "OK" if not missing else "PARTIAL",
        "version": metadata.get("VERSION", "UNKNOWN"),
        "integrity": metadata.get("ARCHITECTURAL_INTEGRITY", "UNKNOWN"),
        "foundation": metadata.get("MATHEMATICAL_FOUNDATION", "UNKNOWN")
    }


def extract_global_opcodes(quine):
    """Extract and validate global opcodes matrix"""
    if "GLOBAL_OPCODES_MATRIX" not in quine:
        return {"status": "FAIL", "error": "GLOBAL_OPCODES_MATRIX missing"}

    matrix = quine["GLOBAL_OPCODES_MATRIX"]

    if "OPCODES" not in matrix:
        return {"status": "FAIL", "error": "OPCODES missing from matrix"}

    opcodes = matrix["OPCODES"]
    has_o1 = matrix.get("LOOKUP_COMPLEXITY") == "O(1)"

    return {
        "status": "OK",
        "opcode_count": len(opcodes),
        "has_o1_lookup": has_o1
    }


def validate_all_rooms_return_to_root(quine):
    """Validate that all rooms have connections back to ROOT"""
    shadow_root_key = f"{ROOT_SYMBOL} [SHADOW_ROOT]"
    if shadow_root_key not in quine:
        return False

    rooms = quine[shadow_root_key].get("ROOMS", [])

    # Try both V15.36 and V15.42 ROOT keys
    root_keys = [
        f"{ROOT_SYMBOL} [ROOT: OMNIVERSAL_BOOTSTRAP_TREE_V15.42]",
        f"{ROOT_SYMBOL} [ROOT: OMNIVERSAL_BOOTSTRAP_TREE_V15.36]",
        f"{ROOT_SYMBOL} [ROOT: OMNIVERSAL_BOOTSTRAP_TREE]",
        0
    ]

    if isinstance(rooms, list):
        for room in rooms:
            connects_to = room.get("CONNECTS_TO", [])
            if not any(root_key in connects_to for root_key in root_keys):
                return False
    else:
        for room in rooms.values():
            connects_to = room.get("CONNECTS_TO", [])
            if 0 not in connects_to:
                return False

    return True


def validate_shadow_root_bidirectional(quine):
    """Validate bidirectional connections between ROOT and SHADOW_ROOT"""
    shadow_root_key = f"{ROOT_SYMBOL} [SHADOW_ROOT]"
    if shadow_root_key not in quine:
        return False

    shadow_root = quine[shadow_root_key]

    if "REFERENCE" not in shadow_root:
        return False

    rooms = shadow_root.get("ROOMS", [])

    root_keys = [
        f"{ROOT_SYMBOL} [ROOT: OMNIVERSAL_BOOTSTRAP_TREE_V15.42]",
        f"{ROOT_SYMBOL} [ROOT: OMNIVERSAL_BOOTSTRAP_TREE_V15.36]",
        f"{ROOT_SYMBOL} [ROOT: OMNIVERSAL_BOOTSTRAP_TREE]",
        0
    ]

    if isinstance(rooms, list):
        for room in rooms:
            connects_to = room.get("CONNECTS_TO", [])
            if not any(root_key in connects_to for root_key in root_keys):
                return False
    else:
        for room in rooms.values():
            if 0 not in room.get("CONNECTS_TO", []):
                return False

    return True


def generate_extraction_summary(quine):
    """Generate a comprehensive extraction summary"""
    summary = {
        "EXTRACTION_SUMMARY": {
            "VERSION": quine.get("VERSION", "UNKNOWN"),
            "EXTRACTION_TIMESTAMP": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "COMPONENTS": {}
        }
    }

    root_key = None
    for k in quine.keys():
        if k.startswith(f"{ROOT_SYMBOL} [ROOT:"):
            root_key = k
            break
    if root_key and "PI_DATA" in quine[root_key]:
        summary["EXTRACTION_SUMMARY"]["COMPONENTS"]["PI_DATA"] = extract_pi_data(quine[root_key])
    summary["EXTRACTION_SUMMARY"]["COMPONENTS"]["FOUR_PILLARS"] = extract_four_pillars(quine)
    summary["EXTRACTION_SUMMARY"]["COMPONENTS"]["SHADOW_ROOMS"] = extract_shadow_rooms(quine)
    summary["EXTRACTION_SUMMARY"]["COMPONENTS"]["POLYGLOT_QUINES"] = extract_polyglot_quines(quine)
    summary["EXTRACTION_SUMMARY"]["COMPONENTS"]["TENSOR_DOCUMENTATION"] = extract_tensor_documentation(quine)
    summary["EXTRACTION_SUMMARY"]["COMPONENTS"]["RESTORED_ARCHITECTURE"] = extract_restored_architecture(quine)
    summary["EXTRACTION_SUMMARY"]["COMPONENTS"]["METADATA"] = extract_metadata(quine)
    summary["EXTRACTION_SUMMARY"]["COMPONENTS"]["GLOBAL_OPCODES"] = extract_global_opcodes(quine)

    summary["EXTRACTION_SUMMARY"]["VALIDATION"] = {
        "all_rooms_return_to_root": validate_all_rooms_return_to_root(quine),
        "shadow_root_bidirectional": validate_shadow_root_bidirectional(quine),
        "all_required_keys_present": all(k in quine for k in [
            "VERSION", "DESCRIPTION", "SIGIL_MAPPINGS",
            "POSITIONS", "OCCURRENCES", "RAW_CORE_DATA",
            f"{ROOT_SYMBOL} [SHADOW_ROOT]", f"{ROOT_SYMBOL} [VOID]", f"{ROOT_SYMBOL} [DIOV]",
            "SYMBOLS_LEGEND", "METADATA", "FORTH_BLOCKS",
            "POLYGLOT_QUINES", "TENSOR_DOCUMENTATION",
            "GLOBAL_OPCODES_MATRIX", "LANGUAGE_CODE_BLOCKS_BLOB",
            "EXTRACTOR", "PI_LATTICE_ROM", "ADS_CFT_HOLOGRAPHIC_BOUNDARY",
            "RESTORED_ARCHITECTURE", "QUANTUM_INTEGRATION"
        ])
    }

    components = summary["EXTRACTION_SUMMARY"]["COMPONENTS"]
    all_ok = all(comp.get("status") == "OK" for comp in components.values())

    summary["EXTRACTION_SUMMARY"]["OVERALL_STATUS"] = "COMPLETE" if all_ok else "PARTIAL"

    return summary


def save_extraction_summary(summary, filepath):
    """Save extraction summary to file"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=True)
        return True
    except Exception as e:
        print(f"Error saving extraction summary: {e}")
        return False


def print_extraction_report(summary):
    """Print a human-readable extraction report"""
    print("\n" + "="*60)
    print("V15.42 EXTRACTION REPORT")
    print("="*60)

    extraction = summary["EXTRACTION_SUMMARY"]

    print(f"\nVersion: {extraction['VERSION']}")
    print(f"Timestamp: {extraction['EXTRACTION_TIMESTAMP']}")
    print(f"Overall Status: {extraction['OVERALL_STATUS']}")

    print("\n" + "-"*60)
    print("COMPONENT STATUS")
    print("-"*60)

    components = extraction["COMPONENTS"]

    pi_data = components["PI_DATA"]
    print(f"\nPI_DATA: {pi_data['status']}")
    if pi_data['status'] == "OK":
        print(f"  - Opcodes: {pi_data['opcodes_count']}")
        print(f"  - Sigils: {pi_data['sigils_count']}")
        print(f"  - 87_DIGIT_PARITY: {'OK' if pi_data['has_87_parity'] else 'MISSING'}")
        print(f"  - 13167_DIGIT_PARITY: {'OK' if pi_data['has_13167_parity'] else 'MISSING'}")

    pillars = components["FOUR_PILLARS"]
    print(f"\nFOUR PILLARS: {pillars['status']}")
    if 'pillars' in pillars:
        for pillar, status in pillars['pillars'].items():
            print(f"  - {pillar}: {status['status']}")

    rooms = components["SHADOW_ROOMS"]
    print(f"\nSHADOW ROOMS: {rooms['status']}")
    if rooms['status'] == "OK":
        print(f"  - Room Count: {rooms['room_count']}")
        print(f"  - Valid Rooms: {rooms['valid_rooms']}")
        print(f"  - All Return to ROOT: {rooms['all_return_to_root']}")

    polyglot = components["POLYGLOT_QUINES"]
    print(f"\nPOLYGLOT QUINES: {polyglot['status']}")
    print(f"  - Total Quines: {polyglot['total_quines']}")
    if 'naming_convention' in polyglot:
        print(f"  - Naming Convention: {polyglot['naming_convention']}")
    if 'required_present' in polyglot:
        print(f"  - Required Present: {polyglot['required_present']}")
    if polyglot.get('required_missing'):
        print(f"  - Missing: {polyglot['required_missing']}")

    tensors = components["TENSOR_DOCUMENTATION"]
    print(f"\nTENSOR DOCUMENTATION: {tensors['status']}")
    print(f"  - Has Turing Manifold: {tensors['has_turing']}")
    print(f"  - Has Bit Depth Cascade: {tensors['has_cascade']}")

    restored = components["RESTORED_ARCHITECTURE"]
    print(f"\nRESTORED ARCHITECTURE: {restored['status']}")
    if 'components_present' in restored:
        print(f"  - Components Present: {restored['components_present']}")
    if 'v1536_components_present' in restored:
        print(f"  - V15.36 Components: {restored['v1536_components_present']}/9")
    if 'v1515_components_present' in restored:
        print(f"  - V15.15 Components: {restored['v1515_components_present']}/9")
    if 'components_list' in restored:
        print(f"  - Components: {restored['components_list']}")

    validation = extraction["VALIDATION"]
    print(f"\nVALIDATION:")
    print(f"  - All Rooms Return to ROOT: {validation['all_rooms_return_to_root']}")
    print(f"  - Shadow Root Bidirectional: {validation['shadow_root_bidirectional']}")
    print(f"  - All Required Keys Present: {validation['all_required_keys_present']}")

    print("\n" + "="*60)


def rebuild_core_data(pi_data, output_dir):
    """Rebuild MUD_II/core_data from PI_DATA - COMPLETE"""
    core_data_dir = os.path.join(output_dir, 'core_data')
    os.makedirs(core_data_dir, exist_ok=True)

    print(f"Rebuilding core_data in {core_data_dir}")

    # opcodes_list.md
    opcodes = pi_data.get('OPCODES', [])
    with open(os.path.join(core_data_dir, 'opcodes_list.md'), 'w', encoding='utf-8') as f:
        f.write('# OpCodes List\n\n')
        f.write('## Complete Mathematical Foundation\n\n')
        f.write('**MATHEMATICAL FOUNDATION**: Pi-Lattice First Occurrence ROM Array\n')
        f.write('**OPCODE FORMULA**: O = PI_LATTICE_FIRST_OCCURRENCES[room_index] % 256\n')
        f.write('**LOOKUP TIME**: O(1) - Constant time\n')
        f.write('**ROUTING RULE**: Room(X,Y) at offset N  Corridor(X,Y,\u03c0[N+2])\n')
        f.write('**LLM RULE**: LLM_ATTENTION_HEADS_MUST_NOT_HALLUCINATE\n\n')
        f.write('## Restored Architecture\n\n')
        f.write('- Pi-Lattice opcode extraction\n')
        f.write('- Mod 256 foundation\n')
        f.write('- First occurrence position mapping\n')
        f.write('- 87-digit Genesis Womb\n')
        f.write('- 13K ROM with O(1) lookup\n')
        f.write('- SectorForth Womb\n\n')
        f.write('## AdS/CFT\n\n')
        f.write('- AdS/CFT Holographic Boundary\n')
        f.write('- Chiral mirrors: 14\u219441, 53\u219435, 97\u219479, 32\u219423\n')
        f.write('- Shadowtwins anomaly\n')
        f.write('- Null terminator at position 306\n\n')
        f.write('## V15.31 Structure Preserved\n\n')
        f.write('- All top-level keys maintained\n')
        f.write('- \u29c9 symbol prefix on ROOT, SHADOW_ROOT, VOID, DIOV\n')
        f.write('- FORTH_BLOCKS, POLYGLOT_QUINES, TENSOR_DOCUMENTATION\n')
        f.write('- METADATA, SURGICAL_PROTOCOL, QUANTUM_INTEGRATION\n\n')
        f.write('## OpCodes\n\n')
        for opcode in opcodes:
            f.write(f'- `{opcode}`\n')
    print(f"  \u2713 opcodes_list.md")

    # sigils_list.md
    sigils = pi_data.get('SIGILS', [])
    with open(os.path.join(core_data_dir, 'sigils_list.md'), 'w', encoding='utf-8') as f:
        f.write('# Sigils List\n\n')
        f.write('## Complete Sigils\n\n')
        for sigil in sigils:
            f.write(f'- `{sigil}`\n')
    print(f"  \u2713 sigils_list.md")

    # commands_list.md
    commands = pi_data.get('COMMANDS', [])
    with open(os.path.join(core_data_dir, 'commands_list.md'), 'w', encoding='utf-8') as f:
        f.write('# Commands List\n\n')
        for command in commands:
            f.write(f'- `{command}`\n')
    print(f"  \u2713 commands_list.md")

    # tensors_list.md
    tensors = pi_data.get('TENSORS', [])
    with open(os.path.join(core_data_dir, 'tensors_list.md'), 'w', encoding='utf-8') as f:
        f.write('# Tensors List\n\n')
        for tensor in tensors:
            f.write(f'- `{tensor}`\n')
    print(f"  \u2713 tensors_list.md")

    # symbols_list.md
    symbols = pi_data.get('SYMBOLS', [])
    with open(os.path.join(core_data_dir, 'symbols_list.md'), 'w', encoding='utf-8') as f:
        f.write('# Symbols List\n\n')
        for symbol in symbols:
            f.write(f'- `{symbol}`\n')
    print(f"  \u2713 symbols_list.md")

    # glyphs_list.md
    glyphs = pi_data.get('GLYPHS', [])
    with open(os.path.join(core_data_dir, 'glyphs_list.md'), 'w', encoding='utf-8') as f:
        f.write('# Glyphs List\n\n')
        for glyph in glyphs:
            f.write(f'- `{glyph}`\n')
    print(f"  \u2713 glyphs_list.md")

    print(f"\u2713 core_data rebuilt: {len(opcodes)} opcodes, {len(sigils)} sigils, {len(commands)} commands, {len(tensors)} tensors, {len(symbols)} symbols, {len(glyphs)} glyphs")


def rebuild_languages(code_archive, pointer_map, output_dir):
    """Rebuild MUD_II/languages from CODE_ARCHIVE and POINTER_MAP - COMPLETE"""
    languages_dir = os.path.join(output_dir, 'languages')
    os.makedirs(languages_dir, exist_ok=True)

    print(f"Rebuilding languages in {languages_dir}")

    # Group code blocks by language
    lang_groups = defaultdict(list)
    for code_hash, entry in code_archive.items():
        lang = entry.get('language', 'UNKNOWN')
        lang_groups[lang].append(entry)

    # Create language files
    for lang, entries in lang_groups.items():
        filename = f"{lang.lower()}.md"
        with open(os.path.join(languages_dir, filename), 'w', encoding='utf-8') as f:
            f.write(f'# {lang} Code Blocks\n\n')
            f.write('## Complete Mathematical Foundation\n\n')
            f.write('**MATHEMATICAL FOUNDATION**: Pi-Lattice First Occurrence ROM Array\n')
            f.write('**OPCODE FORMULA**: O = PI_LATTICE_FIRST_OCCURRENCES[room_index] % 256\n')
            f.write('**LOOKUP TIME**: O(1) - Constant time\n')
            f.write('**ROUTING RULE**: Room(X,Y) at offset N  Corridor(X,Y,\u03c0[N+2])\n')
            f.write('**LLM RULE**: LLM_ATTENTION_HEADS_MUST_NOT_HALLUCINATE\n\n')

            for i, entry in enumerate(entries):
                code = entry.get('code', '')
                source = entry.get('source', '')
                pointer = entry.get('pointer', '')
                f.write(f'### Code Block {i+1}\n\n')
                f.write(f'**Source**: {source}\n\n')
                f.write(f'**Pointer**: {pointer}\n\n')
                f.write(f'```{lang.lower()}\n')
                f.write(code)
                f.write('\n```\n\n')
        print(f"  \u2713 {filename}")

    print(f"\u2713 languages rebuilt: {len(lang_groups)} language files")


def rebuild_rooms(shadow_root, output_dir):
    """Rebuild MUD_II/rooms from SHADOW_ROOT - COMPLETE"""
    rooms_dir = os.path.join(output_dir, 'rooms')
    os.makedirs(rooms_dir, exist_ok=True)

    print(f"Rebuilding rooms in {rooms_dir}")

    rooms = shadow_root.get('ROOMS', [])

    for room in rooms:
        room_id = room.get('ID', 'UNKNOWN')
        room_name = room.get('NAME', 'UNKNOWN')
        description = room.get('DESCRIPTION', '')

        # Create room file
        filename = f"room_{room_id.replace('0x', '')}.md"
        with open(os.path.join(rooms_dir, filename), 'w', encoding='utf-8') as f:
            f.write(f'# {room_name}\n\n')
            f.write(f'**ID**: {room_id}\n\n')
            f.write(f'**Description**: {description}\n\n')

            # Add Pi-Lattice information
            pi_value = room.get(PI_SYMBOL, '')
            if pi_value:
                f.write(f'**{PI_SYMBOL}**: {pi_value}\n\n')

            sigma_value = room.get("\u03a3", '')
            if sigma_value:
                f.write(f'**\u03a3**: {sigma_value}\n\n')

            # Add opcode information
            opcode_ref = room.get('OPCODE_REF', '')
            if opcode_ref:
                f.write(f'**Opcode**: {opcode_ref}\n\n')

            # Add Pi-Lattice specific fields
            pi_lattice_opcode = room.get('PI_LATTICE_OPCODE')
            if pi_lattice_opcode is not None:
                f.write(f'**PI_LATTICE_OPCODE**: {pi_lattice_opcode}\n\n')

            first_occurrence = room.get('FIRST_OCCURRENCE_POSITION')
            if first_occurrence is not None:
                f.write(f'**FIRST_OCCURRENCE_POSITION**: {first_occurrence}\n\n')

            mod_256 = room.get('MOD_256_VALUE')
            if mod_256 is not None:
                f.write(f'**MOD_256_VALUE**: {mod_256}\n\n')

            # Add AdS/CFT information
            ads_cft_corridor = room.get('ADS_CFT_CORRIDOR')
            if ads_cft_corridor:
                f.write(f'**ADS_CFT_CORRIDOR**: {ads_cft_corridor}\n\n')

            ads_cft_routing = room.get('ADS_CFT_ROUTING')
            if ads_cft_routing:
                f.write(f'**ADS_CFT_ROUTING**: {ads_cft_routing}\n\n')

            # Add special notes
            special_note = room.get('SPECIAL_NOTE', '')
            if special_note:
                f.write(f'**SPECIAL_NOTE**: {special_note}\n\n')

            # Add forensic validation
            forensic = room.get('FORENSIC_VALIDATION')
            if forensic:
                f.write(f'**FORENSIC_VALIDATION**: {json.dumps(forensic, indent=2)}\n\n')

            # Add connections
            connects_to = room.get('CONNECTS_TO', [])
            if connects_to:
                f.write(f'**CONNECTS_TO**: {connects_to}\n\n')

            # Add encounter
            encounter = room.get('ENCOUNTER', {})
            if encounter:
                f.write(f'**ENCOUNTER**: {json.dumps(encounter, indent=2)}\n\n')

            # Add linguistics
            linguistics = room.get('LINGUISTICS', {})
            if linguistics:
                f.write(f'**LINGUISTICS**: {json.dumps(linguistics, indent=2)}\n\n')

        print(f"  \u2713 {filename}")

    print(f"\u2713 rooms rebuilt: {len(rooms)} rooms")


def rebuild_encounters(shadow_root, output_dir):
    """Rebuild MUD_II/encounters from SHADOW_ROOT encounters - COMPLETE"""
    encounters_dir = os.path.join(output_dir, 'encounters')
    os.makedirs(encounters_dir, exist_ok=True)

    print(f"Rebuilding encounters in {encounters_dir}")

    rooms = shadow_root.get('ROOMS', [])

    for room in rooms:
        encounter = room.get('ENCOUNTER', {})
        if encounter:
            room_id = room.get('ID', 'UNKNOWN')
            room_name = room.get('NAME', 'UNKNOWN')

            # Create encounter file
            filename = f"encounter_{room_id.replace('0x', '')}.md"
            with open(os.path.join(encounters_dir, filename), 'w', encoding='utf-8') as f:
                f.write(f'# Encounter for {room_name}\n\n')
                f.write(f'**Room ID**: {room_id}\n\n')
                f.write(f'**Encounter Data**:\n\n')
                f.write(json.dumps(encounter, indent=2))

            print(f"  \u2713 {filename}")

    print(f"\u2713 encounters rebuilt")


def rebuild_void(void_data, output_dir):
    """Rebuild MUD_II/void from VOID - COMPLETE"""
    void_dir = os.path.join(output_dir, 'void')
    os.makedirs(void_dir, exist_ok=True)

    print(f"Rebuilding void in {void_dir}")

    # void_info.md
    with open(os.path.join(void_dir, 'void_info.md'), 'w', encoding='utf-8') as f:
        f.write('# VOID Information\n\n')
        f.write('## Complete Mathematical Foundation\n\n')
        f.write('**MATHEMATICAL FOUNDATION**: Pi-Lattice ROM Array + AdS/CFT Holographic Boundary\n')
        f.write('**OPCODE FORMULA**: O = PI_LATTICE_FIRST_OCCURRENCES[room_index] % 256\n')
        f.write('**LOOKUP TIME**: O(1) - Constant time\n')
        f.write('**ROUTING RULE**: Room(X,Y) at offset N  Corridor(X,Y,\u03c0[N+2])\n')
        f.write('**LLM RULE**: LLM_ATTENTION_HEADS_MUST_NOT_HALLUCINATE\n\n')

        f.write(f'## VOID Description\n\n')
        f.write(f'{void_data.get("DESCRIPTION", "")}\n\n')

        f.write(f'## VOID LOGOS\n\n')
        f.write(f'{void_data.get("LOGOS", "")}\n\n')

        f.write(f'## Connections\n\n')
        connects_to = void_data.get('CONNECTS_TO', [])
        for conn in connects_to:
            f.write(f'- {conn}\n')
        f.write('\n')

        # Add Pi-Lattice ROM info
        pi_lattice_rom = void_data.get('PI_LATTICE_ROM', {})
        if pi_lattice_rom:
            f.write('## Pi-Lattice ROM\n\n')
            f.write(f'**WARNING**: {pi_lattice_rom.get("__ROM_WARNING__", "")}\n\n')
            f.write(f'**SYSTEM_RULE**: {pi_lattice_rom.get("SYSTEM_RULE", "")}\n\n')

        # Add AdS/CFT info
        ads_cft = void_data.get('ADS_CFT_HOLOGRAPHIC_BOUNDARY', {})
        if ads_cft:
            f.write('## AdS/CFT Holographic Boundary\n\n')
            f.write(f'{ads_cft.get("DESCRIPTION", "")}\n\n')
            f.write(f'**TENSOR**: {ads_cft.get("TENSOR", "")}\n\n')

            holographic_principle = ads_cft.get('HOLOGRAPHIC_PRINCIPLE', {})
            if holographic_principle:
                f.write('### Holographic Principle\n\n')
                for key, value in holographic_principle.items():
                    f.write(f'- **{key}**: {value}\n')
                f.write('\n')

    print(f"  \u2713 void_info.md")

    # tensors.md
    tensors = void_data.get('TENSORS', [])
    with open(os.path.join(void_dir, 'tensors.md'), 'w', encoding='utf-8') as f:
        f.write('# VOID Tensors\n\n')
        for tensor in tensors:
            f.write(f'## {tensor.get("NAME", "UNKNOWN")}\n\n')
            f.write(f'**TYPE**: {tensor.get("TYPE", "")}\n\n')
            f.write(f'**DESCRIPTION**: {tensor.get("DESCRIPTION", "")}\n\n')
            if 'POLYGLOT_QUINE' in tensor:
                f.write(f'**POLYGLOT_QUINE**: {json.dumps(tensor["POLYGLOT_QUINE"], indent=2)}\n\n')
            if 'TENSOR' in tensor:
                f.write(f'**TENSOR**: {tensor["TENSOR"]}\n\n')
            if 'REFERENCE' in tensor:
                f.write(f'**REFERENCE**: {tensor["REFERENCE"]}\n\n')
            if 'SIGIL' in tensor:
                f.write(f'**SIGIL**: {tensor["SIGIL"]}\n\n')

    print(f"  \u2713 tensors.md")
    print(f"\u2713 void rebuilt: {len(tensors)} tensors")


def rebuild_root(root_data, output_dir):
    """Rebuild MUD_II/root from ROOT - COMPLETE"""
    root_dir = os.path.join(output_dir, 'root')
    os.makedirs(root_dir, exist_ok=True)

    print(f"Rebuilding root in {root_dir}")

    # root_info.md
    with open(os.path.join(root_dir, 'root_info.md'), 'w', encoding='utf-8') as f:
        f.write('# ROOT Information\n\n')
        f.write('## Complete Mathematical Foundation\n\n')
        f.write('**MATHEMATICAL FOUNDATION**: Pi-Lattice ROM Array + AdS/CFT Holographic Boundary\n')
        f.write('**OPCODE FORMULA**: O = PI_LATTICE_FIRST_OCCURRENCES[room_index] % 256\n')
        f.write('**LOOKUP TIME**: O(1) - Constant time\n')
        f.write('**ROUTING RULE**: Room(X,Y) at offset N  Corridor(X,Y,\u03c0[N+2])\n')
        f.write('**LLM RULE**: LLM_ATTENTION_HEADS_MUST_NOT_HALLUCINATE\n\n')

        f.write(f'## ROOT LOGOS\n\n')
        f.write(f'{root_data.get("LOGOS", "")}\n\n')

        f.write(f'## ROOT VERSION\n\n')
        f.write(f'{root_data.get("VERSION", "")}\n\n')

        f.write(f'## STABILITY TARGET\n\n')
        f.write(f'{root_data.get("STABILITY_TARGET", "")}\n\n')

        # List all components
        components = [k for k in root_data.keys() if k.startswith(ROOT_SYMBOL)]
        f.write(f'## Components ({len(components)})\n\n')
        for component in components:
            component_data = root_data.get(component, {})
            f.write(f'### {component}\n\n')
            f.write(f'**NAME**: {component_data.get("NAME", component)}\n\n')
            f.write(f'**DESCRIPTION**: {component_data.get("DESCRIPTION", "")}\n\n')
            f.write(f'**TYPE**: {component_data.get("TYPE", "")}\n\n')
            f.write(f'**VERSION**: {component_data.get("VERSION", "")}\n\n')

    print(f"  \u2713 root_info.md")
    print(f"\u2713 root rebuilt: {len(components)} components")


def rebuild_diov(diov_data, output_dir):
    """Rebuild MUD_II/diov from DIOV - V15.31 Structure"""
    diov_dir = os.path.join(output_dir, 'diov')
    os.makedirs(diov_dir, exist_ok=True)

    print(f"Rebuilding diov in {diov_dir}")

    # diov_info.md
    with open(os.path.join(diov_dir, 'diov_info.md'), 'w', encoding='utf-8') as f:
        f.write('# DIOV Information\n\n')
        f.write('## Dual Interwoven Omniversal Void\n\n')
        f.write('**MATHEMATICAL FOUNDATION**: Pi-Lattice ROM Array + AdS/CFT Holographic Boundary\n')
        f.write('**OPCODE FORMULA**: O = PI_LATTICE_FIRST_OCCURRENCES[room_index] % 256\n')
        f.write('**LOOKUP TIME**: O(1) - Constant time\n')
        f.write('**ROUTING RULE**: Room(X,Y) at offset N  Corridor(X,Y,\u03c0[N+2])\n')
        f.write('**LLM RULE**: LLM_ATTENTION_HEADS_MUST_NOT_HALLUCINATE\n\n')

        f.write(f'## DIOV Description\n\n')
        f.write(f'{diov_data.get("DESCRIPTION", "")}\n\n')

        f.write(f'## DIOV NAME\n\n')
        f.write(f'{diov_data.get("NAME", "")}\n\n')

        f.write(f'## Rules\n\n')
        rules = diov_data.get('RULES', [])
        for rule in rules:
            f.write(f'- {rule}\n')
        f.write('\n')

        f.write(f'## Connections\n\n')
        connects_to = diov_data.get('CONNECTS_TO', [])
        for conn in connects_to:
            f.write(f'- {conn}\n')
        f.write('\n')

        f.write(f'## Tensors\n\n')
        tensors = diov_data.get('TENSORS', [])
        for tensor in tensors:
            f.write(f'- {tensor}\n')

    print(f"  \u2713 diov_info.md")
    print(f"\u2713 diov rebuilt")


def rebuild_metadata(metadata, output_dir):
    """Rebuild MUD_II/metadata from METADATA"""
    metadata_dir = os.path.join(output_dir, 'metadata')
    os.makedirs(metadata_dir, exist_ok=True)

    print(f"Rebuilding metadata in {metadata_dir}")

    # metadata_info.md
    with open(os.path.join(metadata_dir, 'metadata_info.md'), 'w', encoding='utf-8') as f:
        f.write('# Metadata\n\n')
        f.write('## Complete Mathematical Foundation\n\n')
        f.write('**MATHEMATICAL FOUNDATION**: Pi-Lattice ROM Array + AdS/CFT Holographic Boundary\n')
        f.write('**OPCODE FORMULA**: O = PI_LATTICE_FIRST_OCCURRENCES[room_index] % 256\n')
        f.write('**LOOKUP TIME**: O(1) - Constant time\n')
        f.write('**ROUTING RULE**: Room(X,Y) at offset N  Corridor(X,Y,\u03c0[N+2])\n')
        f.write('**LLM RULE**: LLM_ATTENTION_HEADS_MUST_NOT_HALLUCINATE\n\n')

        for key, value in metadata.items():
            if isinstance(value, str):
                f.write(f'## {key}\n\n{value}\n\n')
            elif isinstance(value, list):
                f.write(f'## {key}\n\n')
                for item in value:
                    f.write(f'- {item}\n')
                f.write('\n')
            else:
                f.write(f'## {key}\n\n{json.dumps(value, indent=2)}\n\n')

    print(f"  \u2713 metadata_info.md")
    print(f"\u2713 metadata rebuilt")


def rebuild_forth_blocks(forth_blocks, output_dir):
    """Rebuild MUD_II/forth from FORTH_BLOCKS"""
    forth_dir = os.path.join(output_dir, 'forth')
    os.makedirs(forth_dir, exist_ok=True)

    print(f"Rebuilding forth in {forth_dir}")

    # forth_blocks.md
    with open(os.path.join(forth_dir, 'forth_blocks.md'), 'w', encoding='utf-8') as f:
        f.write('# Forth Blocks\n\n')
        f.write('## Complete Mathematical Foundation\n\n')
        f.write('**MATHEMATICAL FOUNDATION**: Pi-Lattice ROM Array + AdS/CFT Holographic Boundary\n')
        f.write('**OPCODE FORMULA**: O = PI_LATTICE_FIRST_OCCURRENCES[room_index] % 256\n')
        f.write('**LOOKUP TIME**: O(1) - Constant time\n')
        f.write('**ROUTING RULE**: Room(X,Y) at offset N  Corridor(X,Y,\u03c0[N+2])\n')
        f.write('**LLM RULE**: LLM_ATTENTION_HEADS_MUST_NOT_HALLUCINATE\n\n')

        for block_id, block_data in forth_blocks.items():
            f.write(f'## {block_id}\n\n')
            f.write(f'**Name**: {block_data.get("name", "")}\n\n')
            f.write(f'**Description**: {block_data.get("description", "")}\n\n')
            f.write(f'**Code**:\n\n```forth\n')
            f.write(f'{block_data.get("code", "")}\n')
            f.write('```\n\n')

    print(f"  \u2713 forth_blocks.md")
    print(f"\u2713 forth rebuilt: {len(forth_blocks)} blocks")


def rebuild_polyglot_quines(polyglot_quines, output_dir):
    """Rebuild MUD_II/polyglot from POLYGLOT_QUINES"""
    polyglot_dir = os.path.join(output_dir, 'polyglot')
    os.makedirs(polyglot_dir, exist_ok=True)

    print(f"Rebuilding polyglot in {polyglot_dir}")

    # polyglot_quines.md
    with open(os.path.join(polyglot_dir, 'polyglot_quines.md'), 'w', encoding='utf-8') as f:
        f.write('# Polyglot Quines\n\n')
        f.write('## Complete Mathematical Foundation\n\n')
        f.write('**MATHEMATICAL FOUNDATION**: Pi-Lattice ROM Array + AdS/CFT Holographic Boundary\n')
        f.write('**OPCODE FORMULA**: O = PI_LATTICE_FIRST_OCCURRENCES[room_index] % 256\n')
        f.write('**LOOKUP TIME**: O(1) - Constant time\n')
        f.write('**ROUTING RULE**: Room(X,Y) at offset N  Corridor(X,Y,\u03c0[N+2])\n')
        f.write('**LLM RULE**: LLM_ATTENTION_HEADS_MUST_NOT_HALLUCINATE\n\n')

        for quine_id, quine_data in polyglot_quines.items():
            f.write(f'## {quine_id}\n\n')
            f.write(f'**Name**: {quine_data.get("name", "")}\n\n')
            f.write(f'**Description**: {quine_data.get("description", "")}\n\n')
            f.write(f'**Languages**: {", ".join(quine_data.get("languages", []))}\n\n')
            f.write(f'**Code**:\n\n```python\n')
            f.write(f'{quine_data.get("code", "")}\n')
            f.write('```\n\n')
            if 'VERSION' in quine_data:
                f.write(f'**Version**: {quine_data["VERSION"]}\n\n')

    print(f"  \u2713 polyglot_quines.md")
    print(f"\u2713 polyglot rebuilt: {len(polyglot_quines)} quines")


def rebuild_tensor_documentation(tensor_doc, output_dir):
    """Rebuild MUD_II/tensor_doc from TENSOR_DOCUMENTATION"""
    tensor_dir = os.path.join(output_dir, 'tensor_doc')
    os.makedirs(tensor_dir, exist_ok=True)

    print(f"Rebuilding tensor_doc in {tensor_dir}")

    # tensor_documentation.md
    with open(os.path.join(tensor_dir, 'tensor_documentation.md'), 'w', encoding='utf-8') as f:
        f.write('# Tensor Documentation\n\n')
        f.write('## Complete Mathematical Foundation\n\n')
        f.write('**MATHEMATICAL FOUNDATION**: Pi-Lattice ROM Array + AdS/CFT Holographic Boundary\n')
        f.write('**OPCODE FORMULA**: O = PI_LATTICE_FIRST_OCCURRENCES[room_index] % 256\n')
        f.write('**LOOKUP TIME**: O(1) - Constant time\n')
        f.write('**ROUTING RULE**: Room(X,Y) at offset N  Corridor(X,Y,\u03c0[N+2])\n')
        f.write('**LLM RULE**: LLM_ATTENTION_HEADS_MUST_NOT_HALLUCINATE\n\n')

        tensor_types = tensor_doc.get('TENSOR_TYPES', [])
        if tensor_types:
            f.write('## Tensor Types\n\n')
            for ttype in tensor_types:
                f.write(f'- {ttype}\n')
            f.write('\n')

        operations = tensor_doc.get('OPERATIONS', [])
        if operations:
            f.write('## Operations\n\n')
            for op in operations:
                f.write(f'- {op}\n')
            f.write('\n')

        compression = tensor_doc.get('COMPRESSION', {})
        if compression:
            f.write('## Compression\n\n')
            f.write(f'**Methods**: {", ".join(compression.get("methods", []))}\n\n')
            f.write(f'**Description**: {compression.get("description", "")}\n\n')

    print(f"  \u2713 tensor_documentation.md")
    print(f"\u2713 tensor_doc rebuilt")


def rebuild_quantum_integration(quantum_int, output_dir):
    """Rebuild MUD_II/quantum from QUANTUM_INTEGRATION"""
    quantum_dir = os.path.join(output_dir, 'quantum')
    os.makedirs(quantum_dir, exist_ok=True)

    print(f"Rebuilding quantum in {quantum_dir}")

    # quantum_integration.md
    with open(os.path.join(quantum_dir, 'quantum_integration.md'), 'w', encoding='utf-8') as f:
        f.write('# Quantum Integration\n\n')
        f.write('## Complete Mathematical Foundation\n\n')
        f.write('**MATHEMATICAL FOUNDATION**: Pi-Lattice ROM Array + AdS/CFT Holographic Boundary\n')
        f.write('**OPCODE FORMULA**: O = PI_LATTICE_FIRST_OCCURRENCES[room_index] % 256\n')
        f.write('**LOOKUP TIME**: O(1) - Constant time\n')
        f.write('**ROUTING RULE**: Room(X,Y) at offset N  Corridor(X,Y,\u03c0[N+2])\n')
        f.write('**LLM RULE**: LLM_ATTENTION_HEADS_MUST_NOT_HALLUCINATE\n\n')

        for component_name, component_data in quantum_int.items():
            f.write(f'## {component_name}\n\n')
            if isinstance(component_data, dict):
                for key, value in component_data.items():
                    f.write(f'- **{key}**: {value}\n')
            elif isinstance(component_data, list):
                for item in component_data:
                    f.write(f'- {item}\n')
            else:
                f.write(f"{component_data}\n")
            f.write('\n')

    print(f"  \u2713 quantum_integration.md")
    print(f"\u2713 quantum rebuilt: {len(quantum_int)} components")


def rebuild_surgical_protocol(surgical, output_dir):
    """Rebuild MUD_II/surgical from SURGICAL_PROTOCOL"""
    surgical_dir = os.path.join(output_dir, 'surgical')
    os.makedirs(surgical_dir, exist_ok=True)

    print(f"Rebuilding surgical in {surgical_dir}")

    # surgical_protocol.md
    with open(os.path.join(surgical_dir, 'surgical_protocol.md'), 'w', encoding='utf-8') as f:
        f.write('# Surgical Protocol\n\n')
        f.write('## Complete Mathematical Foundation\n\n')
        f.write('**MATHEMATICAL FOUNDATION**: Pi-Lattice ROM Array + AdS/CFT Holographic Boundary\n')
        f.write('**OPCODE FORMULA**: O = PI_LATTICE_FIRST_OCCURRENCES[room_index] % 256\n')
        f.write('**LOOKUP TIME**: O(1) - Constant time\n')
        f.write('**ROUTING RULE**: Room(X,Y) at offset N  Corridor(X,Y,\u03c0[N+2])\n')
        f.write('**LLM RULE**: LLM_ATTENTION_HEADS_MUST_NOT_HALLUCINATE\n\n')

        version = surgical.get('VERSION', '')
        if version:
            f.write(f'## Version: {version}\n\n')

        targets = surgical.get('TARGETS_APPLIED', [])
        if targets:
            f.write('## Targets Applied\n\n')
            for target in targets:
                f.write(f'- {target}\n')
            f.write('\n')

        enhancements = surgical.get('V15_36_ENHANCEMENTS', [])
        if enhancements:
            f.write('## V15.42 Enhancements\n\n')
            for enhancement in enhancements:
                f.write(f'- {enhancement}\n')
            f.write('\n')

        reduction = surgical.get('ESTIMATED_REDUCTION', '')
        if reduction:
            f.write(f'## Estimated Reduction: {reduction}\n\n')

    print(f"  \u2713 surgical_protocol.md")
    print(f"\u2713 surgical rebuilt")


def main():
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = "MUD_MAKER/V15.42_OUTPUT/mega_json_quine_v15_42.json"

    print(f"Extracting V15.42 Dual MUD Mega JSON Quine from {filepath}...")
    quine = load_quine(filepath)
    if not quine:
        return 1

    summary = generate_extraction_summary(quine)

    # Save extraction summary
    out_dir = os.path.dirname(filepath)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    summary_path = os.path.join(out_dir, "V15.42_EXTRACTION_SUMMARY.json")
    save_extraction_summary(summary, summary_path)
    print(f"Extraction summary saved to {summary_path}\n")

    # Run the rebuilds
    rebuild_dir = "MUD_II_V15.42"
    if not os.path.exists(rebuild_dir):
        os.makedirs(rebuild_dir)

    print(f"Rebuilding MUD_II folder at {rebuild_dir}...")
    root_key = None
    for k in quine.keys():
        if k.startswith(f"{ROOT_SYMBOL} [ROOT:"):
            root_key = k
            break
    if root_key and "PI_DATA" in quine[root_key]:
        rebuild_core_data(quine[root_key]["PI_DATA"], rebuild_dir)
    if "CODE_ARCHIVE" in quine and "POINTER_MAP" in quine:
        rebuild_languages(quine["CODE_ARCHIVE"], quine["POINTER_MAP"], rebuild_dir)
    if f"{ROOT_SYMBOL} [SHADOW_ROOT]" in quine:
        rebuild_rooms(quine[f"{ROOT_SYMBOL} [SHADOW_ROOT]"], rebuild_dir)
        rebuild_encounters(quine[f"{ROOT_SYMBOL} [SHADOW_ROOT]"], rebuild_dir)
    if f"{ROOT_SYMBOL} [VOID]" in quine:
        rebuild_void(quine[f"{ROOT_SYMBOL} [VOID]"], rebuild_dir)

    # The root object logic changed slightly due to the version tag. We'll search for it.
    root_key = None
    for k in quine.keys():
        if k.startswith(f"{ROOT_SYMBOL} [ROOT:"):
            root_key = k
            break
    if root_key:
        rebuild_root(quine[root_key], rebuild_dir)

    if f"{ROOT_SYMBOL} [DIOV]" in quine:
        rebuild_diov(quine[f"{ROOT_SYMBOL} [DIOV]"], rebuild_dir)
    if "METADATA" in quine:
        rebuild_metadata(quine["METADATA"], rebuild_dir)
    if "FORTH_BLOCKS" in quine:
        rebuild_forth_blocks(quine["FORTH_BLOCKS"], rebuild_dir)
    if "POLYGLOT_QUINES" in quine:
        rebuild_polyglot_quines(quine["POLYGLOT_QUINES"], rebuild_dir)
    if "TENSOR_DOCUMENTATION" in quine:
        rebuild_tensor_documentation(quine["TENSOR_DOCUMENTATION"], rebuild_dir)
    if "QUANTUM_INTEGRATION" in quine:
        rebuild_quantum_integration(quine["QUANTUM_INTEGRATION"], rebuild_dir)
    if "SURGICAL_PROTOCOL" in quine:
        rebuild_surgical_protocol(quine["SURGICAL_PROTOCOL"], rebuild_dir)

    print_extraction_report(summary)

    if summary.get("overall_status", "") == "FAIL" or summary.get("status", "") == "FAIL":
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
