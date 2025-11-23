# AI Code Fix Agent

This repository provides a small FastAPI service that wraps a local model to provide code-fixing suggestions.

**Note:** The model referenced by `ai/call_model.py` is `Qwen/Qwen2.5-coder-1.5B-Instruct`. This can be large and may require access credentials (Hugging Face token) and sufficient memory (CPU or GPU). If you do not have the model locally or access to it, the service will fail when starting.

**Quick overview:**
- Start the server.
- Send a `POST` to `/fix` with a JSON body: `{ "language", "cwe", "code" }`.
- The service returns `fixed_code`, `diff`, `explanation`, `model_used`, and `token_usage`.

---

**Setup**

- Recommended: create and activate a virtual environment.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

- Install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

- If you need to use the Hugging Face Hub for private/large models, either:
  - run `huggingface-cli login` and enter your token, or
  - set the environment variable `HUGGINGFACE_HUB_TOKEN` before starting the server:

```bash
export HUGGINGFACE_HUB_TOKEN="hf_..."
```

**Optional package notes**
- The project uses `transformers`, `torch` and `fastapi`. Ensure you have compatible `torch` for your platform (CPU vs GPU). If you plan to use GPU, install a CUDA-enabled PyTorch build.

---

**Run the API server**

Start the app with `uvicorn` from the repository root:

```bash
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

- On first start, `ai/call_model.py` will attempt to load the model defined by `MODEL_NAME`.
- If model loading fails due to memory or missing credentials, you will see errors in the server logs.

Once running, the service provides:

- `GET /` — returns a simple "hello world" string.
- `POST /fix` — accepts a JSON body with the fields specified below.

---

**API: `POST /fix`**

Request body (JSON):

```json
{
  "language": "<language-name>",
  "cwe": "<CWE-id-or-description>",
  "code": "<source code string>"
}
```

Example minimal body:

```json
{
  "language": "python",
  "cwe": "CWE-89",
  "code": "def bad_query(user_input):\n    query = \"SELECT * FROM users WHERE name = '\" + user_input + "\'\"\n    execute(query)"
}
```

Response JSON (successful):

```json
{
  "fixed_code": "<string>",
  "diff": "<string>",
  "explanation": "<string>",
  "model_used": "Qwen2.5 coder",
  "token_usage": { "input_tokens": 0, "output_tokens": 0 }
}
```

If the server cannot parse a JSON block from the model output, `fixed_code`, `diff`, and `explanation` may be empty strings.

---

**Testing with Postman (step-by-step)**

1. Open Postman and create a new request.
2. Set request type to `POST` and the URL to `http://localhost:8000/fix`.
3. Under the "Headers" tab, add header `Content-Type: application/json`.
4. Under the "Body" tab, select "raw" and choose `JSON` from the dropdown.
5. Paste a test JSON body, for example:

```json
{
  "language": "python",
  "cwe": "CWE-89",
  "code": "def bad_query(user_input):\n    query = \"SELECT * FROM users WHERE name = '\" + user_input + "\'\"\n    execute(query)"
}
```

6. Click "Send".

7. Inspect the response pane. A successful response will include `fixed_code`, `diff`, and `explanation` fields. Example response body:

```json
{
  "fixed_code": "def bad_query(user_input):\n    # Use parameterized queries to avoid SQL injection\n    stmt = \"SELECT * FROM users WHERE name = %s\"\n    cursor.execute(stmt, (user_input,))",
  "diff": "--- original\n+++ fixed\n@@ -1,3 +1,4 @@\n-def bad_query(user_input):\n-    query = \"SELECT * FROM users WHERE name = '\" + user_input + "'\"\n-    execute(query)\n+def bad_query(user_input):\n+    # Use parameterized queries...",
  "explanation": "Replaced string concatenation with parameterized queries to prevent SQL injection.",
  "model_used": "Qwen2.5 coder",
  "token_usage": { "input_tokens": 42, "output_tokens": 120 }
}
```

Notes for Postman test:
- If the server returns a 5xx error at first request, check logs — model loading may have failed or is still in progress.
- If the response takes a long time, the model is likely generating; this is expected for large models.

---

**Testing with curl**

```bash
curl -X POST "http://localhost:8000/fix" \
  -H "Content-Type: application/json" \
  -d '{"language":"python","cwe":"CWE-89","code":"print(\"hello\")"}'
```

---
