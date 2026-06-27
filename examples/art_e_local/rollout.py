import json

import art

from email_task import Scenario
from email_task import parse_tool_call
from email_task import read_email
from email_task import score_answer
from email_task import search_emails


SYSTEM_PROMPT = """You are an email research agent.

Use one JSON command at a time:
- {"tool": "search", "query": "keywords"}
- {"tool": "read", "message_id": "msg-id"}
- {"tool": "answer", "answer": "final answer", "citations": ["msg-id"]}

Answers must cite the message IDs that support them.
"""


async def rollout(model: art.Model, scenario: Scenario) -> art.Trajectory:
    trajectory = art.Trajectory(
        messages_and_choices=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": (
                    f"Inbox: {scenario.inbox}\n"
                    f"Today: {scenario.query_date.isoformat()}\n"
                    f"Question: {scenario.question}"
                ),
            },
        ],
        metadata={"scenario_id": scenario.id},
        reward=0.0,
    )

    client = model.openai_client()
    for _ in range(6):
        completion = await client.chat.completions.create(
            model=model.get_inference_name(),
            messages=trajectory.messages(),
            max_completion_tokens=256,
        )
        choice = completion.choices[0]
        trajectory.messages_and_choices.append(choice)
        content = choice.message.content
        if not isinstance(content, str):
            trajectory.metrics["invalid_command"] = 1
            return trajectory

        try:
            command = parse_tool_call(content)
        except (ValueError, json.JSONDecodeError):
            trajectory.metrics["invalid_command"] = 1
            return trajectory

        tool = command["tool"]
        if tool == "search":
            results = search_emails(
                scenario.inbox,
                str(command.get("query", "")),
                scenario.query_date,
            )
            observation = [
                {
                    "id": email.id,
                    "sent_at": email.sent_at.isoformat(),
                    "subject": email.subject,
                }
                for email in results
            ]
        elif tool == "read":
            email = read_email(str(command.get("message_id", "")))
            observation = (
                None
                if email is None
                else {
                    "id": email.id,
                    "from": email.sender,
                    "sent_at": email.sent_at.isoformat(),
                    "subject": email.subject,
                    "body": email.body,
                }
            )
        else:
            citations = command.get("citations", [])
            if not isinstance(citations, list):
                citations = []
            answer = str(command.get("answer", ""))
            trajectory.reward = score_answer(scenario, answer, citations)
            trajectory.metrics["answered"] = 1
            return trajectory

        trajectory.messages_and_choices.append(
            {"role": "user", "content": json.dumps({"observation": observation})}
        )

    trajectory.metrics["answered"] = 0
    return trajectory
