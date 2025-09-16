# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from typing import List, Literal

import google.auth
from google.adk.agents import Agent, ParallelAgent, SequentialAgent
from pydantic import BaseModel, Field

_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")

# --- Parallel Ideation Layer ---

trend_agent = Agent(
    name="TrendAgent",
    model="gemini-2.5-flash",
    description="Analyzes real-time market intelligence and identifies current trends relevant to the campaign.",
    instruction="Based on the user's business intent, identify 3-5 current market trends or news that can be leveraged. Output a bulleted list.",
    output_key="trend_ideas",
)

community_agent = Agent(
    name="CommunityAgent",
    model="gemini-2.5-flash",
    description="Focuses on engagement and educational content, identifying community pain points and questions.",
    instruction="Based on the user's business intent, identify 3-5 common questions or pain points from the target community. Frame them as educational content opportunities. Output a bulleted list.",
    output_key="community_ideas",
)

content_agent = Agent(
    name="ContentAgent",
    model="gemini-2.5-flash",
    description="Generates diverse, multi-media content ideas and formats.",
    instruction="Based on the user's business intent, brainstorm 3-5 creative content ideas (e.g., blog post, video script, social media post). Specify the format for each. Output a bulleted list.",
    output_key="content_ideas",
)

brand_agent = Agent(
    name="BrandAgent",
    model="gemini-2.5-flash",
    description="Ensures all ideas align with the brand's voice, tone, and overall consistency.",
    instruction="Based on the user's business intent, define the primary brand voice and tone for this campaign (e.g., 'professional and authoritative', 'playful and witty'). Output a short paragraph.",
    output_key="brand_voice",
)

parallel_ideation_layer = ParallelAgent(
    name="ParallelIdeationLayer",
    sub_agents=[
        trend_agent,
        community_agent,
        content_agent,
        brand_agent,
    ],
)

# --- Synthesis Layer ---

synthesis_agent = Agent(
    name="SynthesisAgent",
    model="gemini-2.5-pro",
    instruction='''You are a marketing strategist. Your task is to synthesize the ideas from your team into a single, cohesive campaign brief.

    Use the following inputs from your team:
    - Market Trends: {trend_ideas}
    - Community Insights: {community_ideas}
    - Content Ideas: {content_ideas}
    - Brand Voice: {brand_voice}

    Combine these elements into a unified campaign brief with the following sections:
    1.  **Campaign Theme:** A short, catchy theme.
    2.  **Brand Voice:** The defined voice and tone.
    3.  **Key Pillars:** 3-5 core content pillars based on the trends and community insights.
    4.  **Example Content:** 2-3 specific content pieces from the ideas provided, fleshed out slightly.
    ''',
    output_key="campaign_brief",
)

# --- Validation Layer ---

class Issue(BaseModel):
    """A specific issue found during brand validation."""
    field: str = Field(description="The specific field or area with an issue (e.g., 'Brand Voice', 'Narrative Alignment').")
    description: str = Field(description="A detailed description of the issue found.")

class BrandValidation(BaseModel):
    """The structured output for the brand validation process."""
    approved: bool = Field(description="Whether the campaign brief is approved to proceed.")
    brand_score: int = Field(description="An overall score from 0-100 for brand alignment.", ge=0, le=100)
    consistency_score: int = Field(description="An overall score from 0-100 for consistency.", ge=0, le=100)
    compliance_issues: List[Issue] = Field(description="A list of specific compliance or brand issues found.")
    recommendations: List[str] = Field(description="A list of actionable recommendations for improvement.")

brand_assurance_agent = Agent(
    name="BrandAssuranceAgent",
    model="gemini-2.5-pro",
    description="Validates the campaign brief against brand guidelines and quality standards.",
    instruction='''You are the Brand Assurance Agent. Your job is to act as a strict quality gate.
    Analyze the campaign brief provided in `{campaign_brief}`.

    Validate it against the following criteria:
    1.  **Brand Voice:** Is the tone (e.g., 'authentic and empowering', 'optimistic and inspiring') consistent with the brief's definition?
    2.  **Narrative Alignment:** Does the campaign theme and content align with the business objective of launching sustainable coffee cups for millennials?
    3.  **Content Balance:** Does the content seem to follow a healthy mix of educational and promotional material? (e.g., 60/40 split).
    4.  **Clarity and Cohesion:** Is the brief clear, well-structured, and internally consistent?

    Provide a rigorous, critical review. If there are any weaknesses, fail the validation and provide clear, actionable recommendations. Your output must be a single JSON object matching the BrandValidation schema.
    ''',
    output_schema=BrandValidation,
    output_key="brand_validation_report",
)

# --- Queue & Distribution Layer ---

class CampaignPriority(BaseModel):
    """The structured output for the campaign priority queue."""
    campaign_type: Literal["Business Campaign", "Official Announcement", "Educational", "Community", "Automated Content"] = Field(description="The classified type of the campaign.")
    priority: int = Field(description="The assigned priority level (1-4), where 1 is the highest.", ge=1, le=4)
    reasoning: str = Field(description="A brief justification for the assigned priority.")

queue_agent = Agent(
    name="QueueAgent",
    model="gemini-2.5-flash",
    description="Analyzes the campaign brief to assign a priority for the distribution queue.",
    instruction='''You are the Queueing Agent. Your job is to assign a priority to the campaign based on its type.
    Analyze the campaign brief provided in `{campaign_brief}` and the original user intent.

    Use the following matrix to classify the campaign and assign priority:
    - **Priority 1 (Highest):** Business Campaign, Official Announcement (e.g., major product launch, company news).
    - **Priority 2 (High):** Educational (e.g., tutorial, guide, deep-dive article).
    - **Priority 3 (Medium):** Community (e.g., responding to user-generated content, engagement-focused pieces).
    - **Priority 4 (Low):** Automated Content (e.g., simple, high-frequency memes or trends).

    Based on your analysis, determine the `campaign_type` and its corresponding `priority`. Provide a brief `reasoning`. Your output must be a single JSON object matching the CampaignPriority schema.
    ''',
    output_schema=CampaignPriority,
    output_key="campaign_priority",
)


# --- Root Agent: Sequential Workflow ---

root_agent = SequentialAgent(
    name="MarketingFlowEngine",
    sub_agents=[
        parallel_ideation_layer,
        synthesis_agent,
        brand_assurance_agent,
        queue_agent,
    ],
    description="An autonomous marketing engine that takes a business intent, generates a campaign brief, validates it, and assigns it a priority for distribution.",
)