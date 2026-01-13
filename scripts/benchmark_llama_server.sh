#!/bin/bash

# llama.cpp Server Benchmark Script
# Performance testing and optimization tool

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Get the project root directory
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Configuration
HOST="${LLAMA_HOST:-127.0.0.1}"
PORT="${LLAMA_PORT:-8080}"
API_URL="http://${HOST}:${PORT}/v1/chat/completions"
RESULTS_DIR="${PROJECT_ROOT}/logs/benchmark"
RESULTS_FILE="${RESULTS_DIR}/results_$(date +%Y%m%d_%H%M%S).json"

# Test configurations
TEST_PROMPTS=(
    "Hello"
    "Write a Python function to calculate factorial"
    "Explain quantum computing in simple terms"
)
TEST_TOKENS=(10 50 100 200 500)
TEST_ITERATIONS=5
WARMUP_REQUESTS=2

# Print banner
print_banner() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  llama.cpp Server Benchmark"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

# Create results directory
create_results_dir() {
    if [ ! -d "$RESULTS_DIR" ]; then
        mkdir -p "$RESULTS_DIR"
    fi
}

# Check server status
check_server() {
    echo -e "${CYAN}Checking server status...${NC}"
    
    if ! curl -s -f --max-time 5 "http://${HOST}:${PORT}/health" > /dev/null 2>&1; then
        echo -e "${RED}✗ Server is not responding${NC}"
        echo ""
        echo "Start the server with:"
        echo "  ${BLUE}./scripts/start_llama_server.sh${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✓${NC} Server is running"
    echo ""
}

# Get server info
get_server_info() {
    echo -e "${CYAN}Server Information:${NC}"
    
    # Get process info
    local pids=$(pgrep -f "llama-server" 2>/dev/null || echo "")
    if [ -n "$pids" ]; then
        for pid in $pids; do
            if kill -0 $pid 2>/dev/null; then
                local mem=$(ps -p $pid -o rss= 2>/dev/null | awk '{print int($1/1024)}' || echo "0")
                echo "  Memory: ${mem}MB"
            fi
        done
    fi
    
    # Get system info
    if command -v sysctl &> /dev/null; then
        local cpu_brand=$(sysctl -n machdep.cpu.brand_string 2>/dev/null || echo "Unknown")
        local cpu_cores=$(sysctl -n hw.ncpu 2>/dev/null || echo "Unknown")
        echo "  CPU: $cpu_brand"
        echo "  Cores: $cpu_cores"
    fi
    
    echo ""
}

# Warmup server
warmup() {
    echo -e "${CYAN}Warming up server...${NC}"
    
    for i in $(seq 1 $WARMUP_REQUESTS); do
        local request="{
            \"model\": \"devstral\",
            \"messages\": [{\"role\": \"user\", \"content\": \"test\"}],
            \"max_tokens\": 10
        }"
        
        curl -s -f --max-time 30 \
            -H "Content-Type: application/json" \
            -d "$request" \
            "$API_URL" > /dev/null 2>&1 || true
        
        echo -n "."
    done
    
    echo ""
    echo -e "${GREEN}✓${NC} Warmup complete"
    echo ""
}

# Run single test
run_test() {
    local prompt="$1"
    local max_tokens="$2"
    
    local request="{
        \"model\": \"devstral\",
        \"messages\": [{\"role\": \"user\", \"content\": \"$prompt\"}],
        \"max_tokens\": $max_tokens,
        \"temperature\": 0.7
    }"
    
    # Measure time (use seconds * 1000 for milliseconds, as macOS date doesn't support %N)
    # #region agent log
    local start=$(($(date +%s) * 1000))
    echo "{\"sessionId\":\"debug-session\",\"runId\":\"post-fix\",\"hypothesisId\":\"A\",\"location\":\"benchmark_llama_server.sh:134\",\"message\":\"Time measurement start\",\"data\":{\"start\":\"$start\",\"is_numeric\":true},\"timestamp\":$(date +%s)000}" >> /Users/andrey.karazhev/Developer/spg/llm-multi-agent-system/.cursor/debug.log
    # #endregion
    local response=$(curl -s -f --max-time 60 \
        -H "Content-Type: application/json" \
        -d "$request" \
        "$API_URL" 2>/dev/null || echo "")
    # #region agent log
    echo "{\"sessionId\":\"debug-session\",\"runId\":\"post-fix\",\"hypothesisId\":\"E\",\"location\":\"benchmark_llama_server.sh:138\",\"message\":\"API response received\",\"data\":{\"response_length\":${#response},\"response_preview\":\"${response:0:100}\"},\"timestamp\":$(date +%s)000}" >> /Users/andrey.karazhev/Developer/spg/llm-multi-agent-system/.cursor/debug.log
    # #endregion
    local end=$(($(date +%s) * 1000))
    # #region agent log
    echo "{\"sessionId\":\"debug-session\",\"runId\":\"post-fix\",\"hypothesisId\":\"A\",\"location\":\"benchmark_llama_server.sh:141\",\"message\":\"Time measurement end\",\"data\":{\"start\":\"$start\",\"end\":\"$end\",\"calculation_result\":$((end - start))},\"timestamp\":$(date +%s)000}" >> /Users/andrey.karazhev/Developer/spg/llm-multi-agent-system/.cursor/debug.log
    # #endregion
    
    local latency=$((end - start))
    # #region agent log
    echo "{\"sessionId\":\"debug-session\",\"runId\":\"post-fix\",\"hypothesisId\":\"B\",\"location\":\"benchmark_llama_server.sh:145\",\"message\":\"Latency calculated\",\"data\":{\"latency\":$latency,\"is_numeric\":true},\"timestamp\":$(date +%s)000}" >> /Users/andrey.karazhev/Developer/spg/llm-multi-agent-system/.cursor/debug.log
    # #endregion
    
    # Parse response
    if [ -z "$response" ] || echo "$response" | grep -q '"error"'; then
        echo "ERROR"
        return 1
    fi
    
    # Extract token counts if available
    local prompt_tokens=0
    local completion_tokens=0
    local total_tokens=0
    
    if command -v jq &> /dev/null; then
        prompt_tokens=$(echo "$response" | jq -r '.usage.prompt_tokens // 0' 2>/dev/null)
        completion_tokens=$(echo "$response" | jq -r '.usage.completion_tokens // 0' 2>/dev/null)
        total_tokens=$(echo "$response" | jq -r '.usage.total_tokens // 0' 2>/dev/null)
        # #region agent log
        echo "{\"sessionId\":\"debug-session\",\"runId\":\"initial\",\"hypothesisId\":\"D\",\"location\":\"benchmark_llama_server.sh:158\",\"message\":\"Token counts parsed\",\"data\":{\"prompt_tokens\":\"$prompt_tokens\",\"completion_tokens\":\"$completion_tokens\",\"total_tokens\":\"$total_tokens\"},\"timestamp\":$(date +%s)000}" >> /Users/andrey.karazhev/Developer/spg/llm-multi-agent-system/.cursor/debug.log
        # #endregion
    fi
    
    # Calculate tokens per second
    local tokens_per_sec=0
    # #region agent log
    echo "{\"sessionId\":\"debug-session\",\"runId\":\"initial\",\"hypothesisId\":\"C\",\"location\":\"benchmark_llama_server.sh:162\",\"message\":\"Before tokens_per_sec calculation\",\"data\":{\"latency\":\"$latency\",\"completion_tokens\":\"$completion_tokens\",\"latency_gt_0\":\"$([ -n \"$latency\" ] && [ \"$latency\" -gt 0 ] 2>/dev/null && echo true || echo false)\",\"completion_gt_0\":\"$([ -n \"$completion_tokens\" ] && [ \"$completion_tokens\" -gt 0 ] 2>/dev/null && echo true || echo false)\"},\"timestamp\":$(date +%s)000}" >> /Users/andrey.karazhev/Developer/spg/llm-multi-agent-system/.cursor/debug.log
    # #endregion
    if [ -n "$latency" ] && [ "$latency" -gt 0 ] 2>/dev/null && [ -n "$completion_tokens" ] && [ "$completion_tokens" -gt 0 ] 2>/dev/null; then
        tokens_per_sec=$(awk "BEGIN {printf \"%.2f\", $completion_tokens / ($latency / 1000)}")
    fi
    
    # Output results
    echo "$latency|$prompt_tokens|$completion_tokens|$total_tokens|$tokens_per_sec"
    return 0
}

# Run latency test
test_latency() {
    echo -e "${MAGENTA}=== Latency Test ===${NC}"
    echo ""
    echo "Testing response time with different prompt sizes..."
    echo ""
    
    printf "%-50s %-15s %-15s %-15s\n" "Prompt" "Min (ms)" "Avg (ms)" "Max (ms)"
    echo "────────────────────────────────────────────────────────────────────────────────"
    
    for prompt in "${TEST_PROMPTS[@]}"; do
        local latencies=()
        local sum=0
        local min=999999
        local max=0
        
        for i in $(seq 1 $TEST_ITERATIONS); do
            local result=$(run_test "$prompt" 50)
            
            if [ "$result" = "ERROR" ]; then
                echo -e "${RED}✗ Test failed${NC}"
                continue
            fi
            
            local latency=$(echo "$result" | cut -d'|' -f1)
            # #region agent log
            echo "{\"sessionId\":\"debug-session\",\"runId\":\"initial\",\"hypothesisId\":\"B\",\"location\":\"benchmark_llama_server.sh:195\",\"message\":\"Latency from result\",\"data\":{\"result\":\"$result\",\"latency\":\"$latency\",\"is_empty\":\"$([ -z \"$latency\" ] && echo true || echo false)\"},\"timestamp\":$(date +%s)000}" >> /Users/andrey.karazhev/Developer/spg/llm-multi-agent-system/.cursor/debug.log
            # #endregion
            latencies+=($latency)
            sum=$((sum + latency))
            
            if [ -n "$latency" ] && [ "$latency" -lt "$min" ] 2>/dev/null; then
                min=$latency
            fi
            if [ -n "$latency" ] && [ "$latency" -gt "$max" ] 2>/dev/null; then
                max=$latency
            fi
            
            echo -n "."
        done
        
        echo -ne "\r"
        
        local avg=$((sum / TEST_ITERATIONS))
        local prompt_short="${prompt:0:45}"
        [ ${#prompt} -gt 45 ] && prompt_short="${prompt_short}..."
        
        printf "%-50s %-15s %-15s %-15s\n" "$prompt_short" "$min" "$avg" "$max"
    done
    
    echo ""
}

# Run throughput test
test_throughput() {
    echo -e "${MAGENTA}=== Throughput Test ===${NC}"
    echo ""
    echo "Testing tokens per second with different response lengths..."
    echo ""
    
    printf "%-15s %-15s %-15s %-20s\n" "Max Tokens" "Avg Latency" "Tokens/sec" "Time/Token"
    echo "────────────────────────────────────────────────────────────────────────────────"
    
    for max_tokens in "${TEST_TOKENS[@]}"; do
        local total_latency=0
        local total_tps=0
        local successful=0
        
        for i in $(seq 1 $TEST_ITERATIONS); do
            local result=$(run_test "Write a story" "$max_tokens")
            
            if [ "$result" = "ERROR" ]; then
                continue
            fi
            
            local latency=$(echo "$result" | cut -d'|' -f1)
            local tps=$(echo "$result" | cut -d'|' -f5)
            # #region agent log
            echo "{\"sessionId\":\"debug-session\",\"runId\":\"initial\",\"hypothesisId\":\"C\",\"location\":\"benchmark_llama_server.sh:244\",\"message\":\"Throughput values\",\"data\":{\"latency\":\"$latency\",\"tps\":\"$tps\",\"total_tps\":\"$total_tps\"},\"timestamp\":$(date +%s)000}" >> /Users/andrey.karazhev/Developer/spg/llm-multi-agent-system/.cursor/debug.log
            # #endregion
            
            total_latency=$((total_latency + latency))
            total_tps=$(awk "BEGIN {print $total_tps + $tps}")
            successful=$((successful + 1))
            
            echo -n "."
        done
        
        echo -ne "\r"
        
        if [ "$successful" -gt 0 ]; then
            local avg_latency=$((total_latency / successful))
            local avg_tps=$(awk "BEGIN {printf \"%.2f\", $total_tps / $successful}")
            local time_per_token=$(awk "BEGIN {printf \"%.0f\", 1000 / $avg_tps}")
            
            printf "%-15s %-15s %-15s %-20s\n" \
                "$max_tokens" \
                "${avg_latency}ms" \
                "$avg_tps" \
                "${time_per_token}ms"
        else
            echo -e "${RED}✗ All tests failed for $max_tokens tokens${NC}"
        fi
    done
    
    echo ""
}

# Run concurrent test
test_concurrent() {
    echo -e "${MAGENTA}=== Concurrent Requests Test ===${NC}"
    echo ""
    echo "Testing server with multiple concurrent requests..."
    echo ""
    
    local concurrent_levels=(1 2 4 8)
    
    printf "%-15s %-15s %-15s %-15s\n" "Concurrent" "Total Time" "Avg/Request" "Requests/sec"
    echo "────────────────────────────────────────────────────────────────────────────────"
    
    for concurrency in "${concurrent_levels[@]}"; do
        local start=$(($(date +%s) * 1000))
        local pids=()
        
        # Launch concurrent requests
        for i in $(seq 1 $concurrency); do
            (run_test "Test concurrent" 20 > /dev/null 2>&1) &
            pids+=($!)
        done
        
        # Wait for all to complete
        for pid in "${pids[@]}"; do
            wait $pid 2>/dev/null || true
        done
        
        local end=$(($(date +%s) * 1000))
        local total_time=$((end - start))
        local avg_time=$((total_time / concurrency))
        local req_per_sec=$(awk "BEGIN {printf \"%.2f\", $concurrency / ($total_time / 1000)}")
        
        printf "%-15s %-15s %-15s %-15s\n" \
            "$concurrency" \
            "${total_time}ms" \
            "${avg_time}ms" \
            "$req_per_sec"
    done
    
    echo ""
}

# Run stress test
test_stress() {
    echo -e "${MAGENTA}=== Stress Test ===${NC}"
    echo ""
    echo "Running continuous load for 30 seconds..."
    echo ""
    
    local duration=30
    local start_time=$(date +%s)
    local end_time=$((start_time + duration))
    local request_count=0
    local success_count=0
    local error_count=0
    local total_latency=0
    
    while [ $(date +%s) -lt $end_time ]; do
        local result=$(run_test "Stress test" 20 2>/dev/null || echo "ERROR")
        
        request_count=$((request_count + 1))
        
        if [ "$result" = "ERROR" ]; then
            error_count=$((error_count + 1))
        else
            success_count=$((success_count + 1))
            local latency=$(echo "$result" | cut -d'|' -f1)
            total_latency=$((total_latency + latency))
        fi
        
        # Progress indicator
        local elapsed=$(($(date +%s) - start_time))
        local progress=$((elapsed * 100 / duration))
        echo -ne "\rProgress: ${progress}% | Requests: $request_count | Success: $success_count | Errors: $error_count"
    done
    
    echo ""
    echo ""
    
    echo "Results:"
    echo "  Total Requests:    $request_count"
    echo "  Successful:        $success_count"
    echo "  Errors:            $error_count"
    
    if [ "$success_count" -gt 0 ]; then
        local avg_latency=$((total_latency / success_count))
        local success_rate=$(awk "BEGIN {printf \"%.2f\", $success_count * 100 / $request_count}")
        local req_per_sec=$(awk "BEGIN {printf \"%.2f\", $request_count / $duration}")
        
        echo "  Success Rate:      ${success_rate}%"
        echo "  Avg Latency:       ${avg_latency}ms"
        echo "  Requests/sec:      $req_per_sec"
    fi
    
    echo ""
}

# Save results
save_results() {
    local results="{
        \"timestamp\": \"$(date -u +"%Y-%m-%dT%H:%M:%SZ")\",
        \"server\": {
            \"host\": \"$HOST\",
            \"port\": \"$PORT\"
        },
        \"configuration\": {
            \"test_iterations\": $TEST_ITERATIONS,
            \"warmup_requests\": $WARMUP_REQUESTS
        }
    }"
    
    echo "$results" > "$RESULTS_FILE"
    echo -e "${GREEN}✓${NC} Results saved to: $RESULTS_FILE"
}

# Print summary
print_summary() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  Benchmark Complete"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "Recommendations:"
    echo ""
    
    # Add some basic recommendations based on results
    echo "  • Monitor server performance during normal operation"
    echo "  • Adjust LLAMA_CTX_SIZE if running out of memory"
    echo "  • Increase LLAMA_GPU_LAYERS for better performance"
    echo "  • Use LLAMA_PARALLEL to handle concurrent requests"
    echo ""
    echo "For detailed monitoring, use:"
    echo "  ${BLUE}./scripts/monitor_llama_server.sh${NC}"
    echo ""
}

# Main execution
main() {
    # Parse arguments
    local run_all=true
    local run_latency=false
    local run_throughput=false
    local run_concurrent=false
    local run_stress=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --latency)
                run_all=false
                run_latency=true
                shift
                ;;
            --throughput)
                run_all=false
                run_throughput=true
                shift
                ;;
            --concurrent)
                run_all=false
                run_concurrent=true
                shift
                ;;
            --stress)
                run_all=false
                run_stress=true
                shift
                ;;
            -h|--help)
                echo "Usage: $0 [OPTIONS]"
                echo ""
                echo "Options:"
                echo "  --latency      Run only latency tests"
                echo "  --throughput   Run only throughput tests"
                echo "  --concurrent   Run only concurrent tests"
                echo "  --stress       Run only stress tests"
                echo "  -h, --help     Show this help message"
                echo ""
                echo "Without options, runs all tests"
                exit 0
                ;;
            *)
                echo "Unknown option: $1"
                echo "Use -h for help"
                exit 1
                ;;
        esac
    done
    
    print_banner
    create_results_dir
    check_server
    get_server_info
    warmup
    
    if $run_all || $run_latency; then
        test_latency
    fi
    
    if $run_all || $run_throughput; then
        test_throughput
    fi
    
    if $run_all || $run_concurrent; then
        test_concurrent
    fi
    
    if $run_all || $run_stress; then
        test_stress
    fi
    
    save_results
    print_summary
}

# Run main function
main "$@"
