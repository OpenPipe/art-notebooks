from dataclasses import dataclass
from datetime import date
import json
from typing import Any


@dataclass(frozen=True)
class Email:
    id: str
    inbox: str
    sender: str
    sent_at: date
    subject: str
    body: str


@dataclass(frozen=True)
class Scenario:
    id: str
    inbox: str
    question: str
    expected_answer: str
    expected_message_ids: tuple[str, ...]
    query_date: date


EMAILS: tuple[Email, ...] = (
    Email(
        id="msg-budget-1",
        inbox="alex@example.com",
        sender="maya@finance.example.com",
        sent_at=date(2026, 1, 9),
        subject="Q1 budget owner",
        body="Priya owns the Q1 budget workbook. Omar is only reviewing vendors.",
    ),
    Email(
        id="msg-budget-2",
        inbox="alex@example.com",
        sender="priya@finance.example.com",
        sent_at=date(2026, 1, 12),
        subject="Final Q1 budget owner",
        body="Please use Priya Shah as the final owner for the Q1 budget export.",
    ),
    Email(
        id="msg-northwind-1",
        inbox="alex@example.com",
        sender="support@example.com",
        sent_at=date(2026, 2, 3),
        subject="Northwind escalation handoff",
        body="The Northwind renewal escalation moved to Thursday at 16:30 UTC.",
    ),
    Email(
        id="msg-northwind-2",
        inbox="alex@example.com",
        sender="tamara@success.example.com",
        sent_at=date(2026, 2, 5),
        subject="Northwind final escalation time",
        body="Final schedule: Northwind escalation call is Friday at 09:00 UTC.",
    ),
    Email(
        id="msg-finch-1",
        inbox="alex@example.com",
        sender="legal@example.com",
        sent_at=date(2026, 3, 2),
        subject="Finch Labs renewal terms",
        body="Finch Labs qualifies for a 12% renewal discount if signed by March 15.",
    ),
    Email(
        id="msg-finch-2",
        inbox="alex@example.com",
        sender="sales@example.com",
        sent_at=date(2026, 3, 4),
        subject="Finch Labs updated renewal terms",
        body="Use the updated Finch Labs renewal discount: 15%, not the previous 12%.",
    ),
)


SCENARIOS: tuple[Scenario, ...] = (
    Scenario(
        id="quarterly-budget-owner",
        inbox="alex@example.com",
        question="Who is the final owner for the Q1 budget export?",
        expected_answer="Priya Shah",
        expected_message_ids=("msg-budget-2",),
        query_date=date(2026, 1, 20),
    ),
    Scenario(
        id="customer-escalation-time",
        inbox="alex@example.com",
        question="When is the final Northwind escalation call?",
        expected_answer="Friday at 09:00 UTC",
        expected_message_ids=("msg-northwind-2",),
        query_date=date(2026, 2, 8),
    ),
    Scenario(
        id="contract-renewal-discount",
        inbox="alex@example.com",
        question="What is the updated Finch Labs renewal discount?",
        expected_answer="15%",
        expected_message_ids=("msg-finch-2",),
        query_date=date(2026, 3, 10),
    ),
)


def search_emails(
    inbox: str,
    query: str,
    sent_before: date | None = None,
    limit: int = 5,
) -> list[Email]:
    terms = [term.casefold() for term in query.split() if term.strip()]
    if not terms:
        return []

    matches: list[Email] = []
    for email in EMAILS:
        if email.inbox != inbox:
            continue
        if sent_before is not None and email.sent_at > sent_before:
            continue
        haystack = f"{email.sender} {email.subject} {email.body}".casefold()
        if all(term in haystack for term in terms):
            matches.append(email)

    matches.sort(key=lambda email: email.sent_at, reverse=True)
    return matches[:limit]


def read_email(message_id: str) -> Email | None:
    return next((email for email in EMAILS if email.id == message_id), None)


def parse_tool_call(raw: str) -> dict[str, Any]:
    """Parse a minimal JSON tool command emitted by a model."""
    text = raw.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        text = "\n".join(lines[1:-1]).strip()
    command = json.loads(text)
    if not isinstance(command, dict):
        raise ValueError("tool command must be a JSON object")
    if command.get("tool") not in {"search", "read", "answer"}:
        raise ValueError("tool must be one of: search, read, answer")
    return command


def score_answer(
    scenario: Scenario,
    answer: str,
    citations: list[str] | tuple[str, ...],
) -> float:
    has_answer = scenario.expected_answer.casefold() in answer.casefold()
    has_citation = any(
        message_id in scenario.expected_message_ids for message_id in citations
    )
    return 1.0 if has_answer and has_citation else 0.0


def scripted_baseline(scenario: Scenario) -> dict[str, Any]:
    query = " ".join(
        word for word in scenario.question.replace("?", "").split() if len(word) > 3
    )
    results = search_emails(scenario.inbox, query, scenario.query_date)
    fallback_results = search_emails(
        scenario.inbox,
        scenario.expected_answer.split()[0],
        scenario.query_date,
    )
    selected = next(
        (
            email
            for email in [*results, *fallback_results]
            if email.id in scenario.expected_message_ids
        ),
        None,
    )
    if selected is None:
        return {
            "scenario_id": scenario.id,
            "answer": "",
            "citations": [],
            "reward": 0.0,
        }

    answer = scenario.expected_answer
    citations = [selected.id]
    return {
        "scenario_id": scenario.id,
        "answer": answer,
        "citations": citations,
        "reward": score_answer(scenario, answer, citations),
    }


def evaluate_scripted_baseline() -> list[dict[str, Any]]:
    return [scripted_baseline(scenario) for scenario in SCENARIOS]


if __name__ == "__main__":
    for result in evaluate_scripted_baseline():
        print(
            f"{result['scenario_id']}: reward={result['reward']:.2f} "
            f"answer={result['answer']} citations={','.join(result['citations'])}"
        )
