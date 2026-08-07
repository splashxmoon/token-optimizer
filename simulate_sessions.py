def simulate_session(turns: int, name: str):
    # Standard Workflow Tokens
    # Average full file read: 1500 tokens
    # Average raw test output: 800 tokens
    
    # Optimized Workflow Tokens
    # Average read_skeleton: 150 tokens
    # Average read_symbol: 450 tokens
    # Average exec_smart: 20 tokens
    # Average read_diff: 50 tokens
    
    standard_context = 0
    optimized_context = 0
    
    cumulative_standard = 0
    cumulative_optimized = 0
    
    for turn in range(1, turns + 1):
        # We simulate a typical alternating pattern: read -> execute -> read -> execute
        if turn % 4 == 1:
            # Action: Explore Codebase
            standard_action = 1500 # read full file
            optimized_action = 150 # read_skeleton
        elif turn % 4 == 2:
            # Action: Run Tests
            standard_action = 800 # raw output
            optimized_action = 20 # exec_smart
        elif turn % 4 == 3:
            # Action: Inspect specific function
            standard_action = 1500 # read full file again
            optimized_action = 450 # read_symbol
        else:
            # Action: Run tests / Verify Diff
            standard_action = 800 # raw output
            optimized_action = 50 # read_diff or exec_smart
            
        # Add basic conversational overhead (user prompt + model thought) per turn
        conversational_overhead = 150
        
        standard_context += standard_action + conversational_overhead
        optimized_context += optimized_action + conversational_overhead
        
        cumulative_standard += standard_context
        cumulative_optimized += optimized_context
        
    savings_percent = 100 - (cumulative_optimized / cumulative_standard) * 100
    
    print(f"--- {name} Session ({turns} Turns) ---")
    print(f"Standard Cumulative Billed Tokens: {cumulative_standard:,}")
    print(f"Optimized Cumulative Billed Tokens: {cumulative_optimized:,}")
    print(f"Total Tokens Saved: {cumulative_standard - cumulative_optimized:,} ({savings_percent:.1f}%)")
    print(f"Final Context Window Size: Standard ({standard_context:,}) vs Optimized ({optimized_context:,})\n")

if __name__ == "__main__":
    print("Simulating Compounding Token Savings Over Conversational Sessions...\n")
    simulate_session(5, "Short")
    simulate_session(15, "Medium")
    simulate_session(30, "Long")
