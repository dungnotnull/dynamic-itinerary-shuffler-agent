# PROJECT-detail.md — dynamic-itinerary-shuffler

## Executive Summary
dynamic-itinerary-shuffler is an AI-powered travel operations agent that replaces static travel plans with a self-healing, adaptive itinerary engine. By fusing combinatorial optimization (OR-Tools TSP/VRP), real-time environmental signals (weather, traffic, venue status), and LLM-driven contextual preference reasoning, the system autonomously re-routes travelers when disruptions occur — substituting venues, re-ordering stops, and handling booking changes on linked platforms without manual intervention.

---

## Problem Statement
Travel plans are written optimistically but executed in chaos. Research by Amadeus (2023) found that 67% of travelers experienced at least one significant itinerary disruption on their last trip; 41% reported spending over 30 minutes manually replanning mid-trip. The global travel experience market is projected to reach $1.2T by 2028 (Statista), yet the dominant tooling (static PDF itineraries, Google Maps saved lists) has no disruption-awareness layer. Key disruption categories:
- **Weather:** Sudden rain/storm forcing outdoor-to-indoor activity swaps
- **Venue closure:** Unexpected closures, sold-out sessions, operational issues
- **Traffic congestion:** Real-time density shifts making scheduled transit times infeasible
- **Mood drift:** Traveler spontaneously wants to change activity category

No existing consumer product combines real-time monitoring + re-optimization + automated rebooking into a unified agent loop.

---

## Target Users & Use Cases

| User Type | Use Case |
|-----------|---------|
| Solo traveler | Automated reroute when museum closes unexpectedly; agent finds nearest alternative with similar theme |
| Family group | Weather triggers swap of outdoor theme park to indoor aquarium; agent rebulks restaurant reservation for new location |
| Business traveler with leisure | Traffic jam compresses lunch window; agent reorders afternoon stops and notifies restaurant of later arrival |
| Travel influencer/creator | Agent logs all real-time swaps with reasoning for content creation ("how my day actually went vs. planned") |
| Group trip coordinator | Centralized agent manages everyone's constraints while optimizing shared itinerary |

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        MOBILE APP (React Native)                │
│   [Itinerary View]  [Map View]  [Disruption Alert]  [Settings] │
└───────────────────────────┬─────────────────────────────────────┘
                            │ REST / WebSocket
┌───────────────────────────▼─────────────────────────────────────┐
│                      FASTAPI BACKEND                            │
│  ┌────────────────┐  ┌──────────────────┐  ┌────────────────┐  │
│  │  Itinerary API │  │  Disruption Mgr  │  │  Booking Layer │  │
│  │  (CRUD, share) │  │  (event daemon)  │  │  (RPA + APIs)  │  │
│  └────────┬───────┘  └────────┬─────────┘  └───────┬────────┘  │
│           │                   │                     │           │
│  ┌────────▼───────────────────▼─────────────────────▼────────┐  │
│  │              OPTIMIZATION ENGINE                           │  │
│  │   OR-Tools TSP/VRP Solver  │  NetworkX Graph Model        │  │
│  │   Dijkstra/A* Routing      │  Time-Window Constraints      │  │
│  └────────────────────────────┬───────────────────────────────┘  │
│                               │                                 │
│  ┌────────────────────────────▼───────────────────────────────┐  │
│  │              LLM CONTEXT LAYER                             │  │
│  │   Claude API (primary) → GPT-4o → Ollama (offline)        │  │
│  │   HuggingFace Sentence Transformers (venue embeddings)     │  │
│  │   Local SLM: Phi-3-mini (offline context)                  │  │
│  └────────────────────────────┬───────────────────────────────┘  │
│                               │                                 │
│  ┌────────────────────────────▼───────────────────────────────┐  │
│  │              DATA LAYER                                     │  │
│  │   SQLite (user profile, itinerary history) [AES-256]       │  │
│  │   Redis (live state cache, disruption queue)               │  │
│  └────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                               │
         ┌─────────────────────┼────────────────────┐
         ▼                     ▼                    ▼
  OpenWeatherMap API    Google Maps Platform    Foursquare/OpenTable
  (weather signals)    (traffic + places)      (venue discovery + booking)
```

---

## Tech Stack

| Component | Technology | Source |
|-----------|-----------|--------|
| Backend API | FastAPI 0.111+ | pip |
| Optimization | Google OR-Tools 9.x | pip (ortools) |
| Graph modeling | NetworkX 3.x | pip |
| Mobile app | React Native 0.74 | npm |
| LLM primary | Anthropic Claude API (claude-sonnet-4-6) | API |
| LLM fallback | OpenAI GPT-4o | API |
| LLM offline | Ollama (llama3.2:3b) | local |
| Local SLM | Phi-3-mini-4k-instruct | HuggingFace |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 | HuggingFace |
| Sentiment | cardiffnlp/twitter-roberta-base-sentiment | HuggingFace |
| Local DB | SQLite + SQLAlchemy 2.x | pip |
| Cache | Redis 7.x | docker / local |
| Booking RPA | Playwright 1.44 | pip |
| Weather | OpenWeatherMap API | API |
| Traffic/Places | Google Maps Platform | API |
| Venue discovery | Foursquare Places API | API |
| Encryption | cryptography (AES-256-GCM) | pip |

---

## ML/DL Models

### Primary HuggingFace Models

| Model ID | Task | Fine-tune Needed? | Training Data |
|----------|------|------------------|---------------|
| `sentence-transformers/all-MiniLM-L6-v2` | Venue semantic embedding for similarity search | No — zero-shot sufficient | N/A |
| `microsoft/Phi-3-mini-4k-instruct` | Offline context reasoning, venue explanation | No — prompt-engineered | N/A |
| `cardiffnlp/twitter-roberta-base-sentiment-latest` | User mood detection from optional text input | No | N/A |

### Optimization (Non-ML)
- **TSP/VRP:** Google OR-Tools with time-window constraints and capacity modeling
- **Routing:** Dijkstra for shortest path; A* for heuristic-guided route planning on graph representation of city map
- **Distance matrix:** Pre-computed via Google Maps Distance Matrix API; cached in Redis

---

## External LLM API Integration (Pluggable Backend Design)

```python
# LLM backend resolution order
LLM_CHAIN = [
    {"provider": "anthropic", "model": "claude-sonnet-4-6", "env": "CLAUDE_API_KEY"},
    {"provider": "openai",    "model": "gpt-4o",            "env": "OPENAI_API_KEY"},
    {"provider": "ollama",    "model": "llama3.2:3b",       "env": "OLLAMA_BASE_URL"},
]
```

**LLM Responsibilities (context layer only):**
- Semantic venue alternative selection ("this user likes artsy cafes, not chain coffee shops")
- Natural language explanation of re-routing decisions to user
- Parsing free-text user preferences during onboarding
- Generating disruption notification messages in user's preferred tone

**Optimization Responsibilities (OR-Tools only):**
- Route ordering (TSP/VRP)
- Time feasibility checking
- Distance/duration matrix computation
- Hard constraint satisfaction (venue opening hours, travel time budgets)

---

## Feature Specification

### MVP Features
- [ ] User creates itinerary via natural language or structured input (venue list, date, duration)
- [ ] OR-Tools optimizer computes optimal visit order with time windows
- [ ] Background daemon monitors weather (OpenWeatherMap) every 5 minutes
- [ ] Disruption detected → alternative venue candidates fetched (Foursquare)
- [ ] LLM ranks candidates by user preference match
- [ ] User receives push notification with proposed swap; 1-tap approval
- [ ] Itinerary automatically re-optimized around swap
- [ ] Local SQLite storage of all itineraries and preference history

### Advanced Features
- [ ] Tier 3 automated rebooking (cancel restaurant reservation + rebook new venue)
- [ ] Traffic-aware re-routing via Google Maps Traffic API
- [ ] Mood-based itinerary adjustment (sentiment analysis of optional user input)
- [ ] Group itinerary coordination (multiple users, merged constraints)
- [ ] Itinerary "replay log" export for content creators
- [ ] Proactive suggestions (weather window opens → prompt outdoor activity move-up)
- [ ] Offline mode with local SLM (Phi-3-mini) for low-connectivity travel
- [ ] Calendar and flight integration (import existing travel plans from Google Calendar)
- [ ] Multi-city trip support with inter-city transit modeling

---

## Full E2E Data Flow

1. **Onboarding:** User inputs travel preferences (activity types, budget tier, dietary restrictions, mobility needs) → stored in AES-256 encrypted local profile
2. **Itinerary creation:** User provides destination + date + venue wishlist → LLM parses and structures → OR-Tools computes optimal order + time slots
3. **Trip start:** Background disruption daemon activates; polls weather + traffic every 5 minutes; venue status checked hourly
4. **Disruption event:** Weather API returns rain forecast OR traffic density exceeds threshold OR venue marked closed
5. **Alternative discovery:** Foursquare Places API queried with category filter + proximity radius; results embedded via sentence-transformers
6. **Preference matching:** User profile embedding compared against venue embeddings; top-3 candidates scored
7. **LLM context reasoning:** Claude API selects best candidate with natural language rationale based on full user preference context
8. **Re-optimization:** OR-Tools re-solves remaining itinerary with substitute venue inserted; new time windows computed
9. **User notification:** Push notification with disruption explanation + proposed swap + single-tap confirm/reject
10. **Booking automation:** If Tier 3 action required: Playwright RPA or direct API cancels old booking, places new booking on target platform
11. **State update:** Redis cache updated with new itinerary state; SQLite logs disruption event with before/after snapshots
12. **Replay log:** All swaps recorded with timestamp, rationale, and outcome for post-trip review

---

## Privacy & Security
- All user preference data and itinerary history stored locally (SQLite, AES-256-GCM)
- No raw user data transmitted to LLM APIs — only anonymized venue selection context
- API keys stored in environment variables, never in code or SQLite
- Booking automation actions require explicit user confirmation for any financial transaction
- RPA credentials for booking platforms stored in OS keychain (keyring library)
- GDPR-compliant: full local data export and deletion available via settings

---

## Key Python/JS Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | 0.111+ | Backend REST API |
| uvicorn | 0.29+ | ASGI server |
| ortools | 9.10+ | TSP/VRP optimization |
| networkx | 3.3+ | Graph modeling |
| httpx | 0.27+ | Async HTTP client |
| anthropic | 0.28+ | Claude API SDK |
| openai | 1.30+ | GPT-4o fallback SDK |
| sentence-transformers | 3.0+ | Venue embedding |
| transformers | 4.41+ | Phi-3-mini, sentiment model |
| torch | 2.3+ | PyTorch backend for HF models |
| sqlalchemy | 2.0+ | SQLite ORM |
| redis | 5.0+ | Redis client |
| playwright | 1.44+ | Booking RPA |
| cryptography | 42.0+ | AES-256-GCM encryption |
| apscheduler | 3.10+ | Background polling daemon |
| keyring | 25.0+ | Secure credential storage |

---

## Improvement Suggestions (Beyond Original Idea)

1. **Predictive disruption:** Train a lightweight time-series model on historical weather/traffic patterns to *predict* likely disruptions 2–3 hours ahead, enabling proactive re-scheduling before disruption occurs.
2. **Social venue intelligence:** Integrate real-time social signals (Instagram location density, TripAdvisor freshness scores) as additional disruption indicators (e.g., venue suddenly very crowded).
3. **Budget-aware optimization:** Add cost as a VRP constraint — when rebooking, automatically filter alternatives within user's remaining daily budget.
4. **Collaborative filtering:** Anonymized (federated) learning across users to improve venue preference predictions for cold-start users.
5. **AR waypoint overlay:** React Native camera layer with AR pins for next stop navigation, re-rendered after each re-optimization.
6. **Vendor partnership SDK:** Expose a webhook API so hotels and tour operators can push real-time availability signals directly into the agent.
7. **Post-trip learning loop:** After each trip, prompt user to rate actual venues visited; feed ratings back into preference model for improved future matching.
8. **Carbon footprint mode:** Add transport mode optimizer that minimizes CO2 while satisfying time constraints — eco-travel itinerary variant.
