import os
import sys
import argparse
from typing import List
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.openai_provider import OpenAIProvider
from src.core.gemini_provider import GeminiProvider
from src.agent.agent import ReActAgent
from src.tools import tool_specs


def _build_provider():
    provider_name = os.getenv("DEFAULT_PROVIDER", "openai").lower()
    if provider_name in {"gemini", "google"}:
        api_key = os.getenv("GEMINI_API_KEY")
        model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        return GeminiProvider(model_name=model, api_key=api_key)
    if provider_name == "local":
        raise ValueError(
            "The local provider has been removed. Set DEFAULT_PROVIDER to 'openai' or 'gemini'."
        )

    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-4o")
    return OpenAIProvider(model_name=model, api_key=api_key)


def _run_cases(agent: ReActAgent, cases: List[str]) -> None:
    for index, prompt in enumerate(cases, start=1):
        print(f"\n=== Case {index} ===")
        print(f"User: {prompt}")
        answer = agent.run(prompt)
        print("Assistant:", answer)


def _interactive_loop(agent: ReActAgent) -> None:
    print("ReAct agent (type 'exit' to quit)")
    while True:
        user_input = input("User: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            break
        answer = agent.run(user_input)
        print("Assistant:", answer)


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="ReAct agent runner")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    args = parser.parse_args()

    provider = _build_provider()
    agent = ReActAgent(llm=provider, tools=tool_specs, max_steps=5)

    cases = [
        "Bay HAN to SGN ngay 2026-06-12. Gia re nhat la bao nhieu va tong chi phi voi 10% thue?",
        "Toi can ve HAN -> SGN ngay 2026-06-12, hanh ly 20kg, ngan sach 2.3 trieu.",
        "Chi chon Vietnam Airlines. Ve bay HAN -> DAD sang som 2026-06-12.",
        "Toi muon 2 ve HAN -> SGN, uu tien ve co hoan/doi, tinh tong gia.",
        "Bay SGN -> HAN ngay 2026-06-13, toi muon ve som nhat co the.",
    ]

    if args.interactive:
        _interactive_loop(agent)
        return

    _run_cases(agent, cases)


if __name__ == "__main__":
    main()
