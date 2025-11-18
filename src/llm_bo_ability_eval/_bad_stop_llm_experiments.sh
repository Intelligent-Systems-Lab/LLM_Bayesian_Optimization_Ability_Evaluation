#!/bin/bash

# Script to stop all running LLM experiments
# Usage: ./stop_llm_experiments.sh [-n|--number N]

# Default to most recent (1)
LOG_NUMBER=1

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -n|--number)
            LOG_NUMBER="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 [-n|--number N]"
            echo "  -n, --number    Stop Nth most recent experiment set (default: 1 for latest)"
            echo "  -h, --help      Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option $1"
            echo "Usage: $0 [-n|--number N] (where N=1 for latest, 2 for second latest, etc.)"
            exit 1
            ;;
    esac
done

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

# Get the Nth most recent PID log file
LATEST_PID_LOG=$(ls -t llm_bo_experiments_*_pids.log 2>/dev/null | sed -n "${LOG_NUMBER}p")

if [ -z "$LATEST_PID_LOG" ]; then
    echo "No LLM experiment PID log found for position ${LOG_NUMBER}."
    echo "Available log files:"
    ls -lt llm_bo_experiments_*_pids.log 2>/dev/null | nl
    if [ $? -ne 0 ]; then
        echo "No experiment log files found."
    fi
    exit 1
fi

echo "Found PID log #${LOG_NUMBER}: $LATEST_PID_LOG"
echo "Stopping all experiments in this log..."

# Read and kill each process
STOPPED_COUNT=0
while read -r EXP_NAME PID; do
    if [ -n "$EXP_NAME" ] && [ -n "$PID" ]; then
        echo "Stopping $EXP_NAME (PID: $PID)..."
        kill_process_tree "$PID"
        STOPPED_COUNT=$((STOPPED_COUNT + 1))
    fi
done < "$LATEST_PID_LOG"

echo "Stopped $STOPPED_COUNT experiments."
echo "All experiments from $LATEST_PID_LOG have been stopped."
