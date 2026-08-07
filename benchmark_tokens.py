import tiktoken
from token_optimizer.tools import extract_skeleton, extract_symbol, exec_smart
import subprocess

def count_tokens(text: str) -> int:
    try:
        enc = tiktoken.get_encoding("cl100k_base")
        return len(enc.encode(text))
    except Exception:
        return len(text) // 4  # Rough fallback

def run_benchmarks():
    target_file = "src/token_optimizer/tools.py"
    
    with open(target_file, "r", encoding="utf-8") as f:
        full_text = f.read()
    
    full_tokens = count_tokens(full_text)
    
    skeleton_text = extract_skeleton(target_file)
    skeleton_tokens = count_tokens(skeleton_text)
    
    symbol_text = extract_symbol(target_file, "extract_skeleton")
    symbol_tokens = count_tokens(symbol_text)
    
    print("--- AST Token Optimization ---")
    print(f"Full File ({target_file}): {full_tokens} tokens")
    print(f"Skeleton View: {skeleton_tokens} tokens (Saved {100 - (skeleton_tokens/full_tokens)*100:.1f}%)")
    print(f"Single Symbol View (extract_skeleton): {symbol_tokens} tokens (Saved {100 - (symbol_tokens/full_tokens)*100:.1f}%)")
    
    print("\n--- Terminal Output Optimization ---")
    raw_cmd = "pip list"
    try:
        raw_output = subprocess.run(raw_cmd, shell=True, capture_output=True, text=True).stdout
        raw_tokens = count_tokens(raw_output)
        
        smart_output = exec_smart(raw_cmd)
        smart_tokens = count_tokens(smart_output)
        
        print(f"Raw Command Output (`{raw_cmd}`): {raw_tokens} tokens")
        print(f"Smart Exec Output: {smart_tokens} tokens (Saved {100 - (smart_tokens/max(1, raw_tokens))*100:.1f}%)")
    except Exception as e:
        print(f"Terminal test failed: {e}")

if __name__ == "__main__":
    run_benchmarks()
