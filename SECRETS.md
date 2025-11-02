What I changed
-----------------
- Removed embedded credentials from these files and replaced them with placeholders:
  - `client_secret.json` (root)
  - `token.json` (root)
  - `lamora/HR_RANK/backend/client_secret.json`
  - `lamora/HR_RANK/backend/token.json`
  - `lamora/HR_RANK/backend/utils/client_secret.json`
- Updated `lamora/HR_RANK/backend/utils/extractor.py` to read the Groq API key from the `GROQ_API_KEY` environment variable instead of a hard-coded string.
- Added a repository `.gitignore` to prevent committing the above files and other common secrets.

Important next steps (you must do these if the repo was pushed to any remote):
1. Treat the removed credentials as compromised: rotate/revoke them immediately (Google Cloud console for OAuth credentials, Groq API key, etc.).
2. Purge secrets from git history if they were ever committed to the remote. Recommended tools:
   - BFG Repo-Cleaner (https://rtyley.github.io/bfg-repo-cleaner/)
   - git filter-repo (https://github.com/newren/git-filter-repo)
   Use these tools to remove the sensitive files and force-push cleaned history to remote.
3. Add replacement secrets locally (do not commit):
   - Save your Google OAuth client file as `client_secret.json` locally (not committed).
   - Run your app's OAuth flow to create `token.json` locally (do not commit).
   - Set `GROQ_API_KEY` in your environment instead of hard-coding it:
     - Windows PowerShell example: `$env:GROQ_API_KEY = "your_key_here"`

Why this matters
-----------------
Committed secrets can be abused, and even if removed later they may still exist in repository history or forks. Rotating keys and cleaning history reduces the risk.

If you want, I can:
- Run a follow-up scan for other potential secrets.
- Help perform git-history cleaning with step-by-step commands (I can generate the exact BFG/git-filter-repo commands and help craft a rotation plan).
