# Project Roadmap

This document outlines the development roadmap for the Visual Marketing Agent.

---

## ✅ **Phase 1: Core Architecture & Visual Refactor (Complete)**

- [x] **Initial Text-Based Pipeline:** Implemented a multi-agent system for generating text-based campaign briefs.
    - [x] Parallel Ideation Layer
    - [x] Synthesis Agent
    - [x] Brand Assurance / Validation Agent
    - [x] Campaign Priority / Queueing Agent
- [x] **Pivot to Visual Generation:** Refactored the entire agent pipeline to focus on generating visual marketing assets for a hypothetical apparel shop.
    - [x] Created `VisualIdeationAgent` to brainstorm visual concepts.
    - [x] Created simulated `ImageGenerationAgent` and `VideoGenerationAgent`.
    - [x] Implemented a tool to access baseline product images.
    - [x] Created `TwitterPublisherAgent` to draft social media posts.
- [x] **Initial Documentation:** Created ADRs for Business Strategy, Technical Direction, and High-Level Architecture. Updated the core architecture document.

---

## ⏳ **Phase 2: Documentation & Workflow Enhancement (In Progress)**

- [ ] **Revise `README.md`:** Update the main project README to reflect the new visual generation focus, including a user journey diagram.
- [ ] **Update ADRs:** Revise the architecture decision records to align with the pivot to visual content.
- [ ] **Enhance Agent Logic:** Improve the prompts and logic for all agents in the new pipeline.
- [ ] **Error Handling:** Implement more robust error handling within the agent workflow.

---

## 未来 **Phase 3: Tooling & Integration (Future)**

- [ ] **Real Image Generation:** Replace the simulated `ImageGenerationAgent` with a tool that calls a real image generation API (e.g., Imagen on Vertex AI).
- [ ] **Real Video Generation:** Replace the simulated `VideoGenerationAgent` with a tool that calls a real video generation API (e.g., Veo).
- [ ] **Social Media Integration:** Replace the placeholder `TwitterPublisherAgent` with a tool that uses the X/Twitter API to post content directly.
- [ ] **Advanced Analytics:** Implement an `AnalyticsTracker` agent to monitor the performance of published content.
- [ ] **Unit & Integration Testing:** Expand the test suite to cover all new tools and agent interactions.
