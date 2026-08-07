import tiktoken
from token_optimizer.tools import extract_skeleton, extract_symbol, exec_smart, read_diff
import subprocess
import os

def count_tokens(text: str) -> int:
    try:
        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))
    except Exception:
        return len(text) // 4

def benchmark_file(filepath: str, symbol_name: str = None):
    print(f"\n[ File: {filepath} ]")
    with open(filepath, "r", encoding="utf-8") as f:
        full_text = f.read()
    
    full_tokens = count_tokens(full_text)
    
    skeleton_text = extract_skeleton(filepath)
    skeleton_tokens = count_tokens(skeleton_text)
    print(f"  Full File Tokens: {full_tokens}")
    print(f"  Skeleton Tokens:  {skeleton_tokens} (Saved {100 - (skeleton_tokens/max(1, full_tokens))*100:.1f}%)")
    
    if symbol_name:
        symbol_text = extract_symbol(filepath, symbol_name)
        symbol_tokens = count_tokens(symbol_text)
        print(f"  Symbol '{symbol_name}' Tokens: {symbol_tokens} (Saved {100 - (symbol_tokens/max(1, full_tokens))*100:.1f}%)")

def benchmark_command(cmd: str, name: str):
    print(f"\n[ Command: {name} ]")
    
    # Raw
    try:
        process = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        # For exec_smart comparison, raw output of failing commands usually goes to stdout and stderr
        raw_output = process.stdout + process.stderr
    except Exception as e:
        raw_output = str(e)
    raw_tokens = count_tokens(raw_output)
    
    # Smart
    smart_output = exec_smart(cmd)
    smart_tokens = count_tokens(smart_output)
    
    print(f"  Raw Output Tokens:   {raw_tokens}")
    print(f"  Smart Output Tokens: {smart_tokens} (Saved {100 - (smart_tokens/max(1, raw_tokens))*100:.1f}%)")

def benchmark_diff(filepath: str):
    print(f"\n[ Git Diff Optimization ]")
    # Native
    try:
        raw_output = subprocess.run(["git", "diff", "HEAD", "--", filepath], capture_output=True, text=True).stdout
        raw_tokens = count_tokens(raw_output)
        
        # Smart
        smart_output = read_diff(filepath)
        smart_tokens = count_tokens(smart_output)
        
        print(f"  Standard Git Diff (3 lines context): {raw_tokens} tokens")
        print(f"  Smart Git Diff (1 line context):     {smart_tokens} tokens (Saved {100 - (smart_tokens/max(1, raw_tokens))*100:.1f}%)")
    except Exception as e:
        print(f"  Failed diff benchmark: {e}")

if __name__ == "__main__":
    print("="*50)
    print("EXHAUSTIVE TOKEN SAVINGS BENCHMARK")
    print("="*50)
    
    # 1. File Benchmarks
    benchmark_file("src/token_optimizer/tools.py", "exec_smart")
    benchmark_file("src/token_optimizer/server.py", "register_tools")
    
    # Create a dummy large file with docstrings
    dummy_code = '''
def calculate_physics_engine():
    """
    This is a massive docstring that takes up an insane amount of tokens.
    It describes everything about the physics engine.
    ''' + "bla bla " * 500 + '''
    """
    x = 1
    y = 2
    for i in range(100):
        # some comment
        x += y
    return x
'''
    with open("dummy_large.py", "w", encoding="utf-8") as f:
        f.write(dummy_code)
    benchmark_file("dummy_large.py", "calculate_physics_engine")
    
    # 2. Command Benchmarks
    benchmark_command("pip list", "pip list (Verbose Passing Command)")
    
    # Failing command with huge output
    fail_code = '''
import sys
for i in range(1000):
    print(f"Error log trace line {i}: Memory fault at 0x000F8392AB")
sys.exit(1)
'''
    with open("fail_script.py", "w", encoding="utf-8") as f:
        f.write(fail_code)
    benchmark_command("python fail_script.py", "python fail_script.py (Failing command with 1000 lines of logs)")
    
    # 3. Diff Benchmarks
    # To test diff, we need to modify a tracked file
    with open("src/token_optimizer/tools.py", "a", encoding="utf-8") as f:
        f.write("\n\n# dummy comment to trigger diff\n")
    benchmark_diff("src/token_optimizer/tools.py")
    
    # Cleanup
    os.remove("dummy_large.py")
    os.remove("fail_script.py")
    subprocess.run(["git", "checkout", "--", "src/token_optimizer/tools.py"])

    print("\nBenchmark Complete!")
