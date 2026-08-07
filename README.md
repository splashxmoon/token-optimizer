# Token Optimizer MCP

An MCP server designed to dramatically reduce token consumption by intelligently stripping unnecessary code bodies and verbose terminal outputs during agent interactions.

## Tools
- `read_skeleton`: AST-based code structural outline.
- `read_symbol`: AST-based exact symbol extraction.
- `exec_smart`: Intelligent terminal execution with success-output stripping.
- `read_diff`: Efficient git diffs.
