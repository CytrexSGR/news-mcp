#!/bin/bash

# Start Content Generator Worker
# Processes pending content generation jobs and creates briefings

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR" || exit 1

echo "Starting Content Generator Worker..."

# Activate virtual environment
source venv/bin/activate

# Set environment variables
export PYTHONPATH="${PROJECT_DIR}"
export CONTENT_WORKER_SLEEP_INTERVAL="${CONTENT_WORKER_SLEEP_INTERVAL:-5.0}"
export CONTENT_WORKER_MAX_JOBS="${CONTENT_WORKER_MAX_JOBS:-5}"
export CONTENT_MAX_COST_PER_JOB="${CONTENT_MAX_COST_PER_JOB:-0.50}"

# Load environment variables from .env file (only simple key=value pairs)
if [ -f "${PROJECT_DIR}/.env" ]; then
    set -a
    source "${PROJECT_DIR}/.env"
    set +a
fi

# Check for OpenAI API key
if [ -z "$OPENAI_API_KEY" ]; then
    echo "Error: OPENAI_API_KEY environment variable not set"
    exit 1
fi

# Create logs and pids directories if they don't exist
mkdir -p logs pids

# Start worker in background
nohup python3 app/worker/content_generator_worker.py > logs/content-worker.log 2>&1 &
WORKER_PID=$!

# Store PID
echo $WORKER_PID > pids/content-worker.pid

echo -e "\033[0;32m✓ Content Generator Worker started successfully!\033[0m"
echo "PID: $WORKER_PID"
echo "Logs: $PROJECT_DIR/logs/content-worker.log"
echo ""
echo "Monitor: tail -f logs/content-worker.log"
echo "Stop: kill $WORKER_PID"
