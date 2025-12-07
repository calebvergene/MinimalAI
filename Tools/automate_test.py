import subprocess
import time 

def run_game():
    """Run the game once and return the last line of output"""
    command = [
        "python3", "AI_Runner.py", "7", "7", "2", "l",
        "../src/checkers-python/main.py",
        "Sample_AIs/Average_AI/main.py"
    ]

    start_time = time.time()
    
    result = subprocess.run(command, capture_output=True, text=True)
    
    # Print all output to terminal
    print(result.stdout, end='')
    if result.stderr:
        print(result.stderr, end='')
    
    # Get the last non-empty line from stdout
    lines = result.stdout.strip().split('\n')
    last_line = lines[-1] if lines else ""
    
    return last_line, time.time() - start_time

def main():
    results = []
    
    with open("game_results90.txt", "w") as f:
        for i in range(100):
            print(f"Running game {i+1}/100...")
            last_output, time_to_run = run_game()
            results.append(last_output)
            f.write(f"Game {i+1}: {int(time_to_run)}s, {last_output}\n")
            f.flush()  # Ensure it's written immediately
    
    from collections import Counter
    counts = Counter(results)
    
    player1_wins = counts.get("player 1 wins", 0)
    ties = counts.get("Tie", 0)
    
    player1_plus_tie = player1_wins + ties


    # Write summary to file
    with open("game_results.txt", "a") as f:
        from collections import Counter
        counts = Counter(results)
        
        f.write("\n" + "="*50 + "\n")
        f.write("SUMMARY\n")
        f.write("="*50 + "\n")
        
        for result, count in counts.items():
            f.write(f"{result}: {count} times ({count/100*100:.1f}%)\n")
    
    print("Results written to game_results.txt")

if __name__ == "__main__":
    main()