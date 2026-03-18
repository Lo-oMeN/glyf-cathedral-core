#!/bin/bash
# Push all GLYF repos to GitHub
# Usage: ./push-all-repos.sh <your_github_token>

TOKEN="${1:-$GITHUB_TOKEN}"

if [ -z "$TOKEN" ]; then
    echo "Error: GitHub token required"
    echo "Usage: ./push-all-repos.sh ghp_xxxxxxxxxxxx"
    exit 1
fi

cd /root/.openclaw/workspace

# Repos to push
declare -A REPOS=(
    ["glyf-cathedral-core"]="Φ-radial lattice optimizer"
    ["glyf-visualizer"]="Manifold music visualizer"
    ["trinity-v6-repo"]="AI substrate"
    ["phi-modality-stack-repo"]="Integration layer"
    ["glyf-research-repo"]="Research documentation"
    ["loom-visualizer-repo"]="Python radial loom"
    ["geo-ai-chronicler"]="Persistent R&D agent"
)

echo "=== Pushing GLYF Cathedral Repos to GitHub ==="
echo ""

for repo in "${!REPOS[@]}"; do
    desc="${REPOS[$repo]}"
    echo "--- Pushing $repo ($desc) ---"
    
    cd "/root/.openclaw/workspace/$repo"
    
    # Check if remote exists
    if git remote get-url origin 2>/dev/null | grep -q github; then
        echo "Remote already configured"
    else
        # Extract repo name (remove -repo suffix for cleaner names)
        repo_name=$(echo "$repo" | sed 's/-repo$//')
        git remote add origin "https://x-access-token:${TOKEN}@github.com/Lo-oMeN/${repo_name}.git" 2>/dev/null || true
    fi
    
    # Rename master to main if needed
    git branch -m main 2>/dev/null || true
    
    # Push
    if git push -u origin main --force 2>&1; then
        echo "✓ $repo pushed successfully"
    else
        echo "✗ $repo push failed (token may lack write permissions)"
    fi
    
    echo ""
done

echo "=== All repos processed ==="
echo ""
echo "Verify at: https://github.com/Lo-oMeN"
