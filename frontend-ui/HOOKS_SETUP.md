# 🔧 Git Hooks Setup for Automatic Version Updates

## Problem
Git hooks are not synchronized between developers through the git repository. Each developer must install the pre-commit hook locally.

## Solution

### Automatic Installation (Recommended)
```bash
# From frontend-ui directory
npm run setup-hooks
```

### Manual Installation
```bash
# From git repository root
./frontend-ui/scripts/setup-hooks.sh
```

## What does the hook do?
- On each commit, checks if there are changes in the `frontend-ui/` directory
- If changes exist, automatically increments the patch version in `package.json`
- Adds the updated `package.json` to the commit
- Displays version update in console

## Version Format
- Format: `major.minor.patch` (e.g., `0.0.20`)
- Auto-increments: **patch** version only
- Manual updates: major and minor versions

## Testing the Setup
After installation, make a test commit:
```bash
cd frontend-ui
echo "// test" >> src/app/app.component.ts
git add src/app/app.component.ts
git commit -m "test: version bump"
# Version should be automatically updated (0.0.20 → 0.0.21)
```

## Troubleshooting

### Hook doesn't work
1. Check permissions: 
   ```bash
   ls -la .git/hooks/pre-commit
   ```
2. Ensure you're in the git repository root when installing
3. Reinstall the hook:
   ```bash
   cd frontend-ui
   npm run setup-hooks
   ```

### Version not updating
- Make sure you have changes in `frontend-ui/` directory
- Check that `package.json` is not in `.gitignore`
- Verify hook is executable: `chmod +x .git/hooks/pre-commit`

### macOS vs Linux
The script automatically detects the OS:
- **macOS**: Uses `sed -i ''`
- **Linux**: Uses `sed -i`

## How it Works

1. **Pre-commit trigger**: Git runs `.git/hooks/pre-commit` before commit
2. **Change detection**: Checks if any `frontend-ui/` files are staged
3. **Version extraction**: Reads current version from `package.json`
4. **Increment**: Adds +1 to patch number
5. **Update**: Writes new version to `package.json`
6. **Stage**: Adds updated `package.json` to the commit

## Example
```bash
# Before commit
"version": "0.0.20"

# After commit with frontend changes
"version": "0.0.21"

# Console output:
🔄 Updating frontend version...
✅ Version updated: 0.0.20 → 0.0.21
```

## Uninstalling
To remove the hook:
```bash
rm .git/hooks/pre-commit
```

## Notes
- Only affects commits with `frontend-ui/` changes
- Backend-only commits don't trigger version updates
- Hook runs locally, not on GitHub/remote
- Each developer must install the hook
