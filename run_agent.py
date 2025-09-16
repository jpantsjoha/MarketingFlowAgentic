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
    query = "Launch a new marketing campaign for our new line of sustainable, reusable coffee cups. Our target audience is environmentally conscious millennials."
    print(f"--- Running Marketing Agent with query: \"{query}\" ---")
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

