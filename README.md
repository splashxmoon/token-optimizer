# ⚡ Token Optimizer MCP

<p align="center">
  <em>A Model Context Protocol (MCP) server that reduces LLM token consumption by 75-94%.</em>
</p>

---

**Token Optimizer** is a powerful MCP skill designed to minimize context window bloat, drastically lower API costs, and improve LLM response times. It intercepts large file reads and verbose terminal outputs, intelligently distilling them down to only the essential information using AST parsing and output truncation.

## ✨ Key Features

- 🏗️ **AST Skeletonization:** Uses `tree-sitter` to parse code and strip implementation bodies, returning only structural outlines (imports, classes, signatures). **Saves up to 90% tokens.**
- 🎯 **Precision Symbol Extraction:** Fetch *only* the specific function, class, or type definition block from a file. **Saves up to 75% tokens.**
- 🔇 **Terminal Log Distillation:** Automatically intercepts passing test suites and builds, stripping verbose `stdout` logs and returning a compact success summary. Retains error traces on failure. **Saves up to 97% tokens.**
- 🔄 **Git Diff Deduplication:** Verifies recent file modifications using `git diff` instead of re-reading full files into the context window.

## 📊 Proven Token Savings

Because LLMs re-process the entire conversation history (context window) on every turn, saving tokens compounds massively over time. We simulated typical development sessions (Read Code -> Run Test -> Edit -> Run Test) to measure cumulative billed tokens.

### Single-Turn Savings (Using `tiktoken`)
- **File Structure Read:** 1,662 tokens ➡️ 157 tokens (**90.6% Reduction**)
- **Single Function Read:** 1,662 tokens ➡️ 544 tokens (**67.3% Reduction**)
- **Terminal Execution:** 745 tokens ➡️ 18 tokens (**97.6% Reduction**)

### Cumulative Session Savings (Compounding Context)
| Session Length | Standard Billed Tokens | Optimized Billed Tokens | Total Tokens Saved |
|---|---|---|---|
| **Short (5 Turns)** | 20,550 | 4,680 | **15,870 (77.2%)** |
| **Medium (15 Turns)** | 158,800 | 37,840 | **120,960 (76.2%)** |
| **Long (30 Turns)** | 609,750 | 147,000 | **462,750 (75.9%)** |

> *In a Long Session (30 turns), the standard agent's context window bloats to 39,000 tokens, causing slow response times and high costs. With Token Optimizer, the context window stays at a lean 9,360 tokens!*

---

## 🚀 Installation

### Plugin Install (Claude Code 1.0.33+)
*The fastest path. One-time marketplace add, then plugin install:*

```bash
/plugin marketplace add splashxmoon/token-optimizer
/plugin install token-optimizer@splashxmoon-token-optimizer
```

### Manual Install (Unix / macOS / Linux)
```bash
git clone --depth 1 https://github.com/splashxmoon/token-optimizer.git
cd token-optimizer
bash install.sh
```

### Windows (PowerShell)
```powershell
git clone --depth 1 https://github.com/splashxmoon/token-optimizer.git
cd token-optimizer
powershell -ExecutionPolicy Bypass -File install.ps1
```
*Why `git clone` instead of `irm | iex`? Security guardrails flag downloading and executing remote code without verification as a supply chain risk. The clone approach lets you inspect `install.ps1` before running it.*

---

## ⚙️ Post-Install Configuration

The manual installation script automatically sets up a clean Python virtual environment (`venv`) and **automatically injects the server configuration directly into your `claude_desktop_config.json`**. 

**Zero manual configuration required!** 

*(Note: If you are using an alternative client like Cursor, the script will also print out the exact configuration block and UI steps for you to copy/paste).*

#### Cursor IDE Configuration
1. Open Cursor Settings > **Features** > **MCP**
2. Click **+ Add New MCP Server**
3. **Name**: `token-optimizer`
4. **Type**: `command`
5. **Command**: `/path/to/token-optimizer/venv/bin/python` *(The install script will provide your exact absolute path)*
6. **Args**: `-m token_optimizer.server`

---

## 🛠️ Tools Provided

### `read_skeleton`
Generates an AST-parsed structural outline of a source file with implementation bodies stripped.
- **Args:** `file_path` (string), `language` (optional string)

### `read_symbol`
Extracts ONLY the specified function, class, or type definition block from a file.
- **Args:** `file_path` (string), `symbol_name` (string)

### `exec_smart`
Executes a shell command (test runner, compiler, linter) and automatically strips passing output, returning ONLY failure stack traces, exit codes, and error lines.
- **Args:** `command` (string), `max_error_lines` (optional int, default 30)

### `read_diff`
Returns a compact git patch/diff of uncommitted edits for a specific file or repository working tree instead of re-reading full files into context.
- **Args:** `file_path` (optional string)

---

## 🧠 How it Works
Token Optimizer leverages [FastMCP](https://github.com/jlowin/fastmcp) to provide tools over the Model Context Protocol. Code parsing is powered by [Tree-sitter](https://tree-sitter.github.io/tree-sitter/), allowing it to seamlessly handle multiple languages (Python, TypeScript, Go, Rust, C++, Java, etc.) dynamically.

## 🤝 Contributing
Pull requests are welcome! If you'd like to add support for more intelligent token reduction strategies, feel free to open an issue or submit a PR.