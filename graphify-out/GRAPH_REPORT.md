# Graph Report - proyecto-odoo-dgd-ingenieria  (2026-09-11)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 155 nodes · 249 edges · 18 communities (14 shown, 4 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4a78fa16`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Community 0
- Community 1
- Community 2
- Community 3
- Community 4
- Community 5
- Community 6
- Community 7
- Community 8
- Community 9
- Community 10
- Community 11
- Community 12
- Community 13
- Community 14
- Community 15
- Community 16
- Community 17

## God Nodes (most connected - your core abstractions)
1. `_compress_file_locked()` - 18 edges
2. `validate()` - 14 edges
3. `detect_file_type()` - 9 edges
4. `should_compress()` - 8 edges
5. `backup_dir_for()` - 8 edges
6. `file_lock()` - 8 edges
7. `main()` - 7 edges
8. `compress_file()` - 7 edges
9. `lock_path_for()` - 6 edges
10. `write_bytes_atomic()` - 6 edges

## Surprising Connections (you probably didn't know these)
- `benchmark_pair()` --calls--> `validate()`  [EXTRACTED]
  .agents/skills/caveman-compress/scripts/benchmark.py → .agents/skills/caveman-compress/scripts/validate.py
- `_compress_file_locked()` --calls--> `validate()`  [EXTRACTED]
  .agents/skills/caveman-compress/scripts/compress.py → .agents/skills/caveman-compress/scripts/validate.py
- `main()` --calls--> `backup_dir_for()`  [EXTRACTED]
  .agents/skills/caveman-compress/scripts/cli.py → .agents/skills/caveman-compress/scripts/compress.py
- `main()` --calls--> `compress_file()`  [EXTRACTED]
  .agents/skills/caveman-compress/scripts/cli.py → .agents/skills/caveman-compress/scripts/compress.py
- `_compress_file_locked()` --calls--> `should_compress()`  [EXTRACTED]
  .agents/skills/caveman-compress/scripts/compress.py → .agents/skills/caveman-compress/scripts/detect.py

## Import Cycles
- None detected.

## Communities (18 total, 4 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.12
Nodes (23): count_bullets(), extract_code_blocks(), extract_fenced_spans(), extract_headings(), extract_indented_code_blocks(), extract_inline_codes(), extract_paths(), extract_urls() (+15 more)

### Community 1 - "Community 1"
Cohesion: 0.18
Nodes (15): main(), print_usage(), Caveman Compress CLI Usage: caveman <filepath>, detect_file_type(), _is_code_line(), _is_json_content(), _is_yaml_content(), Path (+7 more)

### Community 2 - "Community 2"
Cohesion: 0.18
Nodes (15): build_compress_prompt(), build_fix_prompt(), _compress_file_locked(), first_nonblank_line(), _is_smaller_than_body(), mask_code_blocks(), Caveman Memory Compression Orchestrator Usage: python scripts/compress.py…, Return the first non-blank line, stripped — used to detect a prose preamble… (+7 more)

### Community 3 - "Community 3"
Cohesion: 0.20
Nodes (9): description, files, license, name, private, scripts, test, type (+1 more)

### Community 4 - "Community 4"
Cohesion: 0.20
Nodes (9): description, files, license, name, private, scripts, test, type (+1 more)

### Community 5 - "Community 5"
Cohesion: 0.22
Nodes (9): file_lock(), LockTimeoutError, Raised when another process holds the compress lock past LOCK_WAIT_SECONDS., Attempt the OS-native exclusive lock on fd; raises BlockingIOError if another…, Release the OS-native lock on fd; swallows errors since callers use this in a…, Cross-session exclusive lock on filepath's resolved path, backed by the OS's…, _try_lock_nonblocking(), _unlock() (+1 more)

### Community 6 - "Community 6"
Cohesion: 0.50
Nodes (8): call(), database_from_url(), find_id(), get_or_create_order(), get_or_create_product(), load_env(), main(), Demonstrate creating a new purchase item and reusing it in a later order.

### Community 7 - "Community 7"
Cohesion: 0.47
Nodes (8): available_models(), call(), database_from_url(), find_one(), get_or_create(), load_env(), main(), Load functional demo data inspired by GDG Ingenieria's public services.

### Community 8 - "Community 8"
Cohesion: 0.52
Nodes (6): discover_database(), find_group_id(), load_env(), main(), Create the functional test users used by the Odoo project., rpc_call()

### Community 9 - "Community 9"
Cohesion: 0.60
Nodes (5): benchmark_pair(), count_tokens(), main(), print_table(), Path

### Community 10 - "Community 10"
Cohesion: 0.40
Nodes (6): backup_dir_for(), lock_path_for(), Out-of-tree backup dir for filepath, keyed by its parent dir name — kept…, Cross-session lock path keyed on the same (parent-dir-name, stem) identity…, Shared platform-aware base dir for caveman-compress state (backups, locks) —…, _state_base_dir()

### Community 11 - "Community 11"
Cohesion: 0.40
Nodes (6): compress_file(), is_sensitive_path(), Path, Heuristic denylist for files that must never be shipped to a third-party API., Read a source file as UTF-8, returning (text, line_terminator, raw_bytes).…, read_source()

### Community 12 - "Community 12"
Cohesion: 0.40
Nodes (6): Write ``text`` to ``path`` atomically as UTF-8. Path.write_text() truncates the…, Write ``data`` to ``path`` atomically, preserving permission bits., Write to the target file, surfacing the backup location if the write itself…, write_bytes_atomic(), _write_target(), write_text_atomic()

### Community 13 - "Community 13"
Cohesion: 0.50
Nodes (4): call_claude(), r"""Strip an outer ```markdown ... ``` fence when it wraps the ENTIRE output.…, Send a prompt to Claude. Prefers the Anthropic SDK when ANTHROPIC_API_KEY is…, strip_llm_wrapper()

## Knowledge Gaps
- **20 isolated node(s):** `md`, `skillFile`, `skill`, `demo_users.sh script`, `description` (+15 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 66 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `validate()` connect `Community 0` to `Community 9`, `Community 2`?**
  _High betweenness centrality (0.086) - this node is a cross-community bridge._
- **Why does `_compress_file_locked()` connect `Community 2` to `Community 0`, `Community 1`, `Community 10`, `Community 11`, `Community 12`, `Community 13`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **What connects `md`, `skillFile`, `skill` to the rest of the system?**
  _20 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.11904761904761904 - nodes in this community are weakly interconnected._