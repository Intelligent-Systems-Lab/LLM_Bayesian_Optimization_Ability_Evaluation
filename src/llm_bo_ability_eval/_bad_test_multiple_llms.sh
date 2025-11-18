#!/bin/bash

# Shell script to run main.py with multiple LLMs and experiment configurations
# Prepare "llm_key_config.txt" like:
#   gpt:YOUR_GPT_API_KEY
#   gemini:YOUR_GEMINI_API_KEY
#   claude:YOUR_CLAUDE_API_KEY
#   deepseek:YOUR_DEEPSEEK_API_KEY
#   qwen:YOUR_QWEN_API_KEY
#
# Usage: ./test_multiple_llms.sh [options]

# Configuration
LLM_KEY_FILE="llm_key_config.txt"

# List of LLMs to test (edit this array to control which LLMs run)
# declare -a LLMS=("gpt" "gemini" "claude" "deepseek" "qwen")
declare -a LLMS=("gemini" "qwen")

# List of experiment types (100 problems first, then 24 problems)
declare -a EXPERIMENTS=("100" "24")

# Default values
MAX_FILES=""
FOREGROUND=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --foreground)
            FOREGROUND=true
            shift
            ;;
        -m|--max-files)
            MAX_FILES="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 [--foreground] [-m|--max-files N]"
            echo "  --foreground    Run in foreground (default: background)"
            echo "  -m, --max-files Maximum number of files to test (for debugging)"
            echo "  -h, --help      Show this help message"
            echo ""
            echo "Note: Edit the LLMS array in the script to control which LLMs to test."
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            echo "Use -h or --help for usage information"
            exit 1
            ;;
    esac
done

# Set timestamp and log directory
TIMESTAMP=$(date '+%m%d%H%M%S')
LOG_DIR="."
LOG_NAME_PREFIX="${LOG_DIR}/llm_bo_experiments_${TIMESTAMP}"

# Log file to store PIDs
PID_LOG="${LOG_NAME_PREFIX}_pids.log"

# Function to get API key for a given LLM
get_api_key() {
    local llm=$1
    if [ ! -f "$LLM_KEY_FILE" ]; then
        echo "Error: Config file $LLM_KEY_FILE not found!"
        exit 1
    fi
    local key=$(grep "^${llm}:" "$LLM_KEY_FILE" | cut -d':' -f2)
    if [ -z "$key" ]; then
        echo "Error: No API key found for $llm"
        exit 1
    fi
    echo "$key"
}

# Function to start a single experiment
start_single_experiment() {
    local llm="$1"
    local exp="$2"
    local exp_number="$3"
    
    echo "Starting experiment #${exp_number}: LLM=${llm}, Experiment=${exp} problems..."
    
    # Set the problem set path based on experiment type
    local PROBLEM_PATH
    if [ "$exp" == "100" ]; then
        PROBLEM_PATH="problem_set/100problems"
    elif [ "$exp" == "24" ]; then
        PROBLEM_PATH="problem_set/24problems"
    elif [ "$exp" == "5" ]; then
        PROBLEM_PATH="problem_set/5problems"
    else
        PROBLEM_PATH="problem_set/${exp}problems"
    fi
    
    # Create log file for this experiment
    local LOG_FILE="${LOG_NAME_PREFIX}_${exp_number}_${llm}_${exp}problems.log"
    
    # Get API key for this LLM
    local api_key=$(get_api_key "$llm")
    
    # Build command
    local cmd="python main.py -l $llm -e $exp -p $PROBLEM_PATH"
    if [ -n "$MAX_FILES" ]; then
        cmd="$cmd -m $MAX_FILES"
    fi
    
    # Start experiment in background with nohup
    nohup bash -c "
        export OPENAI_API_KEY='$api_key'
        echo 'Starting experiment at $(date)'
        echo 'Command: $cmd'
        echo 'API Key: ${api_key:0:10}...'
        echo '=========================='
        $cmd
        echo '=========================='
        echo 'Experiment completed at $(date)'
    " > "$LOG_FILE" 2>&1 &
    
    local PID=$!
    echo "Started experiment #${exp_number} with PID: ${PID} (log: ${LOG_FILE})"
    echo "${llm}_${exp}problems ${PID}" >> "$PID_LOG"
    
    return 0
}

# Function to run all experiments
run_all_experiments() {
    local exp_counter=1
    
    echo "Starting all LLM experiments..."
    echo "Total LLMs: ${#LLMS[@]}"
    echo "Total experiments per LLM: ${#EXPERIMENTS[@]}"
    echo "Total experiments: $((${#LLMS[@]} * ${#EXPERIMENTS[@]}))"
    echo ""
    
    # Loop through each LLM
    for llm in "${LLMS[@]}"; do
        echo "=== Starting experiments for LLM: $llm ==="
        
        # Loop through each experiment type
        for exp in "${EXPERIMENTS[@]}"; do
            start_single_experiment "$llm" "$exp" "$exp_counter"
            exp_counter=$((exp_counter + 1))
            
            # Small delay between starting experiments
            sleep 2
        done
        
        echo ""
    done
}

# Function to check if all experiments are completed
check_experiment_completion() {
    echo "Checking completion status of experiments..."
    
    local all_completed=true
    local total_experiments=0
    local completed_experiments=0
    
    while read -r exp_name pid; do
        if [ -n "$exp_name" ] && [ -n "$pid" ]; then
            total_experiments=$((total_experiments + 1))
            
            # Check if process is still running
            if ps -p "$pid" > /dev/null 2>&1; then
                echo "Experiment $exp_name (PID: $pid) is still running"
                all_completed=false
            else
                echo "Experiment $exp_name (PID: $pid) has finished"
                completed_experiments=$((completed_experiments + 1))
            fi
        fi
    done < "$PID_LOG"
    
    echo "Progress: $completed_experiments/$total_experiments experiments completed"
    
    $all_completed
}

# Function to stop all running experiments
stop_all_experiments() {
    echo "Stopping all running experiments..."
    
    if [ ! -f "$PID_LOG" ]; then
        echo "No PID log found. No experiments to stop."
        return
    fi
    
    # Function to kill a process and all its children recursively
    kill_process_tree() {
        local PARENT_PID=$1
        local CHILDREN=$(pgrep -P "$PARENT_PID" 2>/dev/null)
        
        # First kill children
        for CHILD_PID in $CHILDREN; do
            kill_process_tree "$CHILD_PID"
        done
        
        # Then kill parent
        if ps -p "$PARENT_PID" > /dev/null 2>&1; then
            echo "Killing process $PARENT_PID"
            kill -9 "$PARENT_PID" 2>/dev/null
        fi
    }
    
    # Read and kill each process
    while read -r exp_name pid; do
        if [ -n "$exp_name" ] && [ -n "$pid" ]; then
            echo "Stopping $exp_name (PID: $pid)..."
            kill_process_tree "$pid"
        fi
    done < "$PID_LOG"
    
    echo "All experiments have been stopped."
}

# Main execution logic
main() {
    # Create log directory if it doesn't exist
    mkdir -p "$LOG_DIR"
    
    # Initialize shell script log
    local SHELL_LOG="${LOG_NAME_PREFIX}_shell.log"
    
    if [ "$FOREGROUND" = true ]; then
        # Run in foreground
        echo "Starting experiments in foreground..."
        echo "Shell logs: $SHELL_LOG"
        echo "PID log: $PID_LOG"
        echo ""
        
        {
            echo "=== LLM BO Experiments Started at $(date) ==="
            echo "Mode: Foreground"
            echo "LLMs: ${LLMS[*]}"
            echo "Experiments: ${EXPERIMENTS[*]}"
            if [ -n "$MAX_FILES" ]; then
                echo "Max files per experiment: $MAX_FILES"
            fi
            echo "================================================"
            
            run_all_experiments
            
            echo ""
            echo "All experiments started. Monitoring completion..."
            
            # Monitor completion
            while true; do
                if check_experiment_completion; then
                    echo "=== All experiments completed at $(date) ==="
                    break
                else
                    echo "Some experiments still running. Checking again in 30 seconds..."
                    sleep 30
                fi
            done
            
        } | tee "$SHELL_LOG"
        
    else
        # Run in background with nohup
        echo "Starting experiments in background..."
        echo "Shell logs: $SHELL_LOG"
        echo "PID log: $PID_LOG"
        echo "Use 'tail -f $SHELL_LOG' to monitor progress"
        echo "Use './stop_llm_experiments.sh' to stop all experiments"
        
        nohup bash -c "
            {
                echo '=== LLM BO Experiments Started at \$(date) ==='
                echo 'Mode: Background'
                echo 'LLMs: ${LLMS[*]}'
                echo 'Experiments: ${EXPERIMENTS[*]}'
                if [ -n '$MAX_FILES' ]; then
                    echo 'Max files per experiment: $MAX_FILES'
                fi
                echo '================================================'
                
                $(declare -f get_api_key)
                $(declare -f start_single_experiment)
                $(declare -f run_all_experiments)
                $(declare -f check_experiment_completion)
                
                # Set variables for the background context
                LLM_KEY_FILE='$LLM_KEY_FILE'
                LOG_NAME_PREFIX='$LOG_NAME_PREFIX'
                PID_LOG='$PID_LOG'
                MAX_FILES='$MAX_FILES'
                declare -a LLMS=(${LLMS[@]})
                declare -a EXPERIMENTS=(${EXPERIMENTS[@]})
                
                run_all_experiments
                
                echo ''
                echo 'All experiments started. Monitoring completion...'
                
                # Monitor completion
                while true; do
                    if check_experiment_completion; then
                        echo '=== All experiments completed at \$(date) ==='
                        break
                    else
                        echo 'Some experiments still running. Checking again in 60 seconds...'
                        sleep 60
                    fi
                done
                
            }
        " > "$SHELL_LOG" 2>&1 &
        
        # Store the main script PID
        local MAIN_PID=$!
        echo "main_script $MAIN_PID" >> "$PID_LOG"
        echo "Background script PID: $MAIN_PID"
    fi
    
    echo ""
    echo "Experiment management commands:"
    echo "  Monitor logs: tail -f $SHELL_LOG"
    echo "  Stop all: ./stop_llm_experiments.sh"
    echo "  Check status: ps aux | grep 'main.py'"
}

# Run main function
main "$@"
