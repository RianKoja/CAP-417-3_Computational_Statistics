#!/bin/bash
# Runs both agent solutions sequentially and then the benchmark
set -e
echo "Running Claude Code solution..."
cd claude-code && python solution.py && cd ..

echo "Running Gemini CLI solution..."
cd gemini-cli  && python solution.py && cd ..

echo "Running benchmark analysis..."
python benchmark/run_benchmark.py
