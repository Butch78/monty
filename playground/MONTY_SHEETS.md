# Monty Sheets

An AI-native spreadsheet engine where every formula is Python, powered by [Monty](https://github.com/pydantic/monty) for sandboxed execution and [Apache DataFusion](https://github.com/apache/datafusion) for columnar performance. Import existing Excel files, understand them with AI, edit with Python formulas, and export back.

## Problem

| Pain point | Who feels it |
|---|---|
| LLMs generate broken Excel formulas but write excellent Python | Everyone using AI with spreadsheets |
| Users can't read, debug, or explain `=IFERROR(INDEX(MATCH(...)))` | Finance teams, analysts |
| Excel caps at ~6k formula rows before it becomes unresponsive | Engineers, data teams |
| No safe way to run user-defined formulas server-side | Platform builders |
| Numpy/Pandas are overkill for tabular business logic | Non-developers who outgrew Excel |

## Solution

A spreadsheet where every cell formula is Python. AI can read, write, explain, and translate formulas because they're just Python. The engine is sandboxed (Monty), columnar (DataFusion), and fast (Rust).

### Why not Quadratic?

[Quadratic](https://www.quadratichq.com) is the closest competitor — a spreadsheet with Python/SQL support, backed by $11.3M from GV. But:

| | Quadratic | Monty Sheets |
|---|---|---|
| Python runtime | CPython in WASM (slow, ~500ms startup) | Monty (Rust-native, ~1ms startup) |
| Sandbox | None (full CPython) | Resource-limited, no filesystem/network |
| Query engine | Custom cell-by-cell | DataFusion (columnar, parallel) |
| Rendering | React + WebGL (PixiJS) | Vue Vapor / SolidJS (fine-grained) |
| Excel import | Manual re-entry | Automated formula translation |
| License | Source-available (restrictive) | Open source |

## Performance Targets

Benchmarks we need to beat to be competitive. Quadratic claims 60fps rendering with millions of cells via WebGL.

### Rendering (frontend)

| Metric | Excel | Google Sheets | Quadratic | Our target |
|---|---|---|---|---|
| Max responsive rows (with formulas) | ~6,000 | ~150 | ~100,000 | **1,000,000+** |
| Visible cell rendering | DOM | DOM | WebGL (10-50 draw calls) | **WebGL + Vue Vapor** |
| Pan/zoom FPS | 30-60 | 15-30 | 60 | **60** |
| Zoom range | 10%-400% | 50%-200% | 1%-1000% | **1%-1000%** |

### Formula evaluation (backend)

| Metric | Excel | Quadratic (Pyodide) | Our target (Monty) |
|---|---|---|---|
| Single cell evaluation | ~10us | ~500us (WASM overhead) | **<5us** |
| 100k cells recalc | ~1s | ~50s | **<500ms** |
| 1M cells recalc | ~10s | impractical | **<5s** |
| Startup per formula | N/A | ~500ms (Pyodide init) | **<1ms** (compiled bytecode) |
| Parallel evaluation | Single-threaded | GIL-limited | **Multi-core (rayon)** |

### Data operations (DataFusion)

| Operation | Excel | Our target |
|---|---|---|
| SUM over 1M rows | ~2s | **<100ms** (Arrow columnar) |
| Filter 1M rows | ~5s | **<200ms** |
| Sort 1M rows | ~8s | **<500ms** |
| GROUP BY + aggregate | ~10s | **<300ms** |
| Join two 100k-row sheets | Not native | **<1s** |

### Memory

| Metric | Quadratic | Our target |
|---|---|---|
| Memory per cell | ~1KB (Python objects) | **~100-200 bytes** (Rust values) |
| 1M cells overhead | ~1GB | **~100-200MB** |
| WebGL eviction threshold | 500MB | **500MB** (same) |

## Architecture

```
+-------------------------------------------------------------------+
|                        Frontend (Browser)                          |
|  +-----------------------------+  +----------------------------+  |
|  | Spreadsheet Grid            |  | AI Chat / Formula Bar      |  |
|  | Vue 3.6 Vapor (no vDOM)     |  |                            |  |
|  | + WebGL canvas for 100k+    |  | "calculate monthly payment"|  |
|  | + Virtual scrolling         |  | > A1*(A2/12)/(1-(1+A2/12)**-A3) |
|  +-----------------------------+  +----------------------------+  |
+-------------------------------------------------------------------+
         |  WebSocket / REST              |  Claude API
         v                                v
+-------------------------------------------------------------------+
|                         Backend (Rust)                             |
|                                                                   |
|  +------------------+  +------------------+  +-----------------+  |
|  | Sheet Engine     |  | Formula Engine   |  | AI Layer        |  |
|  |                  |  |                  |  |                 |  |
|  | - Cell model     |  | - Monty runtime  |  | - NL -> Python  |  |
|  | - Dep graph      |  | - Compile cache  |  | - Excel -> Py   |  |
|  | - Dirty tracking |  | - Parallel eval  |  | - Py -> Excel   |  |
|  | - Topo sort      |  | - Sandbox limits |  | - Explain cell  |  |
|  +------------------+  +------------------+  +-----------------+  |
|           |                     |                                  |
|           v                     v                                  |
|  +------------------------------------------------------------+   |
|  |                    DataFusion Layer                         |   |
|  |                                                            |   |
|  |  - Columnar storage (Arrow arrays)                         |   |
|  |  - SQL query execution (SUM, GROUP BY, JOIN)               |   |
|  |  - Monty UDFs (custom Python formulas as DataFusion UDFs)  |   |
|  |  - Parallel execution (Tokio)                              |   |
|  |  - Parquet/CSV/JSON import                                 |   |
|  +------------------------------------------------------------+   |
|           |                                                        |
|           v                                                        |
|  +------------------------------------------------------------+   |
|  |              Distributed Layer (optional)                   |   |
|  |                                                            |   |
|  |  pydantic/datafusion-distributed                           |   |
|  |  - Scale to multiple nodes for 10M+ rows                  |   |
|  |  - Partition data across workers                           |   |
|  |  - Push compute to data                                   |   |
|  +------------------------------------------------------------+   |
+-------------------------------------------------------------------+
         |                    |
         v                    v
+------------------+  +------------------+
| Excel I/O        |  | Data Sources     |
| calamine (read)  |  | Parquet, CSV     |
| rust_xlsxwriter  |  | Databases (SQL)  |
| (write)          |  | APIs (REST)      |
+------------------+  +------------------+
```

## How It Works

### Cell-level formulas (Monty)

Every cell formula is a Python expression evaluated by Monty:

```
Cell A1: 100000           -> static value
Cell A2: 0.07             -> static value
Cell A3: 360              -> static value
Cell B1: A1 * (1 + A2) ** A3   -> Monty evaluates with {A1: 100000, A2: 0.07, A3: 360}
Cell B2: math.floor(B1)        -> Monty evaluates with {B1: result_of_B1}
```

Under the hood:
1. Parse cell references from expression
2. Build/update dependency graph (DAG)
3. Topological sort for evaluation order
4. Evaluate each dirty cell via `MontyRun` with resolved inputs
5. Detect circular references from the graph

```rust
// Compile formula once, cache the bytecode
let formula = MontyRun::new(
    "import math\nmath.floor(A1 * rate)".into(),
    "cell_B3",
    vec!["A1".into(), "rate".into()],
)?;

// Evaluate with inputs — microseconds per cell
let result = formula.run_no_limits(vec![
    MontyObject::Float(1234.56),
    MontyObject::Float(0.07),
])?;
// result = MontyObject::Int(86)
```

### Column-level operations (DataFusion)

When a formula operates on a range (`SUM(A1:A1000000)`), DataFusion handles it as a columnar operation — no per-cell iteration:

```rust
// Register sheet columns as Arrow arrays in DataFusion
let ctx = SessionContext::new();
ctx.register_batch("sheet1", arrow_batch)?;

// Range operations become SQL queries
let result = ctx.sql("SELECT SUM(A) FROM sheet1 WHERE A > 5").await?;
```

### Custom formulas as DataFusion UDFs

Complex per-row Python logic becomes a DataFusion UDF powered by Monty:

```rust
// User writes: math.floor(price * tax_rate) if region == 'EU' else round(price * 0.08, 2)
// This compiles to a Monty formula, registered as a DataFusion UDF

let udf = create_scalar_function(
    "cell_formula_B",
    vec![DataType::Float64, DataType::Float64, DataType::Utf8],  // price, tax_rate, region
    DataType::Float64,
    move |args| {
        // Monty evaluates each row — but vectorized across the batch
        monty_eval_batch(&compiled_formula, args)
    },
);
ctx.register_udf(udf);

// DataFusion executes it across 1M rows in parallel
let result = ctx.sql("SELECT cell_formula_B(price, tax_rate, region) FROM sheet1").await?;
```

## Excel Import Pipeline

Import `.xlsx` and translate formulas to Python:

```
Excel file (.xlsx)
    |
    v
[calamine] Parse workbook (Rust-native, fast)
    |
    v
For each cell with a formula:
    |
    +---> Simple formula? (~80%)
    |         |
    |         v
    |     Rule-based translator (deterministic, <1ms)
    |         =SUM(A1:A10)      -> sum(cells('A1:A10'))
    |         =FLOOR(A1, 1)     -> math.floor(A1)
    |         =IF(A1>0, A1, 0)  -> A1 if A1 > 0 else 0
    |         =SQRT(A1)         -> math.sqrt(A1)
    |         =PI()*A1^2        -> math.pi * A1 ** 2
    |
    +---> Complex formula? (~20%)
              |
              v
          LLM translator (Claude API)
              - Send: Excel formula + surrounding cell context
              - Receive: Python equivalent + explanation
              - Verify: run both formulas, compare outputs
              - If mismatch: flag for human review
```

### Supported Excel function mappings

```
Excel                          Python (Monty)
-----------------------------------------------------------
=A1 + B1                       A1 + B1
=SUM(A1:A10)                   sum(cells('A1:A10'))
=AVERAGE(A1:A10)               sum(cells('A1:A10')) / len(cells('A1:A10'))
=IF(A1>0, "yes", "no")        'yes' if A1 > 0 else 'no'
=AND(A1>0, B1>0)               A1 > 0 and B1 > 0
=OR(A1>0, B1>0)                A1 > 0 or B1 > 0
=FLOOR(A1, 1)                  math.floor(A1)
=CEILING(A1, 1)                math.ceil(A1)
=SQRT(A1)                      math.sqrt(A1)
=ROUND(A1, 2)                  round(A1, 2)
=ABS(A1)                       abs(A1)
=MIN(A1, B1, C1)               min(A1, B1, C1)
=MAX(A1:A10)                   max(cells('A1:A10'))
=POWER(A1, 2)                  A1 ** 2
=MOD(A1, 3)                    A1 % 3
=LOG(A1)                       math.log10(A1)
=LN(A1)                        math.log(A1)
=EXP(A1)                       math.exp(A1)
=PI()                          math.pi
=SIN/COS/TAN(A1)               math.sin/cos/tan(A1)
=GCD(A1, B1)                   math.gcd(A1, B1)
=FACT(A1)                      math.factorial(A1)
=COMBIN(n, k)                  math.comb(n, k)
=COUNTIF(A1:A10, ">5")         len([x for x in cells('A1:A10') if x > 5])
=SUMIF(A1:A10, ">5")           sum(x for x in cells('A1:A10') if x > 5)
=VLOOKUP(key, range, col, 0)   lookup(key, range, col)
```

## Excel Export Pipeline

```
Python formula
    |
    +---> Has excel_origin and value unchanged?
    |         -> Use original Excel formula (round-trip fidelity)
    |
    +---> Simple Python expression?
    |         -> Rule-based reverse translation
    |         math.floor(A1)         -> =FLOOR(A1, 1)
    |         A1 if A1 > 0 else 0    -> =IF(A1>0, A1, 0)
    |         A1 ** 2                -> =POWER(A1, 2)
    |
    +---> Complex Python?
    |         -> LLM translation to Excel formula
    |         -> If not translatable: export as static value
    |         -> Flag cell as "formula lost in export"
    |
    v
Write .xlsx with rust_xlsxwriter
```

## AI Layer

### Natural language to formula
```
User: "calculate the monthly loan payment"
AI:   A1 * (A2/12) / (1 - (1 + A2/12) ** -A3)
      Explanation: "Standard amortisation formula using principal (A1),
      annual rate (A2), and total months (A3)"
```

### Explain existing formula
```
User clicks cell with: sum(x * y for x, y in zip(col('qty'), col('price')))
AI: "Calculates total revenue by multiplying each item's quantity
     by its price, then summing the results."
```

### Excel import translation
```
Excel:  =IFERROR(INDEX($B$2:$B$100,MATCH(1,(A2=$A$2:$A$100)*(C2=$C$2:$C$100),0)),"Not Found")
AI:     next((b for a, b, c in zip(col('A'), col('B'), col('C'))
              if a == A2 and c == C2), 'Not Found')
        Explanation: "Looks up a value in column B where both column A matches
        this row's A value and column C matches this row's C value."
```

## Tech Stack

| Layer | Technology | Why |
|---|---|---|
| Formula runtime | [Monty](https://github.com/pydantic/monty) | Sandboxed Python, Rust-native, <5us per cell |
| Query engine | [DataFusion](https://github.com/apache/datafusion) | Columnar, parallel, SQL + UDFs |
| Distributed | [datafusion-distributed](https://github.com/pydantic/datafusion-distributed) | Scale to multiple nodes (optional) |
| Excel read | [calamine](https://github.com/tauri-apps/calamine) | Fast Rust-native .xlsx/.ods/.xls parsing |
| Excel write | [rust_xlsxwriter](https://github.com/jmcnamara/rust_xlsxwriter) | Full-featured .xlsx generation |
| Dep graph | [petgraph](https://github.com/petgraph/petgraph) | Topological sort, cycle detection |
| Parallelism | [rayon](https://github.com/rayon-rs/rayon) | Data-parallel cell evaluation |
| AI | [Claude API](https://docs.anthropic.com/) | Formula translation + explanation |
| Frontend grid | Vue 3.6 Vapor or SolidJS | Fine-grained reactivity, no vDOM overhead |
| Canvas render | WebGL (PixiJS or custom) | 100k+ visible cells at 60fps |
| WASM bridge | wasm-bindgen | Client-side Monty for formula preview |

## Project Structure

```
monty-sheets/
    crates/
        monty-sheets-core/          # Core engine (Rust library)
            src/
                lib.rs              # Public API
                sheet.rs            # Sheet model (cells, grid, metadata)
                cell.rs             # Cell types (Value, Formula, Error)
                graph.rs            # Dependency DAG (petgraph) + topo sort
                eval.rs             # Monty evaluation + formula caching
                datafusion.rs       # DataFusion integration + UDF registration
                import/
                    mod.rs
                    excel.rs        # calamine .xlsx parsing
                    translator.rs   # Excel formula -> Python (rule-based)
                    csv.rs          # CSV import
                export/
                    mod.rs
                    excel.rs        # rust_xlsxwriter .xlsx generation
                    reverse.rs      # Python -> Excel (rule-based)
                ai/
                    mod.rs
                    client.rs       # Claude API client
                    translate.rs    # Complex formula translation
                    explain.rs      # Cell explanation generation
            tests/
                fixtures/           # Sample .xlsx files
                test_import.rs
                test_eval.rs
                test_export.rs
                test_roundtrip.rs   # Import -> edit -> export -> compare
                test_datafusion.rs  # Columnar operations
                bench_eval.rs       # Performance benchmarks

        monty-sheets-cli/           # CLI tool
            src/
                main.rs             # import, eval, export, chat commands

        monty-sheets-server/        # HTTP API server
            src/
                main.rs             # WebSocket + REST API
                handlers.rs         # Cell edit, recalc, import/export endpoints

        monty-sheets-wasm/          # WASM build for browser
            src/
                lib.rs              # Client-side formula preview

    frontend/                       # Vue 3.6 Vapor app
        src/
            components/
                Grid.vue            # Spreadsheet grid (Vapor mode)
                FormulaBar.vue      # Formula editor
                Chat.vue            # AI chat panel
            composables/
                useSheet.ts         # Sheet state management
                useWebSocket.ts     # Real-time sync
            workers/
                render.worker.ts    # Off-main-thread layout

    Cargo.toml                      # Workspace
```

## MVP Phases

### Phase 1: CLI — Import & Understand
```bash
monty-sheets import budget.xlsx -o budget.json
monty-sheets show budget.json
monty-sheets explain budget.json B7
monty-sheets graph budget.json          # show dependency graph
```
- Parse .xlsx with calamine
- Rule-based formula translation (~80% coverage)
- LLM fallback for complex formulas
- Output: JSON sheet model with Python formulas

### Phase 2: CLI — Evaluate & Edit
```bash
monty-sheets eval budget.json
monty-sheets set budget.json B7 "math.ceil(sum(col('expenses')) * 1.1)"
monty-sheets eval budget.json           # recalculate
```
- Dependency graph evaluation via Monty
- Formula compilation cache (MontyRun serialization)
- Parallel evaluation with rayon

### Phase 3: CLI — Export & Round-trip
```bash
monty-sheets export budget.json -o budget_v2.xlsx
monty-sheets export budget.json --report # show untranslatable formulas
```
- Python-to-Excel reverse translation
- Round-trip fidelity (preserve original Excel formulas)
- Loss report for untranslatable cells

### Phase 4: DataFusion Integration
- Register sheet data as Arrow tables
- Range operations (SUM, AVERAGE, COUNTIF) via DataFusion SQL
- Custom Monty formulas as DataFusion UDFs
- 1M+ row support

### Phase 5: Web UI
- Vue 3.6 Vapor spreadsheet grid
- WebGL canvas for large datasets
- AI chat panel (Claude API)
- Real-time collaboration via WebSocket

### Phase 6: Distributed
- datafusion-distributed for multi-node queries
- Partition large sheets across workers
- Scale to 10M+ rows

## Example: Full Round-trip

```bash
# 1. Start with an Excel budget spreadsheet
#    A1: "Revenue"  B1: 500000
#    A2: "Tax Rate"  B2: 0.20
#    A3: "Tax"       B3: =B1*B2
#    A4: "Net"       B4: =B1-B3

# 2. Import and translate
$ monty-sheets import budget.xlsx -o budget.json

# 3. See translated formulas
$ monty-sheets show budget.json
  A1: "Revenue"     B1: 500000
  A2: "Tax Rate"    B2: 0.20
  A3: "Tax"         B3: B1 * B2              (was: =B1*B2)
  A4: "Net"         B4: B1 - B3              (was: =B1-B3)

# 4. Add a Python formula
$ monty-sheets set budget.json B5 "math.ceil(B3 * 1.05)"
$ monty-sheets eval budget.json
  B5: math.ceil(B3 * 1.05) = 105000

# 5. Ask AI to add a calculation
$ monty-sheets chat budget.json
> Add effective tax with 5% surcharge, rounded up
  Added B5: math.ceil(B3 * 1.05) = 105000

# 6. Export back to Excel
$ monty-sheets export budget.json -o budget_v2.xlsx
  B3: =B1*B2             (original preserved)
  B4: =B1-B3             (original preserved)
  B5: =CEILING(B3*1.05,1) (translated from Python)

# 7. Open budget_v2.xlsx in Excel — everything works
```

## Key Design Decisions

1. **Monty for formulas, DataFusion for data**: Cell-level Python logic runs in Monty's sandbox. Column-level operations (SUM, filter, sort, join) run in DataFusion. Each engine does what it's best at.

2. **Rule-based translation first, LLM second**: Deterministic translation for ~80% of Excel formulas. LLM only for the complex 20%. Fast, predictable, auditable.

3. **Preserve Excel origin**: Store the original Excel formula alongside the Python translation. On export, prefer the original if the value hasn't changed. Maximum round-trip fidelity.

4. **Vue Vapor over React**: Fine-grained reactivity updates individual cells without vDOM diffing. Critical for a grid with 100k+ visible cells. Falls back to WebGL canvas for extreme scale.

5. **CLI first**: Validate the core engine without UI complexity. The sheet model is JSON — any frontend can consume it later.

6. **Compilation caching**: `MontyRun` is serializable. Compile each unique formula once, cache the bytecode. Most sheets reuse the same formula across rows, so ~50-100 unique compilations covers an entire workbook.

## Proof of Concept

A working Python POC is in `playground/monty_sheets/` with 39 passing tests covering:
- Cell evaluation via Monty (math.floor, sqrt, pi, log, trig, gcd)
- Dependency graph with topological sort (chains, diamonds, cascading updates)
- Excel formula translation (SUM, IF, AND/OR, SQRT, PI, FLOOR, POWER)
- Circular reference detection
- Error handling (division by zero, math domain errors)
- Full budget spreadsheet round-trip

```bash
PYTHONPATH=playground uv run python playground/monty_sheets/test_engine.py
```
