# Graph Report - proyecto-odoo-dgd-ingenieria  (2026-09-11)

## Corpus Check
- 80 files · ~40,942 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 518 nodes · 591 edges · 64 communities (42 shown, 20 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `90865452`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- compress.py
- validate.py
- Perfil de GDG Ingeniería
- What You Must Do When Invoked
- caveman-compress/README.md
- Odoo
- cli.py
- cavecrew/SKILL.md
- Caveman Help
- Caveman Compress
- caveman/SKILL.md
- Demo: crear un item nuevo desde Compras
- caveman-commit
- caveman-review
- caveman-explore/package.json
- caveman-learn/package.json
- graphify reference: extra exports and benchmark
- demo_nuevo_item_compra.py
- seed_demo_data.py
- Review Caveman evidence
- Manage eval-gated experiments
- caveman-setup/SKILL.md
- convert_docx_to_markdown.py
- Evaluate an optimization observation
- caveman-stats
- Demo: cotización con partidas internas
- Demo: inventario y trazabilidad en obra
- Demo: gastos urgentes de terreno
- Demo: puesta en servicio de una subestación
- create_users.py
- caveman-discover/SKILL.md
- graphify reference: query, path, explain
- 06-proyectos/README.md
- Demo: compras imputadas a un proyecto
- Demo: facturación del proyecto
- Demo: rentabilidad del proyecto
- inspect_project_capabilities.py
- skills/caveman-learn — the Caveman Learn editing skill (MIT, public)
- caveman-learn skill
- caveman-explore/tests/skill-file.test.mjs
- graphify reference: add a URL and watch a folder
- graphify reference: commit hook and native CLAUDE.md integration
- graphify reference: incremental update and cluster-only
- caveman-learn/tests/skill-file.test.mjs
- graphify reference: GitHub clone and cross-repo merge
- graphify reference: transcribe video and audio
- AGENTS.md
- __init__.py
- investigate-first/SKILL.md
- lean-build/SKILL.md
- migration/SKILL.md
- safe-refactor/SKILL.md
- surgical-patch/SKILL.md
- verify-and-stop/SKILL.md
- extraction-spec.md
- 01-crm/README.md
- 02-ventas/README.md
- 03-compras/README.md
- 04-inventario/README.md
- 05-contabilidad-facturacion/README.md
- 07-integracion/README.md
- demo_users.sh

## God Nodes (most connected - your core abstractions)
1. `_compress_file_locked()` - 18 edges
2. `validate()` - 14 edges
3. `What You Must Do When Invoked` - 12 edges
4. `Odoo` - 11 edges
5. `/graphify` - 10 edges
6. `detect_file_type()` - 9 edges
7. `backup_dir_for()` - 8 edges
8. `file_lock()` - 8 edges
9. `should_compress()` - 8 edges
10. `main()` - 8 edges

## Surprising Connections (you probably didn't know these)
- `main()` --calls--> `backup_dir_for()`  [EXTRACTED]
  .agents/skills/caveman-compress/scripts/cli.py → .agents/skills/caveman-compress/scripts/compress.py
- `main()` --calls--> `compress_file()`  [EXTRACTED]
  .agents/skills/caveman-compress/scripts/cli.py → .agents/skills/caveman-compress/scripts/compress.py
- `_compress_file_locked()` --calls--> `should_compress()`  [EXTRACTED]
  .agents/skills/caveman-compress/scripts/compress.py → .agents/skills/caveman-compress/scripts/detect.py
- `_compress_file_locked()` --calls--> `validate()`  [EXTRACTED]
  .agents/skills/caveman-compress/scripts/compress.py → .agents/skills/caveman-compress/scripts/validate.py
- `benchmark_pair()` --calls--> `validate()`  [EXTRACTED]
  .agents/skills/caveman-compress/scripts/benchmark.py → .agents/skills/caveman-compress/scripts/validate.py

## Import Cycles
- None detected.

## Communities (64 total, 20 thin omitted)

### Community 0 - "compress.py"
Cohesion: 0.08
Nodes (46): backup_dir_for(), build_compress_prompt(), build_fix_prompt(), call_claude(), compress_file(), _compress_file_locked(), file_lock(), first_nonblank_line() (+38 more)

### Community 1 - "validate.py"
Cohesion: 0.10
Nodes (28): benchmark_pair(), count_tokens(), main(), print_table(), Path, count_bullets(), extract_code_blocks(), extract_fenced_spans() (+20 more)

### Community 2 - "Perfil de GDG Ingeniería"
Cohesion: 0.07
Nodes (24): Demos funcionales, Estructura de cada demo, Áreas, Decisiones, Detalles, Mapeo Inicial, Próximos pasos, Resumen (+16 more)

### Community 3 - "What You Must Do When Invoked"
Cohesion: 0.08
Nodes (24): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+16 more)

### Community 4 - "caveman-compress/README.md"
Cohesion: 0.09
Nodes (20): Before / After, Benchmarks, How It Work, <img src="../../docs/assets/dancing-rock.svg" width="20" height="20" alt="rock"/> Caveman (285 tokens), Install, Original (706 tokens), Part of Caveman, Security (+12 more)

### Community 5 - "Odoo"
Cohesion: 0.19
Nodes (9): add_chatter(), database_from_url(), day(), deadline(), load_env(), main(), Odoo, Create an attractive, idempotent GDG Project demo in Odoo. (+1 more)

### Community 6 - "cli.py"
Cohesion: 0.18
Nodes (15): main(), print_usage(), Caveman Compress CLI Usage: caveman <filepath>, detect_file_type(), _is_code_line(), _is_json_content(), _is_yaml_content(), Path (+7 more)

### Community 7 - "cavecrew/SKILL.md"
Cohesion: 0.14
Nodes (12): cavecrew, Example chaining, How to invoke, Model overrides, See also, What it does, Auto-clarity (inherited), Chaining patterns (+4 more)

### Community 8 - "Caveman Help"
Cohesion: 0.14
Nodes (12): caveman-help, Example output, How to invoke, See also, What it does, Caveman Help, Configure Default Mode, Deactivate (+4 more)

### Community 9 - "Caveman Compress"
Cohesion: 0.17
Nodes (11): Boundaries, Caveman Compress, Compress, Compression Rules, Pattern, Preserve EXACTLY (never modify), Preserve Structure, Process (+3 more)

### Community 10 - "caveman/SKILL.md"
Cohesion: 0.17
Nodes (10): caveman, Example output, How to invoke, See also, What it does, Auto-Clarity, Boundaries, Intensity (+2 more)

### Community 11 - "Demo: crear un item nuevo desde Compras"
Cohesion: 0.17
Nodes (11): 1. Crear una nueva orden de compra, 2. Crear el producto que no existe, 3. Completar y confirmar la orden, 4. Usar el producto en una segunda orden, Antes de comenzar, Comprobación final, Demo: crear un item nuevo desde Compras, Importante (+3 more)

### Community 12 - "caveman-commit"
Cohesion: 0.18
Nodes (9): caveman-commit, Example output, How to invoke, See also, What it does, Auto-Clarity, Boundaries, Examples (+1 more)

### Community 13 - "caveman-review"
Cohesion: 0.18
Nodes (9): caveman-review, Example output, How to invoke, See also, What it does, Auto-Clarity, Boundaries, Examples (+1 more)

### Community 14 - "caveman-explore/package.json"
Cohesion: 0.20
Nodes (9): description, files, license, name, private, scripts, test, type (+1 more)

### Community 15 - "caveman-learn/package.json"
Cohesion: 0.20
Nodes (9): description, files, license, name, private, scripts, test, type (+1 more)

### Community 16 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 17 - "demo_nuevo_item_compra.py"
Cohesion: 0.50
Nodes (8): call(), database_from_url(), find_id(), get_or_create_order(), get_or_create_product(), load_env(), main(), Demonstrate creating a new purchase item and reusing it in a later order.

### Community 18 - "seed_demo_data.py"
Cohesion: 0.47
Nodes (8): available_models(), call(), database_from_url(), find_one(), get_or_create(), load_env(), main(), Load functional demo data inspired by GDG Ingenieria's public services.

### Community 19 - "Review Caveman evidence"
Cohesion: 0.25
Nodes (7): Hard rules, Review Caveman evidence, Step 1 — Load context, Step 2 — Establish baseline, Step 3 — Test the leading explanation with traces, Step 4 — Inspect representative traces, Step 5 — Report

### Community 20 - "Manage eval-gated experiments"
Cohesion: 0.25
Nodes (7): Manage eval-gated experiments, Non-negotiable gates, Step 1 — Load project and experiment, Step 2 — Evaluate evidence, Step 3 — Propose one action, Step 4 — Block unsafe execution, Step 5 — Re-read after external operator action

### Community 21 - "caveman-setup/SKILL.md"
Cohesion: 0.25
Nodes (7): Failure templates (use verbatim, filled in — never soften), Rules (non-negotiable), Step 1 — Find every live LLM callsite, Step 2 — Pick the app slug, Step 3 — Wire each callsite, Step 4 — Verify with one real request, Step 5 — Report

### Community 22 - "convert_docx_to_markdown.py"
Cohesion: 0.46
Nodes (7): cell_text(), convert(), main(), paragraph_to_markdown(), Convert a simple DOCX document to Markdown without external packages., table_to_markdown(), text_from_run()

### Community 23 - "Evaluate an optimization observation"
Cohesion: 0.29
Nodes (6): 1. Read the exact observations, 2. Ask the operator to choose, 3. Design a candidate and paired eval, 4. Apply only the approved candidate, 5. Report observations, not savings, Evaluate an optimization observation

### Community 24 - "caveman-stats"
Cohesion: 0.29
Nodes (5): caveman-stats, Example output, How to invoke, See also, What it does

### Community 25 - "Demo: cotización con partidas internas"
Cohesion: 0.29
Nodes (6): Caso de negocio, Demo: cotización con partidas internas, Objetivo, Pasos, Resultado esperado, Validación

### Community 26 - "Demo: inventario y trazabilidad en obra"
Cohesion: 0.29
Nodes (6): Caso de negocio, Demo: inventario y trazabilidad en obra, Objetivo, Pasos, Resultado esperado, Validación

### Community 27 - "Demo: gastos urgentes de terreno"
Cohesion: 0.29
Nodes (6): Caso de negocio, Demo: gastos urgentes de terreno, Objetivo, Pasos, Resultado esperado, Validación

### Community 28 - "Demo: puesta en servicio de una subestación"
Cohesion: 0.29
Nodes (7): Demo: puesta en servicio de una subestación, Guion de demostración con efecto wow, Lista de control antes de recibir al cliente, Objetivo, Preparar la demo automáticamente, Relación con el negocio, Resultado esperado

### Community 29 - "create_users.py"
Cohesion: 0.52
Nodes (6): discover_database(), find_group_id(), load_env(), main(), Create the functional test users used by the Odoo project., rpc_call()

### Community 30 - "caveman-discover/SKILL.md"
Cohesion: 0.33
Nodes (5): Step 1 — Inventory the workflows, Step 2 — Name them, Step 3 — Propose, then apply, Step 4 — Verify, Step 5 — Report

### Community 31 - "graphify reference: query, path, explain"
Cohesion: 0.33
Nodes (5): For /graphify explain, For /graphify path, graphify reference: query, path, explain, Step 0 — Constrained query expansion (REQUIRED before traversal), Step 1 — Traversal

### Community 32 - "06-proyectos/README.md"
Cohesion: 0.33
Nodes (3): Casos disponibles, Demos de Proyectos, Orden recomendado

### Community 33 - "Demo: compras imputadas a un proyecto"
Cohesion: 0.33
Nodes (6): Caso de negocio, Demo: compras imputadas a un proyecto, Objetivo, Pasos, Resultado esperado, Validación

### Community 34 - "Demo: facturación del proyecto"
Cohesion: 0.33
Nodes (5): Demo: facturación del proyecto, Objetivo, Pasos, Resultado esperado, Validación

### Community 35 - "Demo: rentabilidad del proyecto"
Cohesion: 0.33
Nodes (5): Demo: rentabilidad del proyecto, Objetivo, Pasos, Resultado esperado, Validación

### Community 36 - "inspect_project_capabilities.py"
Cohesion: 0.53
Nodes (5): database_from_url(), load_env(), main(), Inspect read-only Odoo Project capabilities for demo preparation., rpc()

### Community 37 - "skills/caveman-learn — the Caveman Learn editing skill (MIT, public)"
Cohesion: 0.40
Nodes (4): Boundary (binding), Install path, Layout, skills/caveman-learn — the Caveman Learn editing skill (MIT, public)

### Community 38 - "caveman-learn skill"
Cohesion: 0.40
Nodes (4): caveman-learn skill, Honesty, Install, What it does

### Community 40 - "graphify reference: add a URL and watch a folder"
Cohesion: 0.50
Nodes (3): For /graphify add, For --watch, graphify reference: add a URL and watch a folder

### Community 41 - "graphify reference: commit hook and native CLAUDE.md integration"
Cohesion: 0.50
Nodes (3): For git commit hook, For native CLAUDE.md integration, graphify reference: commit hook and native CLAUDE.md integration

### Community 42 - "graphify reference: incremental update and cluster-only"
Cohesion: 0.50
Nodes (3): For --cluster-only, For --update (incremental re-extraction), graphify reference: incremental update and cluster-only

## Knowledge Gaps
- **247 isolated node(s):** `name`, `version`, `license`, `private`, `type` (+242 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 330 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `validate()` connect `validate.py` to `compress.py`?**
  _High betweenness centrality (0.008) - this node is a cross-community bridge._
- **Why does `_compress_file_locked()` connect `compress.py` to `validate.py`, `cli.py`?**
  _High betweenness centrality (0.004) - this node is a cross-community bridge._
- **What connects `name`, `version`, `license` to the rest of the system?**
  _247 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `compress.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07585568917668825 - nodes in this community are weakly interconnected._
- **Should `validate.py` be split into smaller, more focused modules?**
  _Cohesion score 0.10160427807486631 - nodes in this community are weakly interconnected._
- **Should `Perfil de GDG Ingeniería` be split into smaller, more focused modules?**
  _Cohesion score 0.07142857142857142 - nodes in this community are weakly interconnected._
- **Should `What You Must Do When Invoked` be split into smaller, more focused modules?**
  _Cohesion score 0.08 - nodes in this community are weakly interconnected._