# PROJECT-DEVELOPMENT-PHASE-TRACKING.md — dynamic-itinerary-shuffler

## Overview
16-week development roadmap from research to production deployment.
Each phase builds on the previous; phases 0–2 can be executed by a solo developer.

---

## Phase 0: Research & Environment Setup
**Timeline:** Week 1–2
**Goal:** Validated tech stack, working development environment, API access confirmed.

### Tasks
- [x] Set up Python 3.11+ virtual environment; install all core dependencies
- [x] Provision Redis instance (Docker) and verify connection
- [x] Register and test all external API keys: OpenWeatherMap, Google Maps Platform, Foursquare, Anthropic, OpenAI
- [x] Run OR-Tools basic TSP example with 5–10 nodes to validate solver setup
- [x] Download and test HuggingFace models locally: `all-MiniLM-L6-v2`, `Phi-3-mini-4k-instruct`, `twitter-roberta-base-sentiment`
- [x] Set up local Ollama instance with `llama3.2:3b`
- [x] Research Google Maps Distance Matrix API pricing and rate limits
- [x] Study OR-Tools VRPTW (Vehicle Routing Problem with Time Windows) documentation
- [x] Spike: prototype a 5-stop itinerary optimization and verify output correctness
- [x] Initialize FastAPI project skeleton with health check endpoint

### Deliverables
- Working development environment with all dependencies installed
- Verified API key access for all external services
- Proof-of-concept TSP solver returning correct optimal order for a sample itinerary

### Success Criteria
- OR-Tools correctly solves a 10-stop TSP with time windows in under 2 seconds
- All 3 HuggingFace models load and run inference without errors
- Anthropic Claude API returns a valid venue recommendation response

### Estimated Effort
~20 hours (2 developers × 10 hours, or 1 developer × 20 hours)

---

## Phase 1: MVP — Core Loop Working
**Timeline:** Week 3–6
**Goal:** Full end-to-end flow working for the happy path (no disruptions); user can create and view an optimized itinerary.

### Tasks
- [x] Implement SQLite schema: `users`, `itineraries`, `itinerary_stops`, `venues`, `preferences`
- [x] Implement AES-25 la-AES-256-GCM encryption wrapper for sensitive SQLite fields
- [x] Build FastAPI routes: `POST /itineraries`, `GET /itineraries/{id}`, `PUT /itineraries/{id}`, `DELETE /itineraries/{id}`
- [x] Implement OR-Tools VRPTW solver module: input venue list → output ordered stop sequence with arrival/departure times
- [x] Integrate Google Maps Distance Matrix API to compute travel time matrix for solver
- [x] Build venue preference onboarding flow (structured input: activity types, budget, dietary, mobility)
- [x] Implement LLM preference parsing: free-text preference input → structured preference object
- [x] Build React Native app screens: Onboarding, Home, Itinerary Detail, Map View
- [x] Implement map visualization with optimized route overlay (react-native-maps)
- [x] Write unit tests for TSP solver (correctness, edge cases: 1 stop, max stops)
- [x] Integration test: full itinerary creation API → solver → stored in DB → retrieved by app

### Deliverables
- Working mobile app (iOS/Android dev builds) showing an optimized itinerary on a map
- FastAPI backend with full CRUD for itineraries
- Encrypted local SQLite database with user profile and itinerary data

### Success Criteria
- User can create a 5-stop itinerary via the app in under 2 minutes
- Optimizer returns correct visit order with feasible time windows for all stops
- All itinerary data persists across app restarts (encrypted SQLite)

### Estimated Effort
~80 hours

---

## Phase 2: ML/AI Integration — Smart Features
**Timeline:** Week 7–10
**Goal:** Disruption detection active; LLM-powered venue substitution working end-to-end.

### Tasks
- [x] Implement APScheduler background daemon: polls OpenWeatherMap every 5 minutes per active trip
- [x] Implement weather disruption classifier: precipitation probability > 60% OR wind > 40 km/h → trigger disruption event
- [x] Implement Google Maps Traffic API polling: average speed below threshold → trigger congestion event
- [x] Implement venue status checker: Foursquare API + hours verification → detect closures
- [x] Build disruption event queue (Redis pub/sub)
- [x] Implement Foursquare alternative venue discovery: category-filtered, radius-bounded search
- [x] Implement sentence-transformers venue embedding pipeline: embed all candidate venues at discovery time
- [x] Implement preference-based venue ranking: cosine similarity between user profile embedding and candidate embeddings
- [x] Integrate Claude API for contextual venue selection: top-3 candidates → LLM selects best with rationale
- [x] Implement GPT-4o fallback and Ollama offline fallback for LLM chain
- [x] Implement Phi-3-mini local SLM for fully offline reasoning (no network required)
- [x] Implement 3-tier disruption response logic:
  - Tier 1: push notification with suggested swap (user manually confirms)
  - Tier 2: auto-swap low-risk items (free venues, no booking needed)
  - Tier 3: queue for booking automation (Phase 3)
- [x] Re-optimization module: OR-Tools re-runs with substitute venue, new distance matrix, updated time windows
- [x] Push notification integration (Firebase Cloud Messaging or Expo Notifications)
- [x] Write integration tests: mock weather API → disruption event → re-optimization → correct new schedule

### Deliverables
- Live disruption detection daemon running during active trips
- End-to-end: weather disruption → alternative venue selected by LLM → itinerary re-optimized → user notified
- 3-tier disruption response system operational

### Success Criteria
- Disruption detected within 5 minutes of weather API data changing
- LLM venue selection matches human judgment in >80% of test cases (manual evaluation on 20 scenarios)
- Re-optimized itinerary delivered to user within 30 seconds of disruption detection
- System gracefully degrades to offline Phi-3-mini when no internet connectivity

### Estimated Effort
~100 hours

---

## Phase 3: External LLM API Integration
**Timeline:** Week 11–12
**Goal:** Booking automation layer operational; full Tier 3 automated rebooking working for supported platforms.

### Tasks
- [x] Research and document target booking platforms with direct APIs: OpenTable, Klook, GetYourGuide
- [x] Implement OpenTable API integration: check availability, create/cancel reservation
- [x] Implement Klook/GetYourGuide API integration: check availability, initiate booking
- [x] Implement Playwright RPA fallback for platforms without APIs: browser automation for booking forms
- [x] Build RPA credential manager: OS keychain (keyring library) for secure credential storage
- [x] Implement booking confirmation flow: all Tier 3 actions require explicit user tap-to-confirm
- [x] Implement booking state tracker: pending, confirmed, cancelled — stored in SQLite
- [x] Build booking automation error handling: retry with exponential backoff, fallback to Tier 2 on failure
- [x] Implement cancellation policy awareness: warn user if cancellation fees apply before auto-cancel
- [x] Integration test: full Tier 3 flow — disruption detected → alternative found → booking cancelled → new booking placed → user confirmed → itinerary updated

### Deliverables
- Automated booking cancellation and rebooking for supported platforms (OpenTable, Klook)
- RPA fallback operational for unsupported platforms
- Full audit trail of all booking actions in SQLite

### Success Criteria
- Automated rebooking completes end-to-end in under 60 seconds for API-supported platforms
- Zero financial transactions executed without explicit user confirmation
- Cancellation policy warning shown for 100% of rebooking scenarios with fees

### Estimated Effort
~60 hours

---

## Phase 4: Self-Improving Knowledge Loop — SECOND-KNOWLEDGE-BRAIN Auto-Update
**Timeline:** Week 13–14
**Goal:** Automated crawler updates SECOND-KNOWLEDGE-BRAIN.md weekly; post-trip learning loop feeds user ratings back into preference model.

### Tasks
- [x] Implement crawl4ai crawler targeting ArXiv (cs.AI, cs.LG, cs.RO), HuggingFace Papers, ACM DL
- [x] Search queries: "itinerary optimization", "travel disruption prediction", "vehicle routing real-time", "travel recommendation personalization"
- [x] Configure crawler to append new papers to SECOND-KNOWLEDGE-BRAIN.md with date stamp
- [x] Implement HuggingFace model leaderboard scraper: check Papers with Code for updated SOTA models in route optimization and recommendation
- [x] Build post-trip user rating prompt: after trip ends, prompt user to rate each venue (1–5 stars, free text)
- [ ] Implement rating → preference update loop: update user preference embedding in SQLite based on post-trip ratings
- [x] Implement A/B test framework for LLM venue selection: track which selections user accepted vs. rejected; log outcome
- [x] Build preference drift detector: compare current preference embedding to baseline; alert if significant drift
- [x] Schedule weekly crawl4ai run via APScheduler or system cron

### Deliverables
- Weekly automated research crawler updating SECOND-KNOWLEDGE-BRAIN.md
- Post-trip learning loop: user ratings → improved preference model
- A/B outcome logging for LLM venue selection quality tracking

### Success Criteria
- Crawler runs weekly without manual intervention; adds at least 2 new relevant papers per run
- User preference model improves measurably (measured by acceptance rate of LLM suggestions) after 3+ trips

### Estimated Effort
~40 hours

---

## Phase 5: Testing, Polish & Deployment
**Timeline:** Week 15–16
**Goal:** Production-ready app with full test coverage, performance tuning, and deployment pipeline.

### Tasks
- [x] Write full unit test suite: solver, disruption detector, LLM chain, booking module (target 80%+ coverage)
- [x] Write E2E test suite: 5 complete trip scenarios with injected disruptions
- [x] Performance testing: verify re-optimization completes within SLA (30s) for 15-stop itinerary
- [x] Load testing: 100 concurrent active trips on backend (APScheduler daemon)
- [x] Mobile app UX polish: loading states, error messages, offline mode indicators
- [x] Accessibility audit: screen reader support, contrast ratios, touch target sizes
- [x] App store preparation: screenshots, app description, privacy policy
- [x] Backend deployment: containerize with Docker, deploy to cloud (AWS ECS or Fly.io)
- [x] Configure environment variable management (AWS Secrets Manager or Fly.io secrets)
- [x] Set up CI/CD pipeline (GitHub Actions): lint → test → build → deploy on merge to main
- [x] Set up monitoring: Sentry for error tracking, custom metrics for disruption detection latency
- [x] Security audit: OWASP checklist, API key exposure scan, RPA credential audit
- [x] Beta test with 5–10 real travelers; collect feedback and fix critical bugs

### Deliverables
- Production-deployed backend (containerized, monitored)
- App store-ready mobile builds (iOS + Android)
- Full CI/CD pipeline
- Beta test feedback incorporated

### Success Criteria
- 80%+ unit test coverage
- E2E test suite passes for all 5 trip scenarios
- Re-optimization SLA met: 100% of re-optimizations complete within 30 seconds
- Zero critical security findings in audit
- Beta users rate itinerary recovery experience ≥4/5 stars

### Estimated Effort
~80 hours

---

## Total Estimated Effort
| Phase | Hours |
|-------|-------|
| Phase 0: Setup | 20 |
| Phase 1: MVP | 80 |
| Phase 2: ML/AI | 100 |
| Phase 3: Booking | 60 |
| Phase 4: Self-improve | 40 |
| Phase 5: Deploy | 80 |
| **Total** | **380 hours** |

*Approximately 4 months for a 2-person team at 50% allocation, or 10 weeks for a full-time solo developer.*
