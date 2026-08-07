from token_optimizer.tools import extract_skeleton, extract_symbol, exec_smart, read_diff

print("=== TESTING extract_skeleton ===")
print(extract_skeleton("src/token_optimizer/server.py"))

print("\n=== TESTING extract_symbol ===")
print(extract_symbol("src/token_optimizer/server.py", "exec_smart"))

print("\n=== TESTING exec_smart (success) ===")
print(exec_smart("echo hello"))

print("\n=== TESTING exec_smart (failure) ===")
print(exec_smart("python -c 'print(\"foo\"); 1/0'"))

print("\n=== TESTING read_diff ===")
print(read_diff())
