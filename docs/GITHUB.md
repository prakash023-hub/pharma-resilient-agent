# Push PharmaGuard to GitHub

Run these commands from the `pharmaguard` folder.

## 1. Create a new public repo on GitHub

Name suggestion: `pharmaguard-resilient-agent`

Do **not** initialize with a README (this project already has one).

## 2. Push from your machine

```bash
cd pharmaguard
cp .env.example .env
# Edit .env — add your rotated TFY_API_KEY

git init
git add .
git commit -m "$(cat <<'EOF'
Add PharmaGuard resilient clinical agent for TrueFoundry hackathon.

Wire AI Gateway routing, MCP OpenFDA tool access, guardrails, and real failure demos for submission.
EOF
)"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/pharmaguard-resilient-agent.git
git push -u origin main
```

## 3. Update submission doc

Edit `docs/SUBMISSION.md` and replace `<your-public-repo-url>` with your GitHub URL.

## Security checklist before push

- [ ] `.env` is **not** staged (`git status` should not list it)
- [ ] Old API key rotated in TrueFoundry
- [ ] No tokens in commit history
