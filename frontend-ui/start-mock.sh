#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║        🎭  LLM Multi-Agent UI - MOCK MODE  🎭            ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check if we're in the frontend-ui directory
if [ ! -f "package.json" ]; then
    echo -e "${YELLOW}⚠️  Not in frontend-ui directory, changing...${NC}"
    cd "$(dirname "$0")" || exit 1
fi

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}📦 Installing dependencies...${NC}"
    npm install
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ npm install failed${NC}"
        exit 1
    fi
fi

echo -e "${BLUE}🚀 Starting development server in MOCK mode...${NC}"
echo ""
echo -e "${GREEN}✨ Features:${NC}"
echo "   • No backend required"
echo "   • Pre-populated with test data"
echo "   • 5 AI agents with different statuses"
echo "   • 6 sample workflows"
echo "   • Auto-opens browser at http://localhost:4200"
echo ""
echo -e "${BLUE}📊 Mock Data:${NC}"
echo "   • Business Analyst (IDLE)"
echo "   • Developer (WORKING)"
echo "   • QA Engineer (COMPLETED)"
echo "   • DevOps Engineer (WORKING)"
echo "   • Technical Writer (IDLE)"
echo ""
echo -e "${BLUE}🎯 Workflows:${NC}"
echo "   • Feature Development (RUNNING)"
echo "   • Bug Fix (COMPLETED)"
echo "   • Infrastructure Setup (COMPLETED)"
echo "   • Documentation (COMPLETED)"
echo "   • Chat Feature (FAILED)"
echo "   • Performance Analysis (COMPLETED)"
echo ""
echo -e "${YELLOW}⏳ Starting server... This may take a minute...${NC}"
echo ""

# Start the development server with mock configuration
npm run start:mock

# If the server stops, show message
echo ""
echo -e "${YELLOW}👋 Mock server stopped${NC}"
