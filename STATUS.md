# Project Status & Maturity

**Version:** 0.2.0
**State:** Development / Simulation Phase

This document outlines the current progress, capabilities, and limitations of the Visual Marketing Agent.

---

## ✅ Progress to Date

- **Core Agentic Architecture:** A robust multi-agent pipeline has been implemented using the Google ADK framework (`SequentialAgent` and `ParallelAgent`).
- **Visual Generation Workflow:** The agent logic has been successfully pivoted from text-based generation to a visual-first workflow for a hypothetical apparel shop.
- **End-to-End Simulation:** The entire pipeline—from taking a business intent to generating a final social media post—is functional and validated using **simulated** tool outputs.
- **Tool Integration Scaffolding:** Placeholder tools for listing baseline images, generating images, and generating videos have been created and integrated into the agent logic.
- **Comprehensive Documentation:**
    - A `README.md` and `ROADMAP.md` have been created.
    - Architecture Decision Records (ADRs) documenting the business and technical strategy are in place.

---

## 📊 Current Maturity State

### What is Working

- **End-to-End Workflow Logic:** You can run `uv run python run_agent.py` or use the `make validate-all` command to execute the full pipeline. The agent will correctly:
    1.  Receive a business intent.
    2.  Brainstorm visual concepts.
    3.  Call the image and video generation tools with the correct inputs (prompts and baseline image paths).
    4.  Receive the placeholder responses from the tools.
    5.  Draft a final tweet using the placeholder responses.
- **Interactive Testing UI:** The `make playground` command successfully launches the `adk web` UI, allowing for interactive testing of the simulated workflow.
- **Unit Tests:** Basic unit tests for the helper tools are in place and passing.

### What is NOT Working (Next Steps for Implementation)

- **Real Image/Video Generation:** This is the most significant limitation. The agent **does not** call any real AI models to generate visual assets. The `generate_image...` and `generate_video...` functions are **simulations** that only create placeholder text files. To achieve the goal of seeing real generated images, a developer must replace the simulation logic in `app/agent.py` with actual API calls to services like Imagen or Veo.
- **X/Twitter Integration:** The `TwitterPublisherAgent` only *drafts* a tweet. It does not have a tool to connect to the X/Twitter API to publish the post. This integration needs to be built.
- **Advanced Validation:** The sophisticated validation loop described in the latest HLD (ADR-003) is documented but **not yet implemented**. The current pipeline is a simple sequential flow.

---

## 🎯 The Envisioned User Journey (Target State)

The ultimate goal is to use the `adk web` UI where a user can provide a prompt like:

> "Generate me marketing images and a video for my new cat t-shirt merch."

The system should then:
1.  Use the baseline images from the `@images_baseline/**` folder as a reference.
2.  Call the appropriate Gemini models (e.g., Imagen, Veo) to generate **real, relevant visual assets** showing people wearing the merchandise in various settings.
3.  Present the final generated assets and the composed social media post to the user in the UI.

Achieving this vision requires completing the "What is NOT Working" items listed above.
