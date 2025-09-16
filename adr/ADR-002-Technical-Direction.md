# ADR-002: Technology Stack and Framework

**Status:** Accepted

## Context

To build a robust, multi-agent system, we require a framework that simplifies agent orchestration, state management, and tool integration. The chosen technology stack must support rapid development, have a strong ecosystem of AI/ML libraries, and be suitable for production deployment on Google Cloud.

## Decision

We will use the **Python** programming language and the **Google Agent Development Kit (ADK)**. The project will be built upon the "Agent Starter Pack" template, which provides a production-ready foundation including CI/CD, observability, and deployment best practices for Google Cloud.

## Consequences

**Positive:**
- **Rich Ecosystem:** Python is the de facto standard for AI/ML development, providing access to a vast array of libraries and tools.
- **Simplified Orchestration:** The ADK provides high-level primitives for building multi-agent systems, such as `SequentialAgent` and `ParallelAgent`, which map directly to our desired architecture.
- **Reliable Data Flow:** ADK's state management and `output_schema` features (using Pydantic) allow for the creation of reliable, self-validating data pipelines between agents.
- **Production-Ready:** Starting with the "Agent Starter Pack" accelerates our path to production by providing pre-configured infrastructure and deployment patterns.

**Negative:**
- **Framework Specificity:** Commits us to the ADK framework, requiring developers to learn its specific patterns and conventions.
