# Visual Marketing Agent

An autonomous AI agent for generating visual marketing campaigns for an apparel shop, built with Google's Agent Development Kit (ADK).

**Local ENV VARS required** in .env.local `GEMINI_API_KEY=nnnnn`

---

## 👕 Project Overview

This project implements a sophisticated, multi-agent system designed to automate the creation of visual marketing assets. Given a high-level business intent, the agent generates creative concepts, produces simulated images and videos of models wearing merchandise, and drafts a social media post ready for publication on X/Twitter.

The primary use case is for a hypothetical apparel shop specializing in t-shirts with cat prints.

---

## 🚀 Agent Workflow

The agent operates in a sequential pipeline, where each step builds upon the last. This ensures a structured and coherent workflow from concept to final output.

```mermaid
flowchart TD
    subgraph VisualMarketingAgent
        A[1. Business Intent <br><i>(e.g., 'Summer campaign for cat t-shirts')</i>] --> B{2. Visual Ideation};
        B --> C[3. Visual Generation <br><i>(Parallel Image & Video Simulation)</i>];
        C --> D{4. Twitter Publishing};
    end
    D --> E[5. Formatted Tweet <br><i>(Text + Simulated Asset)</i>];
```

1.  **Business Intent:** The process starts with a high-level goal provided by the user.
2.  **Visual Ideation:** The `VisualIdeationAgent` brainstorms several distinct visual concepts and scenes that fit the campaign's theme.
3.  **Visual Generation:** A parallel layer simulates the creation of visual assets:
    *   The `ImageGenerationAgent` selects a baseline product image and a concept to describe a final, realistic marketing still.
    *   The `VideoGenerationAgent` describes a short, engaging video clip based on a chosen concept.
4.  **Twitter Publishing:** The `TwitterPublisherAgent` takes the generated asset descriptions and drafts a compelling tweet, complete with relevant hashtags and a call to action.
5.  **Final Output:** The result is a ready-to-use social media post.

---

## ⚙️ Project Structure

This project is organized as follows:

```
marketingflow/
├── app/                 # Core application code
│   ├── agent.py         # Main agent logic
│   └── ...
├── adr/                 # Architecture Decision Records
├── images_baseline/     # Baseline product images for generation
├── tests/               # Unit and integration tests
├── README.md            # This file
├── ROADMAP.md           # Project roadmap
├── TODO.md              # Current development tasks
└── pyproject.toml       # Project dependencies and configuration
```

---

## ⚡ Quick Start

### Prerequisites
- **uv**: Python package manager - [Install](https://docs.astral.sh/uv/getting-started/installation/)
- **Google Cloud SDK**: For GCP services - [Install](https://cloud.google.com/sdk/docs/install)

### Installation
Install all required dependencies:
```bash
make install
```

### Running the Agent
To run the agent with the default apparel shop scenario, execute the test script:
```bash
uv run python run_agent.py
```
This will run the full pipeline and print the output of each agent to the console. You can modify the `query` in `run_agent.py` to test different business intents.