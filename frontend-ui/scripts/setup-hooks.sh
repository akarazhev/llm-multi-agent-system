#!/bin/bash

# Script to install pre-commit hook for automatic version updates
# Run from git repository root

echo "🔧 Installing pre-commit hook for automatic version updates..."

# Create pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash

# Check if there are changes in frontend-ui directory
if git diff --cached --name-only | grep -q "frontend-ui/"; then
    echo "🔄 Updating frontend version..."
    cd frontend-ui
    
    # Get current version
    current_version=$(grep '"version"' package.json | sed 's/.*"version": "\([^"]*\)".*/\1/')
    
    # Increment patch version
    IFS='.' read -ra VERSION_PARTS <<< "$current_version"
    major=${VERSION_PARTS[0]}
    minor=${VERSION_PARTS[1]}
    patch=${VERSION_PARTS[2]}
    new_patch=$((patch + 1))
    new_version="$major.$minor.$new_patch"
    
    # Update package.json (macOS compatible)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s/\"version\": \"$current_version\"/\"version\": \"$new_version\"/" package.json
    else
        # Linux
        sed -i "s/\"version\": \"$current_version\"/\"version\": \"$new_version\"/" package.json
    fi
    
    cd ..
    git add frontend-ui/package.json
    echo "✅ Version updated: $current_version → $new_version"
fi
EOF

# Make hook executable
chmod +x .git/hooks/pre-commit

echo "✅ Pre-commit hook installed successfully!"
echo "📝 Version will be automatically incremented on each commit with frontend changes"
echo ""
echo "Test the hook with:"
echo "  cd frontend-ui"
echo "  echo '// test' >> src/app/app.component.ts"
echo "  git add src/app/app.component.ts"
echo "  git commit -m 'test: version bump'"
