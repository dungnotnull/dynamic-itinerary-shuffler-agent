# CLAUDE.md — dynamic-itinerary-shuffler

## Project Identity
- **Name:** dynamic-itinerary-shuffler
- **Tagline:** Your travel plans, resilient by design — AI reroutes in real time so you never miss a beat.
- **Status/Phase:** Pre-development (specification complete)

---

## Core Problem Being Solved
Static travel itineraries break the moment reality diverges from the plan — a sudden rainstorm, a venue closure, gridlock traffic, or a spontaneous mood shift. Travelers either scramble to improvise on their own or accept a degraded experience. The dynamic-itinerary-shuffler acts as a real-time travel operations center: it monitors live signals (weather, traffic density, venue status) and, when disruption is detected, immediately re-optimizes the remaining schedule, substitutes alternative venues that match the user's personal preferences, and autonomously handles booking changes (cancellations, rebookings) across linked apps — all without requiring the traveler to lift a finger.

---

## Architecture Summary
- **Platform:** Python backend service (FastAPI) + React Native mobile companion
- **Optimization Core:** Google OR-Tools (TSP/VRP solver), NetworkX graph modeling, Dijkstra/A* routing
- **ML Stack:** HuggingFace transformers for preference understanding; local SLM (Phi-3-mini or Qwen2-0.5B) for offline fallback context reasoning
- **Real-Time Data:** OpenWeatherMap API, Google Maps Platform (Traffic & Places), Foursquare Places API
- **Booking Automation:** Playwright/Selenium-based RPA layer for partner app integrations; direct API where available (OpenTable, Klook)
- **External LLM APIs:** Claude API (primary context & preference matching), GPT-4o (fallback), local Ollama (offline)
- **Storage:** SQLite (user profile, preferences, itinerary history), Redis (live state cache)

---

## Key Technical Decisions
1. **Separation of optimization and context layers:** TSP/VRP via OR-Tools handles time/distance math; LLM handles semantic preference matching for alternative venue selection — never mix the two.
2. **Event-driven disruption detection:** Background polling daemon checks weather/traffic every 5 minutes; disruption triggers an async re-optimization pipeline, not a synchronous block.
3. **Pluggable LLM backend:** Claude API → GPT-4o → local Ollama fallback chain; local SLM always available offline.
4. **Booking RPA as last resort:** Prefer direct partner APIs; use RPA (Playwright) only when no API exists, with human-in-the-loop confirmation for high-value transactions.
5. **Privacy-first user profile:** Travel preferences, behavioral patterns stored locally in AES-256 encrypted SQLite; never sent to external services raw.
6. **3-tier disruption response:** Tier 1 = nudge (notify, suggest swap); Tier 2 = soft re-route (auto-swap low-cost items); Tier 3 = full re-optimization with booking changes.

---

## External LLM API Integrations

| Provider | Model | Purpose | Config Key |
|----------|-------|---------|------------|
| Anthropic Claude | claude-sonnet-4-6 | Context reasoning, preference-based venue selection | `CLAUDE_API_KEY` |
| OpenAI GPT-4o | gpt-4o | Fallback LLM for venue selection & explanation | `OPENAI_API_KEY` |
| Ollama (local) | llama3.2:3b | Fully offline fallback context reasoning | `OLLAMA_BASE_URL` |

---

## HuggingFace Models in Use

| Model ID | Purpose | Link |
|----------|---------|------|
| `sentence-transformers/all-MiniLM-L6-v2` | Venue semantic similarity embedding for preference matching | https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2 |
| `microsoft/Phi-3-mini-4k-instruct` | Local SLM for offline itinerary context reasoning | https://huggingface.co/microsoft/Phi-3-mini-4k-instruct |
| `cardiffnlp/twitter-roberta-base-sentiment-latest` | User mood/sentiment detection from optional journal input | https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest |

---

## Current Active Development Tasks
- [ ] Scaffold FastAPI backend project structure
- [ ] Implement OR-Tools TSP solver with time-window constraints
- [ ] Build disruption detection daemon (weather + traffic polling)
- [ ] Integrate Claude API for venue preference matching
- [ ] Implement sentence-transformer embedding for venue similarity
- [ ] Build React Native companion app skeleton
- [ ] Implement AES-256 encrypted local SQLite user profile store
- [ ] Build RPA booking automation layer (Playwright)
- [ ] End-to-end integration test: disruption → re-optimize → rebook

---

## Related Files
- `PROJECT-detail.md` — Full technical specification and feature list
- `PROJECT-DEVELOPMENT-PHASE-TRACKING.md` — Phase-by-phase development roadmap
- `SECOND-KNOWLEDGE-BRAIN.md` — Research papers, SOTA models, self-update protocol
