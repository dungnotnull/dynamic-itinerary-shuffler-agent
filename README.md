# Dynamic Itinerary Shuffler Agent

An AI-powered travel operations center that replaces static travel plans with a self-healing, adaptive itinerary engine. 

## Overview

Most travel itineraries are static and break the moment reality diverges from the plan. This project implements a real-time travel agent that monitors live signals (weather, traffic, venue status) and autonomously re-optimizes schedules and handles booking changes without manual intervention.

## Core Architecture

The system is built on a three-layer architecture:

1. Optimization Layer: Uses Google OR-Tools to solve the Vehicle Routing Problem with Time Windows (VRPTW), ensuring all stops are feasible and distance-optimized.
2. Intelligence Layer: Combines Sentence-Transformers for semantic venue matching and a pluggable LLM chain (Claude, GPT-4o, Ollama) for preference-based reasoning.
3. Execution Layer: A FastAPI backend integrated with Playwright for RPA-based booking automation and a Redis queue for asynchronous disruption handling.

## Key Features

- Dynamic Re-routing: Automatic route adjustment based on real-time traffic and weather.
- Semantic Venue Substitution: Substitutes closed or unsuitable venues with alternatives that match the user's specific "vibe" and preference profile.
- Privacy-First Profiles: User preferences are stored in AES-256-GCM encrypted SQLite databases.
- Autonomous Booking: Handles cancellations and new bookings via a browser-automation RPA layer.
- Self-Improving Knowledge: An automated research crawler updates the project's knowledge base with the latest SOTA routing and AI papers.

## Tech Stack

- Backend: FastAPI, SQLAlchemy, Redis
- Optimization: Google OR-Tools, NetworkX
- AI/ML: HuggingFace (Sentence-Transformers), Anthropic Claude, OpenAI GPT-4o, Ollama
- Automation: Playwright
- Database: SQLite (Encrypted)
- Deployment: Docker, Docker Compose

## Getting Started

### Installation

1. Clone the repository:
   git clone https://github.com/dungnotnull/dynamic-itinerary-shuffler-agent.git

2. Install dependencies:
   pip install -r requirements.txt

3. Configure Environment:
   Create a .env file based on .env.example and add your API keys.

4. Run the project:
   docker-compose up --build

### Simulation Mode

To test the full "Sensing-to-Healing" pipeline without API keys:
1. Seed the database:
   python scripts/seed_db.py
2. Run the system simulator:
   python scripts/simulator.py

## Project Roadmap

- Phase 0: Research and Environment Setup (Completed)
- Phase 1: MVP Core Loop (Completed)
- Phase 2: ML/AI Disruption Integration (Completed)
- Phase 3: Automated Booking Layer (Completed)
- Phase 4: Knowledge Brain Auto-Update (Completed)
- Phase 5: Production Hardening and Deployment (Completed)
