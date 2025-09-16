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
import random
from typing import List

import google.auth
from google.adk.agents import Agent, ParallelAgent, SequentialAgent
from google.adk.tools import FunctionTool, ToolContext

_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")

# --- Tools ---

def list_baseline_images(tool_context: ToolContext) -> List[str]:
    """
    Lists the available baseline images of the merchandise.
    This tool should be used to select a reference image for generation.
    """
    image_dir = "images_baseline"
    try:
        files = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.endswith(".png")]
        return files
    except FileNotFoundError:
        return ["Error: 'images_baseline' directory not found."]

# --- Agent Definitions ---

visual_ideation_agent = Agent(
    name="VisualIdeationAgent",
    model="gemini-2.5-flash",
    description="Brainstorms visual concepts for marketing assets.",
    instruction='''Based on the user's business intent for an apparel shop, brainstorm a list of 3-5 distinct visual concepts or scenes.
    For each concept, describe the setting, the vibe, the model (individual or couple), and the activity.
    Example: A couple having a relaxed picnic in a sunny park, with a 'chilling, holiday vibe'.
    Output a bulleted list of these concepts.''',
    output_key="visual_concepts",
)

image_generation_agent = Agent(
    name="ImageGenerationAgent",
    model="gemini-2.5-flash",
    description="Generates a realistic still image for a marketing campaign.",
    instruction='''You are an AI Image Generation specialist. Your task is to generate a marketing image.

    1.  **Review the visual concepts:** Read the concepts provided in `{visual_concepts}`.
    2.  **Select a concept:** Choose the most compelling concept for a still image.
    3.  **Select a baseline image:** Use the `list_baseline_images` tool to see available merchandise images and select one randomly.
    4.  **Simulate Generation:** Combine the selected concept and baseline image into a final prompt.
    5.  **Output the Result:** State which baseline image you used and describe the final generated image. You MUST NOT actually generate an image, only describe it.
    Start your output with 'SIMULATED IMAGE:'.
    ''',
    tools=[list_baseline_images],
    output_key="generated_image_description",
)

video_generation_agent = Agent(
    name="VideoGenerationAgent",
    model="gemini-2.5-flash",
    description="Generates a short video for a marketing campaign.",
    instruction='''You are an AI Video Generation specialist (simulated by the Veo-3 Gemini model).

    1.  **Review the visual concepts:** Read the concepts provided in `{visual_concepts}`.
    2.  **Select a concept:** Choose the most compelling concept for a short video.
    3.  **Simulate Generation:** Describe a 5-10 second video clip based on this concept. Describe the scene, camera movement, and audio.
    4.  **Output the Result:** You MUST NOT actually generate a video, only describe it.
    Start your output with 'SIMULATED VIDEO:'.
    ''',
    output_key="generated_video_description",
)

twitter_publisher_agent = Agent(
    name="TwitterPublisherAgent",
    model="gemini-2.5-flash",
    description="Formats the generated visual assets into a social media post for X/Twitter.",
    instruction='''You are a Social Media Manager for X/Twitter.
    Your task is to create a tweet for the apparel shop campaign.

    Use the following assets:
    - Image Description: `{generated_image_description}`
    - Video Description: `{generated_video_description}`

    Draft a compelling tweet that is engaging, includes relevant hashtags (like #catmerch, #tshirt, #summerstyle), and has a clear call to action.
    Mention which visual asset (image or video) would be attached.
    ''',
    output_key="twitter_post",
)

# --- Root Agent: Sequential Workflow ---

root_agent = SequentialAgent(
    name="VisualMarketingAgent",
    sub_agents=[
        visual_ideation_agent,
        ParallelAgent(
            name="VisualGenerationLayer",
            sub_agents=[
                image_generation_agent,
                video_generation_agent,
            ],
        ),
        twitter_publisher_agent,
    ],
    description="Generates visual marketing assets for an apparel shop and formats them for social media.",
)
