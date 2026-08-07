# ⚡ Token Optimizer MCP

<p align="center">
  <em>A Model Context Protocol (MCP) server that reduces LLM token consumption by 75-94%.</em>
</p>

---

**Token Optimizer** is a powerful MCP skill designed to minimize context window bloat, drastically lower API costs, and improve LLM response times. It intercepts large file reads and verbose terminal outputs, intelligently distilling them down to only the essential information using AST parsing and output truncation.

## ✨ Key Features

- 🏗️ **AST Skeletonization:** Uses `tree-sitter` to parse code and strip implementation bodies, returning only structural outlines (imports, classes, signatures). **Saves up to 90% tokens.**
- 🎯 **Precision Symbol Extraction:** Fetch *only* the specific function, class, or interface you need to edit without loading the entire file into context. **Saves up to 75% tokens.**
- 🔇 **Terminal Log Distillation:** Automatically intercepts passing test suites and builds, stripping verbose `stdout` logs and returning a compact success summary. Retains error traces on failure. **Saves up to 97% tokens.**
- 🔄 **Git Diff Deduplication:** Verifies recent file modifications using `git diff` instead of re-reading full files into the context window.

## 📊 Proven Token Savings

Based on our `tiktoken` benchmarks:
- **File Structure Read:** 1,563 tokens ➡️ 157 tokens (**90.0% Reduction**)
- **Single Function Read:** 1,563 tokens ➡️ 447 tokens (**71.4% Reduction**)
- **Terminal Execution:** 745 tokens ➡️ 18 tokens (**97.6% Reduction**)

---

## 🚀 Installation

### Plugin Install (Claude Code 1.0.33+)
*The fastest path. One-time marketplace add, then plugin install:*

```bash
/plugin marketplace add splashxmoon/token-optimizer
/plugin install token-optimizer@splashxmoon-token-optimizer
```
*Note: No global Python packages or PATH shims are created. The installation is isolated within your client.*

### Manual Install (Unix / macOS / Linux)
```bash
git clone --depth 1 https://github.com/splashxmoon/token-optimizer.git
bash token-optimizer/install.sh
```

### Windows (PowerShell)
```powershell
git clone --depth 1 https://github.com/splashxmoon/token-optimizer.git
powershell -ExecutionPolicy Bypass -File token-optimizer\install.ps1
```
*Why `git clone` instead of `irm | iex`? Security guardrails flag downloading and executing remote code without verification as a supply chain risk. The clone approach lets you inspect `install.ps1` before running it.*

### Post-Install Configuration
If you used the Manual Install, the setup script will output a JSON snippet. Add it to your `mcp.json` or MCP client config:

```json
{
  "mcpServers": {
    "token-optimizer": {
      "command": "/path/to/token-optimizer/venv/bin/python",
      "args": [
        "-m",
        "token_optimizer.server"
      ]
    }
  }
}
```

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
- **Args:** `command` (string), `max_error_lines` (optional int, default 50)

### `read_diff`
Returns a compact git patch/diff of uncommitted edits for a specific file or repository working tree instead of re-reading full files into context.
- **Args:** `file_path` (optional string)

---

## 🧠 How it Works
Token Optimizer leverages [FastMCP](https://github.com/jlowin/fastmcp) to provide tools over the Model Context Protocol. Code parsing is powered by [Tree-sitter](https://tree-sitter.github.io/tree-sitter/), allowing it to seamlessly handle multiple languages (Python, TypeScript, Go, Rust, C++, Java, etc.) dynamically.

## 🤝 Contributing
Pull requests are welcome! If you'd like to add support for more intelligent token reduction strategies, feel free to open an issue or submit a PR.