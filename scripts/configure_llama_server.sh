#!/bin/bash

# llama.cpp Server Configuration Manager
# Interactive configuration tool for llama-server settings

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Get the project root directory
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Configuration file paths
ENV_FILE="${PROJECT_ROOT}/.env"
ENV_EXAMPLE="${PROJECT_ROOT}/.env.example"
CONFIG_DIR="${PROJECT_ROOT}/.llama"
CONFIG_FILE="${CONFIG_DIR}/server.conf"

# Print banner
print_banner() {
    clear
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  llama.cpp Server Configuration Manager"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

# Create config directory
create_config_dir() {
    if [ ! -d "$CONFIG_DIR" ]; then
        mkdir -p "$CONFIG_DIR"
    fi
}

# Load current configuration
load_config() {
    # Load from environment
    export LLAMA_MODEL="${LLAMA_MODEL:-unsloth/Devstral-Small-2-24B-Instruct-2512-GGUF:UD-Q4_K_XL}"
    export LLAMA_HOST="${LLAMA_HOST:-127.0.0.1}"
    export LLAMA_PORT="${LLAMA_PORT:-8080}"
    export LLAMA_CTX_SIZE="${LLAMA_CTX_SIZE:-16384}"
    export LLAMA_GPU_LAYERS="${LLAMA_GPU_LAYERS:-99}"
    export LLAMA_THREADS="${LLAMA_THREADS:--1}"
    export LLAMA_BATCH_SIZE="${LLAMA_BATCH_SIZE:-512}"
    export LLAMA_PARALLEL="${LLAMA_PARALLEL:-4}"
    export LLAMA_LOG_LEVEL="${LLAMA_LOG_LEVEL:-info}"
    
    # Load from config file if exists
    if [ -f "$CONFIG_FILE" ]; then
        source "$CONFIG_FILE"
    fi
}

# Save configuration
save_config() {
    create_config_dir
    
    cat > "$CONFIG_FILE" << EOF
# llama.cpp Server Configuration
# Generated on $(date)

# Model configuration
export LLAMA_MODEL="$LLAMA_MODEL"

# Network configuration
export LLAMA_HOST="$LLAMA_HOST"
export LLAMA_PORT="$LLAMA_PORT"

# Performance configuration
export LLAMA_CTX_SIZE="$LLAMA_CTX_SIZE"
export LLAMA_GPU_LAYERS="$LLAMA_GPU_LAYERS"
export LLAMA_THREADS="$LLAMA_THREADS"
export LLAMA_BATCH_SIZE="$LLAMA_BATCH_SIZE"
export LLAMA_PARALLEL="$LLAMA_PARALLEL"

# Logging configuration
export LLAMA_LOG_LEVEL="$LLAMA_LOG_LEVEL"
EOF
    
    echo -e "${GREEN}✓${NC} Configuration saved to $CONFIG_FILE"
    echo ""
    echo "To use this configuration, add to your shell profile:"
    echo "  ${BLUE}source $CONFIG_FILE${NC}"
}

# Update .env file
update_env_file() {
    if [ ! -f "$ENV_FILE" ]; then
        if [ -f "$ENV_EXAMPLE" ]; then
            cp "$ENV_EXAMPLE" "$ENV_FILE"
            echo -e "${GREEN}✓${NC} Created .env file from .env.example"
        else
            touch "$ENV_FILE"
            echo -e "${GREEN}✓${NC} Created new .env file"
        fi
    fi
    
    # Update or add OPENAI_API_BASE
    if grep -q "^OPENAI_API_BASE=" "$ENV_FILE"; then
        sed -i.bak "s|^OPENAI_API_BASE=.*|OPENAI_API_BASE=http://${LLAMA_HOST}:${LLAMA_PORT}/v1|" "$ENV_FILE"
    else
        echo "OPENAI_API_BASE=http://${LLAMA_HOST}:${LLAMA_PORT}/v1" >> "$ENV_FILE"
    fi
    
    # Update or add OPENAI_API_KEY
    if grep -q "^OPENAI_API_KEY=" "$ENV_FILE"; then
        sed -i.bak "s|^OPENAI_API_KEY=.*|OPENAI_API_KEY=not-needed|" "$ENV_FILE"
    else
        echo "OPENAI_API_KEY=not-needed" >> "$ENV_FILE"
    fi
    
    # Update or add OPENAI_API_MODEL
    if grep -q "^OPENAI_API_MODEL=" "$ENV_FILE"; then
        sed -i.bak "s|^OPENAI_API_MODEL=.*|OPENAI_API_MODEL=devstral|" "$ENV_FILE"
    else
        echo "OPENAI_API_MODEL=devstral" >> "$ENV_FILE"
    fi
    
    # Clean up backup file
    rm -f "${ENV_FILE}.bak"
    
    echo -e "${GREEN}✓${NC} Updated .env file"
}

# Show current configuration
show_config() {
    echo -e "${CYAN}Current Configuration:${NC}"
    echo ""
    echo "Model Settings:"
    echo "  Model:          $LLAMA_MODEL"
    echo ""
    echo "Network Settings:"
    echo "  Host:           $LLAMA_HOST"
    echo "  Port:           $LLAMA_PORT"
    echo ""
    echo "Performance Settings:"
    echo "  Context Size:   $LLAMA_CTX_SIZE tokens"
    echo "  GPU Layers:     $LLAMA_GPU_LAYERS"
    echo "  CPU Threads:    $LLAMA_THREADS"
    echo "  Batch Size:     $LLAMA_BATCH_SIZE"
    echo "  Parallel:       $LLAMA_PARALLEL"
    echo ""
    echo "Logging:"
    echo "  Log Level:      $LLAMA_LOG_LEVEL"
    echo ""
}

# Prompt for input with default
prompt_with_default() {
    local prompt="$1"
    local default="$2"
    local value
    
    read -p "$prompt [$default]: " value
    echo "${value:-$default}"
}

# Configure model
configure_model() {
    echo -e "${CYAN}=== Model Configuration ===${NC}"
    echo ""
    echo "Popular models:"
    echo "  1. Devstral-Small-2-24B (default, 14GB, fast)"
    echo "  2. Qwen2.5-Coder-32B (coding specialist, 20GB)"
    echo "  3. Llama-3.2-3B (small, 2GB, very fast)"
    echo "  4. DeepSeek-Coder-33B (large coding model, 20GB)"
    echo "  5. Custom model path"
    echo ""
    
    local choice
    read -p "Select model [1-5] or Enter for default: " choice
    
    case $choice in
        1|"")
            LLAMA_MODEL="unsloth/Devstral-Small-2-24B-Instruct-2512-GGUF:UD-Q4_K_XL"
            ;;
        2)
            LLAMA_MODEL="unsloth/Qwen2.5-Coder-32B-Instruct-GGUF:Q4_K_M"
            ;;
        3)
            LLAMA_MODEL="unsloth/Llama-3.2-3B-Instruct-GGUF:Q4_K_M"
            ;;
        4)
            LLAMA_MODEL="unsloth/DeepSeek-Coder-33B-Instruct-GGUF:Q4_K_M"
            ;;
        5)
            LLAMA_MODEL=$(prompt_with_default "Enter custom model path or HF repo" "$LLAMA_MODEL")
            ;;
    esac
    
    echo -e "${GREEN}✓${NC} Model: $LLAMA_MODEL"
    echo ""
}

# Configure network
configure_network() {
    echo -e "${CYAN}=== Network Configuration ===${NC}"
    echo ""
    
    LLAMA_HOST=$(prompt_with_default "Host address" "$LLAMA_HOST")
    LLAMA_PORT=$(prompt_with_default "Port number" "$LLAMA_PORT")
    
    echo -e "${GREEN}✓${NC} Network: ${LLAMA_HOST}:${LLAMA_PORT}"
    echo ""
}

# Configure performance
configure_performance() {
    echo -e "${CYAN}=== Performance Configuration ===${NC}"
    echo ""
    
    echo "Context Size (tokens):"
    echo "  4096   - Small, fast, low memory"
    echo "  8192   - Medium (recommended)"
    echo "  16384  - Large, slower, more memory (default)"
    echo "  32768  - Very large, slow, high memory"
    echo ""
    LLAMA_CTX_SIZE=$(prompt_with_default "Context size" "$LLAMA_CTX_SIZE")
    
    echo ""
    echo "GPU Layers:"
    echo "  0      - CPU only"
    echo "  -1/99  - All layers on GPU (default)"
    echo "  N      - Specific number of layers"
    echo ""
    LLAMA_GPU_LAYERS=$(prompt_with_default "GPU layers" "$LLAMA_GPU_LAYERS")
    
    echo ""
    echo "CPU Threads:"
    echo "  -1     - Auto-detect (default)"
    echo "  N      - Specific number"
    echo ""
    LLAMA_THREADS=$(prompt_with_default "CPU threads" "$LLAMA_THREADS")
    
    echo ""
    LLAMA_BATCH_SIZE=$(prompt_with_default "Batch size" "$LLAMA_BATCH_SIZE")
    LLAMA_PARALLEL=$(prompt_with_default "Parallel requests" "$LLAMA_PARALLEL")
    
    echo -e "${GREEN}✓${NC} Performance configured"
    echo ""
}

# Configure logging
configure_logging() {
    echo -e "${CYAN}=== Logging Configuration ===${NC}"
    echo ""
    
    echo "Log levels: debug, info, warning, error"
    LLAMA_LOG_LEVEL=$(prompt_with_default "Log level" "$LLAMA_LOG_LEVEL")
    
    echo -e "${GREEN}✓${NC} Logging: $LLAMA_LOG_LEVEL"
    echo ""
}

# Preset configurations
apply_preset() {
    echo -e "${CYAN}=== Configuration Presets ===${NC}"
    echo ""
    echo "1. Development (fast, low memory)"
    echo "2. Balanced (default)"
    echo "3. Production (high quality)"
    echo "4. Maximum Performance (requires powerful hardware)"
    echo "5. CPU Only (no GPU)"
    echo ""
    
    local preset
    read -p "Select preset [1-5] or Enter to skip: " preset
    
    case $preset in
        1)
            echo "Applying Development preset..."
            LLAMA_MODEL="unsloth/Llama-3.2-3B-Instruct-GGUF:Q4_K_M"
            LLAMA_CTX_SIZE=4096
            LLAMA_GPU_LAYERS=99
            LLAMA_THREADS=-1
            LLAMA_BATCH_SIZE=256
            LLAMA_PARALLEL=2
            ;;
        2)
            echo "Applying Balanced preset..."
            LLAMA_MODEL="unsloth/Devstral-Small-2-24B-Instruct-2512-GGUF:UD-Q4_K_XL"
            LLAMA_CTX_SIZE=16384
            LLAMA_GPU_LAYERS=99
            LLAMA_THREADS=-1
            LLAMA_BATCH_SIZE=512
            LLAMA_PARALLEL=4
            ;;
        3)
            echo "Applying Production preset..."
            LLAMA_MODEL="unsloth/Qwen2.5-Coder-32B-Instruct-GGUF:Q4_K_M"
            LLAMA_CTX_SIZE=16384
            LLAMA_GPU_LAYERS=99
            LLAMA_THREADS=-1
            LLAMA_BATCH_SIZE=512
            LLAMA_PARALLEL=8
            ;;
        4)
            echo "Applying Maximum Performance preset..."
            LLAMA_MODEL="unsloth/Qwen2.5-Coder-32B-Instruct-GGUF:Q8_0"
            LLAMA_CTX_SIZE=32768
            LLAMA_GPU_LAYERS=99
            LLAMA_THREADS=-1
            LLAMA_BATCH_SIZE=1024
            LLAMA_PARALLEL=8
            ;;
        5)
            echo "Applying CPU Only preset..."
            LLAMA_MODEL="unsloth/Llama-3.2-3B-Instruct-GGUF:Q4_K_M"
            LLAMA_CTX_SIZE=4096
            LLAMA_GPU_LAYERS=0
            LLAMA_THREADS=8
            LLAMA_BATCH_SIZE=256
            LLAMA_PARALLEL=2
            ;;
        "")
            echo "Skipping preset..."
            return
            ;;
    esac
    
    echo -e "${GREEN}✓${NC} Preset applied"
    echo ""
}

# Interactive configuration
interactive_config() {
    echo "Would you like to:"
    echo "  1. Apply a preset configuration"
    echo "  2. Configure manually"
    echo "  3. View current configuration and exit"
    echo ""
    
    local choice
    read -p "Select option [1-3]: " choice
    
    case $choice in
        1)
            apply_preset
            ;;
        2)
            configure_model
            configure_network
            configure_performance
            configure_logging
            ;;
        3)
            show_config
            exit 0
            ;;
        *)
            echo "Invalid option"
            exit 1
            ;;
    esac
}

# Verify configuration
verify_config() {
    echo -e "${CYAN}=== Verification ===${NC}"
    echo ""
    
    # Check if llama-server is installed
    if command -v llama-server &> /dev/null; then
        echo -e "${GREEN}✓${NC} llama-server is installed"
    else
        echo -e "${YELLOW}⚠️  llama-server not found${NC}"
        echo "  Install with: brew install llama.cpp"
    fi
    
    # Check port availability
    if lsof -Pi :$LLAMA_PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Port $LLAMA_PORT is already in use${NC}"
    else
        echo -e "${GREEN}✓${NC} Port $LLAMA_PORT is available"
    fi
    
    # Estimate memory requirements
    local ctx_mem=$((LLAMA_CTX_SIZE / 1024))
    echo ""
    echo "Estimated memory usage: ~${ctx_mem}GB + model size"
    
    echo ""
}

# Main menu
main_menu() {
    print_banner
    load_config
    show_config
    
    echo -e "${YELLOW}Press Enter to configure or Ctrl+C to exit${NC}"
    read
    
    interactive_config
    
    echo ""
    show_config
    
    verify_config
    
    echo ""
    read -p "Save this configuration? (y/N): " -n 1 -r
    echo
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        save_config
        update_env_file
        
        echo ""
        echo -e "${GREEN}Configuration saved successfully!${NC}"
        echo ""
        echo "Next steps:"
        echo "  1. Source the configuration:"
        echo "     ${BLUE}source $CONFIG_FILE${NC}"
        echo ""
        echo "  2. Start the server:"
        echo "     ${BLUE}./scripts/start_llama_server.sh${NC}"
        echo ""
    else
        echo "Configuration not saved"
    fi
}

# Export configuration
export_config() {
    echo "# llama.cpp Environment Variables"
    echo "# Add to your ~/.bashrc or ~/.zshrc"
    echo ""
    echo "export LLAMA_MODEL=\"$LLAMA_MODEL\""
    echo "export LLAMA_HOST=\"$LLAMA_HOST\""
    echo "export LLAMA_PORT=\"$LLAMA_PORT\""
    echo "export LLAMA_CTX_SIZE=\"$LLAMA_CTX_SIZE\""
    echo "export LLAMA_GPU_LAYERS=\"$LLAMA_GPU_LAYERS\""
    echo "export LLAMA_THREADS=\"$LLAMA_THREADS\""
    echo "export LLAMA_BATCH_SIZE=\"$LLAMA_BATCH_SIZE\""
    echo "export LLAMA_PARALLEL=\"$LLAMA_PARALLEL\""
    echo "export LLAMA_LOG_LEVEL=\"$LLAMA_LOG_LEVEL\""
}

# Parse command line arguments
if [ "$1" = "--export" ]; then
    load_config
    export_config
    exit 0
elif [ "$1" = "--show" ]; then
    load_config
    show_config
    exit 0
elif [ "$1" = "--help" ]; then
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --show      Show current configuration"
    echo "  --export    Export configuration as environment variables"
    echo "  --help      Show this help message"
    echo ""
    echo "Without options, runs interactive configuration wizard"
    exit 0
fi

# Run main menu
main_menu
