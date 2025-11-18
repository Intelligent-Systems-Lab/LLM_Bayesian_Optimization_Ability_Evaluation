# llm="qwen"
# exp="100"
# MAX_FILES="2"



# # Set timestamp and log directory
# LLM_CONFIG="qwen"
# TIMESTAMP=$(date '+%m%d%H%M%S')
# LOG_DIR="$HOME/jacklab/flowerHome/LLM_Bayesian_Optimization_Ability_Evaluation/src/llm_bo_ability_eval"
# LOG_NAME_PREFIX="$LOG_DIR/morph_floptuna_${TIMESTAMP}_${LLM_CONFIG}"

# # Log file to store PIDs
# PID_LOG="${LOG_NAME_PREFIX}_pids.log"

# # Configuration
# LLM_KEY_FILE="llm_key_config.txt"

# # Function to get API key for a given LLM
# get_api_key() {
#     local llm=$1
#     if [ ! -f "$LLM_KEY_FILE" ]; then
#         echo "Error: Config file $LLM_KEY_FILE not found!"
#         exit 1
#     fi
#     local key=$(grep "^${llm}:" "$LLM_KEY_FILE" | cut -d':' -f2)
#     if [ -z "$key" ]; then
#         echo "Error: No API key found for $llm"
#         exit 1
#     fi
#     echo "$key"
# }

# # Create log file for this experiment
# LOG_FILE="${LOG_NAME_PREFIX}_${llm}_${exp}problems.log"

# # Get API key for this LLM
# api_key=$(get_api_key "$llm")
# export OPENAI_API_KEY="$api_key"

# # Build command
# cmd="python main.py -l $llm -e $exp -p $PROBLEM_PATH"
# if [ -n "$MAX_FILES" ]; then
#     cmd="$cmd -m $MAX_FILES"
# fi

# nohup $cmd
echo "start!!!"
python main.py -l qwen -e 24 -p problem_set/24problems_tpe -m 2

# # Start experiment in background with nohup
# nohup $cmd > "$LOG_FILE" 2>&1 &

# PID=$!
# echo "Started experiment #${exp_number} with PID: ${PID} (log: ${LOG_FILE})"
# echo "${llm}_${exp}problems ${PID}" >> "$PID_LOG"
