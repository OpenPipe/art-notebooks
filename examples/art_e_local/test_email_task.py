from datetime import date
import json

from email_task import SCENARIOS
from email_task import parse_tool_call
from email_task import read_email
from email_task import score_answer
from email_task import search_emails
from email_task import scripted_baseline


def test_search_filters_by_inbox_keywords_and_date() -> None:
    results = search_emails(
        "alex@example.com",
        "Finch renewal",
        sent_before=date(2026, 3, 3),
    )

    assert [email.id for email in results] == ["msg-finch-1"]


def test_read_email_returns_none_for_unknown_message() -> None:
    assert read_email("missing-message") is None


def test_score_answer_requires_expected_answer_and_citation() -> None:
    scenario = SCENARIOS[0]

    assert score_answer(scenario, "Priya Shah owns it.", ["msg-budget-2"]) == 1.0
    assert score_answer(scenario, "Priya Shah owns it.", ["msg-budget-1"]) == 0.0
    assert score_answer(scenario, "Omar owns it.", ["msg-budget-2"]) == 0.0


def test_parse_tool_call_accepts_plain_and_fenced_json() -> None:
    command = {"tool": "search", "query": "Northwind final"}

    assert parse_tool_call(json.dumps(command)) == command
    assert parse_tool_call(f"```json\n{json.dumps(command)}\n```") == command


def test_scripted_baseline_solves_all_fixtures() -> None:
    rewards = [scripted_baseline(scenario)["reward"] for scenario in SCENARIOS]

    assert rewards == [1.0, 1.0, 1.0]
