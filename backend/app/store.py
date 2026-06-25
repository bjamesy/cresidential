from typing import Any

# In-memory session store: session_id -> plaid access_token
sessions: dict[str, str] = {}

# In-memory job store: job_id -> job state
jobs: dict[str, dict[str, Any]] = {}
