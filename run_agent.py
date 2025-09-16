import asyncio
import os

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from app.agent import root_agent
from google.genai import types as genai_types


async def main():
    """Runs the agent with a sample query."""
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name="app", user_id="test_user", session_id="test_session"
    )
    runner = Runner(
        agent=root_agent, app_name="app", session_service=session_service
    )
    query = "We are launching a new summer collection for our apparel shop which focuses on t-shirts with cat prints. We need marketing assets for a social media campaign on X/Twitter. The campaign should have a relaxed, holiday vibe, targeting young adults. Use our baseline cat images to generate realistic images of people wearing the t-shirts in outdoor settings like beaches, parks, or on vacation."
    print(f"--- Running Visual Marketing Agent with query: \"{query}\" ---")
    async for event in runner.run_async(
        user_id="test_user",
        session_id="test_session",
        new_message=genai_types.Content(
            role="user",
            parts=[genai_types.Part.from_text(text=query)]
        ),
    ):
        # Print all non-user text events to see the flow
        if event.author != "user" and event.content and event.content.parts and event.content.parts[0].text:
            print(f"\n--- Output from {event.author} ---")
            print(event.content.parts[0].text)


if __name__ == "__main__":
    asyncio.run(main())

