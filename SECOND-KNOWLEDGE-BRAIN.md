# SECOND-KNOWLEDGE-BRAIN.md — dynamic-itinerary-shuffler

> This file is the self-improving knowledge base for the project. It grows automatically via the crawl4ai crawler (see Self-Update Protocol below) and is supplemented by manual additions during development.

---

## Core Concepts & Theoretical Foundations

### Vehicle Routing Problem (VRP) & TSP
The foundational combinatorial optimization problem for itinerary planning. The **Traveling Salesman Problem (TSP)** minimizes total travel distance/time for a single-vehicle, single-visit-per-node tour. The **Vehicle Routing Problem with Time Windows (VRPTW)** extends this to: multiple vehicles, capacity constraints, and hard time-window constraints per stop (venue opening hours). Modern solvers use:
- **Column generation + branch-and-price** (exact, for small instances <20 nodes)
- **Metaheuristics:** Large Neighborhood Search (LNS), Simulated Annealing, Genetic Algorithms (for larger instances)
- **Google OR-Tools** implements a hybrid: CP-SAT solver + guided local search metaheuristic

### Real-Time Adaptive Re-Optimization
The key novelty of this project over standard itinerary planners. The **Dynamic Vehicle Routing Problem (DVRP)** covers scenarios where new requests or disruptions arrive during execution. Key academic frameworks:
- **Rolling horizon optimization:** Re-solve the remaining sub-problem when a disruption occurs, treating already-visited stops as fixed
- **Robust optimization:** Build slack into initial schedule to absorb minor disruptions without full re-solve
- **Stochastic VRP:** Model disruption probability distributions proactively

### Semantic Preference Matching
Using sentence embeddings (dense vector representations) to match venue characteristics against user preference profiles. Cosine similarity in embedding space approximates semantic relatedness — a user who likes "cozy independent bookshops" will have their embedding cluster near venues tagged "quiet", "artisan", "literary" even if those exact words weren't used.

### LLM as Context Reasoner (not Optimizer)
A critical architectural principle: LLMs excel at understanding nuanced human preferences and generating natural language rationale, but are unreliable for combinatorial optimization (they hallucinate feasibility). The correct division: OR-Tools handles all mathematical optimization; LLM handles semantic preference reasoning and user communication only.

---

## Key Research Papers

| Title | Authors | Year | Venue | Link | Relevance |
|-------|---------|------|-------|------|-----------|
| Dynamic Vehicle Routing: A Review | Pillac et al. | 2013 | Computers & Operations Research | https://doi.org/10.1016/j.cor.2012.11.007 | Foundational survey on DVRP — must-read for disruption handling architecture |
| OR-Tools: A Constraint Programming Solver | Perron & Furnon | 2023 | Google Research | https://developers.google.com/optimization | Primary solver documentation and theory |
| BERT: Pre-training of Deep Bidirectional Transformers | Devlin et al. | 2019 | NAACL | https://arxiv.org/abs/1810.04805 | Foundation for sentence-transformers embeddings used in venue matching |
| Sentence-BERT: Sentence Embeddings using Siamese BERT | Reimers & Gurevych | 2019 | EMNLP | https://arxiv.org/abs/1908.10084 | Direct basis for all-MiniLM-L6-v2; core to venue preference matching |
| Attention Is All You Need | Vaswani et al. | 2017 | NeurIPS | https://arxiv.org/abs/1706.03762 | Transformer foundation underpinning all LLM components |
| Large Language Models as Optimizers | Yang et al. | 2023 | ICLR 2024 | https://arxiv.org/abs/2309.03409 | Analysis of LLM optimization capability limitations — justifies keeping OR-Tools for math |
| Learning to Route in Similarity Estimation for Effective Recommendations | Huang et al. | 2021 | WWW | https://doi.org/10.1145/3442381.3450047 | Graph-based travel recommendation routing |
| Phi-3 Technical Report | Abdin et al. (Microsoft) | 2024 | arXiv | https://arxiv.org/abs/2404.14219 | Phi-3-mini model used for offline SLM reasoning |
| Robust Itinerary Recommendation with Uncertain Venue Availability | Zhou et al. | 2022 | KDD | https://doi.org/10.1145/3534678.3539134 | Direct relevance: robust itinerary planning under uncertainty |
| Real-Time Traffic Flow Prediction: A Review | Lana et al. | 2018 | IEEE TITS | https://doi.org/10.1109/TITS.2018.2803404 | Background on traffic prediction models for disruption detection |
| TravelPlanner: A Benchmark for Real-World Planning with LLMs | Xie et al. | 2024 | ICML | https://arxiv.org/abs/2402.01622 | Benchmark for LLM travel planning — validates our LLM-as-context (not optimizer) approach |

---

## State-of-the-Art ML/DL Models

### Venue Embedding & Recommendation

| Model ID | Task | Benchmark | Notes |
|----------|------|-----------|-------|
| `sentence-transformers/all-MiniLM-L6-v2` | General semantic embeddings | SBERT benchmarks | 80MB, fast inference, ideal for mobile-adjacent server use |
| `sentence-transformers/all-mpnet-base-v2` | Higher-quality embeddings | Outperforms MiniLM on SBERT | Larger (420MB); use if preference matching quality is insufficient |
| `BAAI/bge-m3` | Multilingual embeddings | MTEB SOTA | Use for multi-language itinerary support (international travelers) |

### Local SLM (Offline Reasoning)

| Model ID | Task | Size | Notes |
|----------|------|------|-------|
| `microsoft/Phi-3-mini-4k-instruct` | Context reasoning, venue explanation | 3.8B params, ~2.3GB | Primary offline SLM |
| `Qwen/Qwen2-0.5B-Instruct` | Ultra-lightweight offline reasoning | 0.5B params, ~300MB | For very constrained mobile scenarios |
| `google/gemma-2-2b-it` | Instruction following | 2B params | Alternative to Phi-3-mini |

### Sentiment / Mood Detection

| Model ID | Task | Notes |
|----------|------|-------|
| `cardiffnlp/twitter-roberta-base-sentiment-latest` | 3-class sentiment (pos/neg/neu) | Trained on social media text; robust to informal input |
| `j-hartmann/emotion-english-distilroberta-base` | 7-class emotion (joy, anger, etc.) | Richer than sentiment; useful for mood-aware itinerary adjustment |

### Disruption Prediction (Future Work)

| Model ID | Task | Notes |
|----------|------|-------|
| `google/timesfm-1.0-200m` | Time-series forecasting | Could predict traffic congestion patterns; experimental |
| Custom LSTM/TCN | Weather + traffic disruption probability | Requires training on historical API data; Phase 4+ |

---

## Tools, Libraries & Frameworks

| Tool | GitHub | Use Case |
|------|--------|---------|
| Google OR-Tools | https://github.com/google/or-tools | TSP/VRPTW solver — core optimization engine |
| NetworkX | https://github.com/networkx/networkx | City graph modeling, shortest path |
| sentence-transformers | https://github.com/UKPLab/sentence-transformers | Venue embedding pipeline |
| Playwright | https://github.com/microsoft/playwright | Booking RPA automation |
| FastAPI | https://github.com/tiangolo/fastapi | Backend REST API framework |
| APScheduler | https://github.com/agronholm/apscheduler | Background polling daemon for disruption detection |
| crawl4ai | https://github.com/unclecode/crawl4ai | Automated research crawler for SECOND-KNOWLEDGE-BRAIN updates |
| Anthropic SDK | https://github.com/anthropics/anthropic-sdk-python | Claude API integration |
| keyring | https://github.com/jaraco/keyring | Secure OS keychain credential storage |
| cryptography | https://github.com/pyca/cryptography | AES-256-GCM encryption for local SQLite data |
| react-native-maps | https://github.com/react-native-maps/react-native-maps | Itinerary map visualization |
| Redis | https://github.com/redis/redis | Live state cache, disruption event queue |
| SQLAlchemy | https://github.com/sqlalchemy/sqlalchemy | SQLite ORM |
| httpx | https://github.com/encode/httpx | Async HTTP client for external APIs |
| transformers | https://github.com/huggingface/transformers | HuggingFace model loading |

---

## Self-Update Protocol (crawl4ai Configuration)

### Target Sources
| Source | URL / Query | Frequency |
|--------|------------|-----------|
| ArXiv cs.AI | https://arxiv.org/search/?query=itinerary+optimization&searchtype=all | Weekly |
| ArXiv cs.LG | https://arxiv.org/search/?query=travel+recommendation+personalization&searchtype=all | Weekly |
| ArXiv cs.RO | https://arxiv.org/search/?query=vehicle+routing+real-time+dynamic&searchtype=all | Weekly |
| HuggingFace Papers | https://huggingface.co/papers?q=route+optimization | Weekly |
| Papers with Code | https://paperswithcode.com/task/route-optimization | Weekly |
| ACM Digital Library | https://dl.acm.org/search/proceedings?query=itinerary&within=owners.owner=HOSTED | Monthly |

### Domain-Specific Search Queries
```
"dynamic vehicle routing problem"
"itinerary optimization disruption"
"travel recommendation LLM"
"real-time re-routing travelers"
"venue recommendation personalization"
"traffic prediction deep learning"
"weather-aware travel planning"
"TSP time windows heuristics"
"travel disruption recovery"
"point of interest recommendation"
```

### Crawler Configuration (crawl4ai)
```python
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig

config = CrawlerRunConfig(
    target_sources=SOURCES,
    search_queries=QUERIES,
    output_file="SECOND-KNOWLEDGE-BRAIN.md",
    append_mode=True,
    date_stamp=True,
    dedup_by="doi_or_arxiv_id",
    max_results_per_query=5,
    relevance_threshold=0.7,
)
```

### Update Frequency
- **Weekly:** ArXiv, HuggingFace Papers, Papers with Code
- **Monthly:** ACM Digital Library, Google Scholar
- **On-demand:** When major new model release detected (e.g., new SOTA in VRPTW)

### New Entry Format (Date-Stamped)
```markdown
<!-- CRAWL UPDATE: 2026-06-10 -->
| {Title} | {Authors} | {Year} | {Venue} | {DOI/arXiv} | {Relevance note} |
```

---

## Knowledge Update Log

| Date | Source | New Additions | Notes |
|------|--------|--------------|-------|
| 2026-06-03 | Manual (project initialization) | 11 papers, 3 model tables, full tool list | Initial knowledge base created |

---

*Next scheduled crawl: 2026-06-10 (weekly cadence)*
