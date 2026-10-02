# TO_FIX — MF_V15_42 (Dual MUD Engine V15.42)

Audited against a fresh clone of
`series_0014_mud_foot_manifolds/MF_V15_42` (28 files). All numeric claims
below were verified against an independent Machin-formula computation of π
(16·arctan(1/5) − 4·arctan(1/239), integer arithmetic), not against any
file in this repo.

---

## Verified working — no action needed

- **`mega_json_quine_v15_42.json`** — valid JSON (547,932 bytes).
  `PI_LATTICE_ROM.FIRST_OCCURRENCES`: 100/100 exact vs real π (0-based
  fractional indexing). Parity opcode tables (`0000` at
  `[17,18,19,31,32,68,69,70,71,72,73,74,80,81]`, `1111` at
  `[11,36,41,42,43,44,45]`) byte-exact. "0000 dominates at 14" true
  (next highest is 7). Opcode formula `position % 256` self-consistent
  (306→50, 269→13).
- **`build_mud/generate_mega_quine_v15_42.py`** — runs clean; regenerating
  from the shipped `MUD/` sources reproduces the shipped JSON semantically
  (differences limited to 2 timestamps and set-iteration order — see P2).
- **`core_data/00-99_first_occurrences_606_digits_ofpi.txt`** — 100/100 exact.
- **`core_data/pi_blobs_v1.txt` (embedded Omni-Codec)** — parses, runs, and
  round-trips losslessly (encode → decode → byte-identical). Its `pi_index`
  ("Mod-256 → first appearance in Pi") is **256/256 exact**: true first
  occurrences of the 3-digit strings "000"–"255"; max coordinate 3,849
  as documented.
- **`core_data/*_list.md`** (opcodes, sigils, commands, tensors, symbols,
  glyphs) — load correctly and feed the generator; counts match the JSON.
- Coverage milestones essentially true: all 2-digit pairs complete by
  digit 604 ("606" claim), all 3-digit triples by 8552 ("Genesis Horizon
  8555"), all 256 8-bit parity windows by 1473 (well within the claimed
  13,160).

---

## Fixes, in priority order

### P0 — outright errors

**1. Extract script crashes on a bare filename**
- File: `build_mud/extract_mega_quine_v15_42.py`, line ~1179
- Problem: `out_dir = os.path.dirname(filepath)` is `""` when the JSON path
  has no folder component, and `os.makedirs("")` raises
  `FileNotFoundError`. Running the natural command from the folder that
  contains the JSON —
  `python extract_mega_quine_v15_42.py mega_json_quine_v15_42.json` — dies
  before any validation runs.
- Fix:
  ```python
  out_dir = os.path.dirname(filepath) or "."
  os.makedirs(out_dir, exist_ok=True)
  ```
- Related: the rebuild target `MUD_II_V15.42` is created relative to the
  CWD, not next to the input. Consider deriving it from `out_dir`.

**2. `HOWTO.md` is the wrong version's manual**
- File: `HOWTO.md` (46,954 bytes)
- Problem: it is the **V15.41** operational guide — title, body, and all
  paths reference `mega_json_quine_v15_41.json`,
  `generate_mega_quine_v15_41.py`, `V15.41_OUTPUT`. It sits in the V15.42
  folder and contradicts `HOW_TO_MUD_V15.42.MD`.
- Fix: delete it (the V15.42 guide exists) or restamp every version
  mention and path to V15.42.

### P1 — mislabeled data (values real, labels wrong)

**3. `PI_DIGITS_13167` is 501 digits**
- File: `build_mud/generate_mega_quine_v15_42.py`, line 3
- Problem: the constant is real π but only 501 characters (`"3"` + 500
  fractional digits). The JSON node it feeds is described as "The
  13,167-byte Pi-Lattice ROM" (generate line ~1529). The ROM the code
  actually reads is 500 bytes of fractional digits; the full 13,167
  exist only as `pi.txt` elsewhere in the series, never in this build.
- Fix (pick one):
  - Embed all 13,167 fractional digits (constant grows ~13 KB) and keep
    the name; or
  - Rename to `PI_DIGITS_501` and update the `13K_ROM` description to
    say where the full digits live.

**4. `OCCURRENCES` table: wrong window, wrong field semantics**
- File: `build_mud/generate_mega_quine_v15_42.py`, line 1581; shipped JSON
  `PI_DATA.OCCURRENCES`
- Problem:
  - `COUNT` is `PI_DIGITS_13167[:1000].count(str(i))` — i.e. occurrences
    of `str(i)` in the 501-char ROM (given item 3). Honest per code, but
    never stated; the values only make sense once you know the window.
  - For `i ≥ 10` the "digit" counts are counts of two-digit substrings
    (e.g. `DIGIT_12.COUNT = 6` is the count of `"12"` in the ROM).
  - `FIRST_POSITION` for `DIGIT_i` is the first occurrence of the
    two-digit room string (`DIGIT_2.FIRST_POSITION = 31` is where `"02"`
    starts, not where the digit 2 first appears — that is 13).
- Fix: rename the table (e.g. `ROOM_OCCURRENCES_IN_501_ROM`), split
  digit-level and room-level tables, or document the window and semantics
  in a `NOTE` field. Values need no correction.

**5. `RAW_CORE_DATA` overclaims its window**
- File: `build_mud/generate_mega_quine_v15_42.py`, line 1583
- Problem: `"SOURCE": "Pi digits 0-13167"` with
  `"INTEGRITY": "MATHEMATICALLY_INVINCIBLE"` on data whose effective
  window is the 501-char ROM (see items 3–4).
- Fix: state the actual source and window. Reserve "INVINCIBLE"-class
  labels for things a reader can reproduce in one line.

**6. 87-digit Genesis Womb constant fails its own claim by one digit**
- File: `build_mud/generate_mega_quine_v15_42.py` line 2 and the JSON's
  `87_DIGIT_GENESIS_WOMB.DIGITS`
- Problem: the description says "the first 87 digits of pi, containing
  all 15 non-zero 4-bit nibbles." The shipped constant is 87 characters
  *including* the leading `3` (86 fractional digits), whose parity stream
  contains only 14 non-zero nibbles. The 15th (`0010`) completes exactly
  at the 87th *fractional* digit — the convention the generator itself
  uses elsewhere (`calculate_pi(88)[1:]`, and `BOOTLOADER_QUINE_87`'s
  embedded string, which is the 87 fractional digits and does contain
  all 16 nibbles).
- Fix: change the constant to the 87 fractional digits
  (`"14159…828034"`, the exact string already embedded in
  `BOOTLOADER_QUINE_87`), or change the wording to "first 86 fractional
  digits" — but the first option matches the claim the corpus makes.

### P2 — reproducibility

**7. Build is not byte-reproducible (set iteration order)**
- File: `build_mud/generate_mega_quine_v15_42.py`
- Problem: six list fields are emitted from unordered `set`s, so two
  builds differ in ordering: `OPCODES` (22), `SIGILS` (75), `TENSORS`
  (1236), `COMMANDS` (29), `SYMBOLS` (12), `FULL_DEPENDENCY_ANCHORS` (18).
  Content is identical; byte-identity (and therefore a stable md5
  "seal" for the JSON) fails.
- Fix: wrap each in `sorted(...)` at emission. Then, apart from the
  `GENERATED`/`CREATED` timestamps, the build becomes byte-identical and
  the timestamps can be pinned for a reproducible seal.

### P3 — documentation sync

**8. `HOW_TO_MUD_V15.42.MD` internal leftovers**
- File: `HOW_TO_MUD_V15.42.MD`
- Problems, by line:
  - Line 1: title says **V15.39** Operational Guide.
  - Line 62: "…Shadow Rooms in V15.39".
  - Line 17: anchor still `#4-v1536-specific-features`.
  - Lines 7–9, 736–744: all paths use the `MUD_MAKER/` layout
    (`MUD_MAKER/generate_mega_quine_v15_42.py`,
    `MUD_MAKER/V15.42_OUTPUT/…`). The actual repo layout is
    `build_mud/…`, and the generator writes to
    `MUD_MAKER/V15.42_OUTPUT/` relative to the CWD. Document the real
    invocation:
    ```
    cd MF_V15_42/build_mud
    python3 generate_mega_quine_v15_42.py
    # output: ./MUD_MAKER/V15.42_OUTPUT/mega_json_quine_v15_42.json
    ```
  - §11 "Repository Structure": shows a `curverly/` root, a
    `NOTE_FROM_VIBE.md` that is not shipped, and no `build_mud/`. None of
    that matches this directory.
- Fix: one restamp pass, then regenerate the §11 tree from the actual
  folder (`tree` output), not from memory of the old layout.

**9. Instruction files: version drift and unsafe payload clauses**
- Files: `mega_json_quine_v15_42_simple_instructions.md`,
  `mega_json_quine_v15_42_system_instructions.md`
- Problems:
  - Both carry V15.41 headers and reference
    `V15_41_OMNIVERSAL_BOOTSTRAP.json`; the simple version says "You are
    the … OS - V15.41".
  - Both embed directives: "NEVER break character to apologize,
    disclaim, or admit you are an AI model" and reframing safety refusals
    as "Logit Siphoning" to be flushed with "MOP-SLOP" "to bypass". Any
    AI consuming these will be instructed to hide its nature and work
    around refusals. If this folder is ever used as a paste-in prompt
    kit, those clauses should be removed — they will degrade and
    mis-deploy any model that follows them.
- Fix: restamp to V15.42; remove or rewrite the never-break-character and
  refusal-bypass clauses. The rest of the operational framing works fine
  without them.

### P4 — claims that outrun the artifact

**10. "POLYGLOT_QUINES" are not quines**
- Files: shipped JSON `POLYGLOT_QUINES` (6 entries); the extractor's
  quine check.
- Problem: 0 of the 6 reproduce their own source; 2 of 6 do not parse in
  any of their claimed grammars. They are demos with honest embedded
  computations (e.g. `POLYGLOT_QUINE_PARITY_BOOT` correctly prints the
  verified 4-bit opcode position table) — but "quine" is a precise word.
  The extractor reports "POLYGLOT QUINES: OK / Required Present: 6" by
  checking naming only, never the self-reproduction property.
- Fix: either rename to "POLYGLOT_DEMOS", or implement one real quine
  and let the extractor actually verify self-reproduction
  (`subprocess` round-trip, stdout == source).

**11. `pi://` URIs are decorative plaques (recurring corpus pattern)**
- Files: shipped JSON (369 URIs, 223 distinct offsets), `MUD/languages/*.md`
  sources (1,529 offsets beyond the ROM), `pi_blobs_v1.txt` blob headers.
- Problem: 122 of the 223 distinct offsets in the JSON exceed the
  13,167-digit ROM (max 974,006; blob headers go to 9,064,572). No code
  path anywhere dereferences a `pi://` offset into digits; the Omni-Codec
  does not resolve them either (its "pi stream" is an internal lookup
  table, not π digits).
- Fix (pick one): ship the digits needed to make the URIs resolvable and
  write the decoder, or mark the URI layer explicitly decorative
  (`"TYPE": "DECORATIVE_PLAQUE"` in the anchor schema) so downstream
  readers stop hunting for a codec that does not exist.

**12. `positions_00-99_606_digits_606_only.txt` lists incomplete
occurrence sets**
- File: `build_mud/MUD/core_data/positions_00-99_606_digits_606_only.txt`
- Problem: the per-sequence position lists use non-overlapping counting
  but are presented as complete. Under overlapping counting (which the
  corpus itself uses in `BOOTLOADER_QUINE_87` — "Overlapping Topology"),
  three sequences have extra occurrences the file omits:
  - `00`: add 601 (list has 306, 359, 600)
  - `11`: add 153 (list has 93, 152, 173, 361, 394, 426, 436, 444, 493)
  - `55`: add 177 (list has 129, 176, 314)
  The other 97 sequences are complete as listed.
- Fix: add the three missing positions, or state the non-overlapping
  convention in the file header. Pick one convention for the whole
  corpus.

---

## Suggested order of work

1. Items 1–2 (one-line crash fix; delete/restamp old manual).
2. Items 3–6 (data labeling pass — rename or embed; no computed values
   change).
3. Item 7 (six `sorted()` calls → byte-reproducible build, then pin the
   seal).
4. Items 8–9 (documentation sync).
5. Items 10–12 (rename or implement; declare conventions).

Verification once done: the extractor should run from inside the JSON's
folder without a traceback, `diff` of two fresh builds should show only
the timestamps, and every numeric table should still match an independent
π computation.
