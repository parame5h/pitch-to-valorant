# Pitch to Valorant Lobby

Submit your startup idea and get roasted by 5 Valorant agents acting as VCs — live, one verdict at a time.

## Agents
- **Jett** — evaluates market growth and 10x potential
- **Viper** — hunts competitors and market saturation
- **Reyna** — tears apart product logic and technical feasibility
- **Sova** — finds failed startups that tried the same thing
- **Sage** — synthesizes everything into a final lobby verdict

## Stack
- LLM: Groq (openai/gpt-oss-120b)
- Search: DuckDuckGo (real-time web search)
- Orchestration: asyncio (`asyncio.gather` + `asyncio.as_completed` for concurrent agent calls)
- Backend: FastAPI, streaming results via Server-Sent Events (SSE)
- Frontend: HTML/CSS/JS, consuming the SSE stream live via `fetch()` + `ReadableStream`

## Architecture
1. User submits a pitch through the frontend.
2. Keywords are extracted from the pitch (via Groq) to drive search queries.
3. Jett and Viper run concurrently, each running their own DuckDuckGo searches and Groq calls.
4. A short delay avoids Groq/DuckDuckGo rate limits before the next batch.
5. Reyna and Sova run concurrently next.
6. Sage receives all four verdicts and synthesizes a final lobby score.
7. Each agent's result is streamed to the frontend the moment it resolves — via `POST /analyze` returning `text/event-stream` — so the user watches the debrief unfold live instead of waiting for the full pipeline to finish.

## Running locally
```bash
uvicorn main:app --reload
```
Then open `http://127.0.0.1:8000/` — the FastAPI app serves the frontend directly from `static/index.html`.

## Future Work
- **Authentication** — `/analyze` is currently open; add API key or session-based auth before any public deployment to prevent abuse of the underlying Groq quota.
- **Replace fixed sleep-based rate limiting** — the pipeline currently uses hardcoded `asyncio.sleep()` calls between agent batches to avoid hitting Groq/search rate limits. Swap this for a proper rate limiter (token bucket, retry-with-backoff on 429s, or a request queue) so latency scales with actual API headroom instead of a fixed guess.
- **Structured error handling for LLM output** — agent calls currently assume the LLM always returns valid JSON matching the expected schema. Add try/except around parsing with a graceful fallback (retry once, or return a clearly-marked error verdict) instead of crashing the whole request.
- **Per-agent SSE progress events** — currently the frontend only learns an agent is "active" client-side (via a naive local timer/state), not from the backend. Consider emitting a lightweight `{"agent": "jett", "status": "analyzing"}` event when a batch starts, so the loading state is driven by real backend progress instead of assumption.
- **Caching** — cache search results per pitch/keyword combo for a short window, in case a user resubmits a similar pitch, to cut down on redundant DuckDuckGo calls.
- **Persisting past analyses** — store submitted pitches and verdicts (e.g. MongoDB) so users could revisit or share a past lobby result via a shareable link.
