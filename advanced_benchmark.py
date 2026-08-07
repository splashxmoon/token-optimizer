import tiktoken

def count_tokens(text: str) -> int:
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))

# Define Token Costs (Approximations based on Claude 3.5 Sonnet / GPT-4o input costs)
COST_PER_MILLION_TOKENS = 3.00

# Base metrics derived from our previous empirical tests
METRICS = {
    "read_file_small": {"std": 500, "opt": 50},       # 90% savings
    "read_file_large": {"std": 5000, "opt": 250},     # 95% savings
    "read_file_bloat": {"std": 1500, "opt": 15},      # 99% savings (docstrings)
    "read_symbol": {"std": 5000, "opt": 300},         # read full large file vs just symbol
    "test_pass": {"std": 800, "opt": 20},             # 97% savings
    "test_fail": {"std": 14000, "opt": 450},          # 96% savings
    "git_diff": {"std": 500, "opt": 200},             # 60% savings
    "chat_overhead": 200                              # tokens per turn just talking
}

class Persona:
    def __init__(self, name, pattern):
        self.name = name
        self.pattern = pattern  # list of action keys

personas = [
    Persona("The Explorer", ["read_file_large", "read_file_bloat", "read_file_small", "read_symbol"] * 10),
    Persona("The Debugger", ["test_fail", "read_symbol", "test_fail", "git_diff"] * 10),
    Persona("The Developer", ["read_file_small", "read_symbol", "test_pass", "git_diff", "test_fail"] * 10)
]

def format_money(tokens: int) -> str:
    return f"${(tokens / 1_000_000) * COST_PER_MILLION_TOKENS:.4f}"

def run_simulation(persona: Persona, turns: int):
    std_context = 0
    opt_context = 0
    
    std_cumulative = 0
    opt_cumulative = 0
    
    for turn in range(turns):
        action = persona.pattern[turn % len(persona.pattern)]
        
        std_action_tokens = METRICS[action]["std"]
        opt_action_tokens = METRICS[action]["opt"]
        
        # Context grows with each action
        std_context += std_action_tokens + METRICS["chat_overhead"]
        opt_context += opt_action_tokens + METRICS["chat_overhead"]
        
        # LLMs bill cumulatively for the entire context window every turn
        std_cumulative += std_context
        opt_cumulative += opt_context
        
    savings_pct = (1 - (opt_cumulative / std_cumulative)) * 100 if std_cumulative > 0 else 0
    
    return {
        "turns": turns,
        "std_cum": std_cumulative,
        "opt_cum": opt_cumulative,
        "std_cost": format_money(std_cumulative),
        "opt_cost": format_money(opt_cumulative),
        "savings_pct": savings_pct,
        "std_final_ctx": std_context,
        "opt_final_ctx": opt_context
    }

print("=== ADVANCED TOKEN OPTIMIZATION BENCHMARK ===\n")

for persona in personas:
    print(f"[{persona.name} Persona]")
    for turns in [10, 50, 100]:
        res = run_simulation(persona, turns)
        print(f"  {turns} Turns:")
        print(f"    Std Context: {res['std_final_ctx']:,} | Opt Context: {res['opt_final_ctx']:,}")
        print(f"    Std Billed:  {res['std_cum']:,} tokens ({res['std_cost']})")
        print(f"    Opt Billed:  {res['opt_cum']:,} tokens ({res['opt_cost']})")
        print(f"    Savings:     {res['savings_pct']:.2f}%\n")
