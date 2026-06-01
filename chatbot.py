import os
import argparse
from typing import List
from dotenv import load_dotenv

from src.core.openai_provider import OpenAIProvider
from src.core.gemini_provider import GeminiProvider
from src.telemetry.metrics import tracker
from src.telemetry.logger import logger


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


def _baseline_prompt(user_input: str) -> str:
    return (
        "You are a helpful travel assistant. Answer directly without using tools. "
        "If information is missing, make a best guess and explain assumptions.\n\n"
        f"User request: {user_input}"
    )


def _run_cases(provider, cases: List[str]) -> None:
    for index, prompt in enumerate(cases, start=1):
        logger.log_event("CHATBOT_CASE_START", {"index": index, "prompt": prompt})
        response = provider.generate(_baseline_prompt(prompt))
        tracker.track_request(
            provider=response.get("provider", "unknown"),
            model=provider.model_name,
            usage=response.get("usage", {}),
            latency_ms=response.get("latency_ms", 0),
        )
        print(f"\n=== Case {index} ===")
        print(f"User: {prompt}")
        print("Assistant:", response.get("content", ""))
        logger.log_event(
            "CHATBOT_CASE_END",
            {
                "index": index,
                "latency_ms": response.get("latency_ms", 0),
                "tokens": response.get("usage", {}),
            },
        )


def _interactive_loop(provider) -> None:
    print("Chatbot baseline (type 'exit' to quit)")
    while True:
        user_input = input("User: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            break
        response = provider.generate(_baseline_prompt(user_input))
        tracker.track_request(
            provider=response.get("provider", "unknown"),
            model=provider.model_name,
            usage=response.get("usage", {}),
            latency_ms=response.get("latency_ms", 0),
        )
        print("Assistant:", response.get("content", ""))


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Baseline chatbot runner")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    args = parser.parse_args()

    provider = _build_provider()
    cases = [
        "Bay HAN to SGN ngay 2026-06-12. Gia re nhat la bao nhieu va tong chi phi voi 10% thue?",
        "Toi can ve HAN -> SGN ngay 2026-06-12, hanh ly 20kg, ngan sach 2.3 trieu.",
        "Chi chon Vietnam Airlines. Ve bay HAN -> DAD sang som 2026-06-12.",
        "Toi muon 2 ve HAN -> SGN, uu tien ve co hoan/doi, tinh tong gia.",
        "Bay SGN -> HAN ngay 2026-06-13, toi muon ve som nhat co the.",
    ]

    if args.interactive:
        _interactive_loop(provider)
        return

    _run_cases(provider, cases)


if __name__ == "__main__":
    main()
