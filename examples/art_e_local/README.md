# Local ART-E Email Task

This example is a small, deterministic version of the ART-E email-search task.
It lets contributors inspect the task contract without API keys, GPUs, W&B, or
remote email infrastructure.

The task exposes three pieces that a training notebook or rollout can reuse:

- `search_emails()` returns matching messages from a local inbox fixture.
- `read_email()` loads a full message by ID.
- `score_answer()` rewards answers that include the expected answer and cite the
  supporting message.
- `rollout.py` shows how to wrap the local tools in an ART `Trajectory`.

Run the offline baseline:

```bash
python examples/art_e_local/email_task.py
```

Run the focused tests:

```bash
pytest examples/art_e_local/test_email_task.py -q
```

The notebook `art-e-local-task.ipynb` walks through the same workflow and is
intended as a lightweight companion to the serverless ART-E notebook.
