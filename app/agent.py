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
from pydantic import BaseModel

_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")

# --- Tool Data Models ---

class ImageGenerationResult(BaseModel):
    """The result of the simulated image generation tool."""
    status: str
    generated_image_path: str

class VideoGenerationResult(BaseModel):
    """The result of the simulated video generation tool."""
    status: str
    generated_video_path: str

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

def generate_image_from_prompt_and_image(prompt: str, baseline_image_path: str, tool_context: ToolContext) -> ImageGenerationResult:
    """
    Simulates generating an image from a text prompt and a baseline image using a Gemini model.
    In a real implementation, this tool would call the Gemini image generation API.
    """
    print(f"--- SIMULATING IMAGE GENERATION ---")
    print(f"Model: gemini-2.5-flash-image-preview")
    print(f"Prompt: {prompt}")
    print(f"Baseline Image: {baseline_image_path}")

    output_dir = "generated_images"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    base_name = os.path.basename(baseline_image_path)
    file_name, file_ext = os.path.splitext(base_name)
    generated_image_name = f"simulated_{file_name}_{random.randint(1000,9999)}{file_ext}"
    generated_image_path = os.path.join(output_dir, generated_image_name)

    with open(generated_image_path, "w") as f:
        f.write(f"This is a simulated image based on {baseline_image_path} and prompt: '{prompt}'")

    return ImageGenerationResult(status="success", generated_image_path=generated_image_path)

def generate_video_from_prompt_and_image(prompt: str, baseline_image_path: str, tool_context: ToolContext) -> VideoGenerationResult:
    """
    Simulates a two-step video generation from a prompt and a baseline image using Imagen and Veo models.
    In a real implementation, this tool would call the respective Google Cloud APIs.
    """
    print(f"--- SIMULATING VIDEO GENERATION (2-STEP) ---")
    print(f"Step 1: Generating initial image with Imagen...")
    print(f"   - Prompt: {prompt}")
    print(f"   - Baseline Image: {baseline_image_path}")
    print(f"Step 2: Generating video with Veo-3 using initial image...")

    output_dir = "generated_videos"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    base_name = os.path.basename(baseline_image_path)
    file_name, _ = os.path.splitext(base_name)
    generated_video_name = f"simulated_video_{file_name}_{random.randint(1000,9999)}.mp4"
    generated_video_path = os.path.join(output_dir, generated_video_name)

    with open(generated_video_path, "w") as f:
        f.write(f"This is a simulated video based on {baseline_image_path} and prompt: '{prompt}'")

    return VideoGenerationResult(status="success", generated_video_path=generated_video_path)

# --- Agent Definitions ---

visual_ideation_agent = Agent(
    name="VisualIdeationAgent",
    model="gemini-2.5-flash",
    description="Brainstorms visual concepts for marketing assets.",
    instruction="""Based on the user's business intent for an apparel shop, brainstorm a list of 3-5 distinct visual concepts or scenes.
    For each concept, describe the setting, the vibe, the model (individual or couple), and the activity.
    Example: A couple having a relaxed picnic in a sunny park, with a 'chilling, holiday vibe'.
    Output a bulleted list of these concepts.""",
    output_key="visual_concepts",
)

image_generation_agent = Agent(
    name="ImageGenerationAgent",
    model="gemini-2.5-flash",
    description="Generates a realistic still image for a marketing campaign by orchestrating multiple tools.",
    instruction="""You are an AI Image Generation specialist. Your task is to generate a marketing image.

    1.  **Get available merchandise images:** Use the `list_baseline_images` tool to see the list of available cat print t-shirt images.
    2.  **Select a baseline image:** Randomly pick one image path from the list.
    3.  **Review the visual concepts:** Read the concepts provided in `{visual_concepts}`.
    4.  **Create a detailed prompt:** Combine the user's business intent and the most compelling visual concept into a detailed creative prompt for the image generation model. The prompt should be a single, descriptive paragraph.
    5.  **Generate the image:** Call the `generate_image_from_prompt_and_image` tool with your detailed prompt and the selected baseline image path.
    6.  **Output the result:** Your final output should be ONLY the path to the generated image, extracted from the tool's result.
    """,
    tools=[list_baseline_images, generate_image_from_prompt_and_image],
    output_key="generated_image_path",
)

video_generation_agent = Agent(
    name="VideoGenerationAgent",
    model="gemini-2.5-flash",
    description="Generates a short video clip for a marketing campaign by orchestrating multiple tools.",
    instruction="""You are an AI Video Generation specialist. Your task is to generate a short marketing video.

    1.  **Get available merchandise images:** Use the `list_baseline_images` tool to see the list of available cat print t-shirt images.
    2.  **Select a baseline image:** Randomly pick one image path from the list.
    3.  **Review the visual concepts:** Read the concepts provided in `{visual_concepts}`.
    4.  **Create a detailed prompt:** Combine the user's business intent and the most compelling visual concept into a detailed creative prompt for the video generation model. The prompt should be a single, descriptive paragraph.
    5.  **Generate the video:** Call the `generate_video_from_prompt_and_image` tool with your detailed prompt and the selected baseline image path.
    6.  **Output the result:** Your final output should be ONLY the path to the generated video, extracted from the tool's result.
    """,
    tools=[list_baseline_images, generate_video_from_prompt_and_image],
    output_key="generated_video_path",
)

twitter_publisher_agent = Agent(
    name="TwitterPublisherAgent",
    model="gemini-2.5-flash",
    description="Formats the generated visual assets into a social media post for X/Twitter.",
    instruction="""You are a Social Media Manager for X/Twitter.
    Your task is to create a tweet for the apparel shop campaign.

    Use the following assets:
    - Generated Image Path: `{generated_image_path}`
    - Generated Video Path: `{generated_video_path}`

    Draft a compelling tweet that is engaging and includes relevant hashtags (like #catmerch, #tshirt, #summerstyle). Decide whether the image or the video is more impactful and state which one should be attached to the tweet.
    """,
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