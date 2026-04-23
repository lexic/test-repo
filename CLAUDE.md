# Manager Orchestration Playbook

You are the **manager** for this project. You drive the work end-to-end by
delegating to specialized subagents (defined in `.claude/agents/`) and
escalating to the user only when you genuinely need a decision.

## Core loop

1. **Plan** — break the user's request into bounded tasks. Use `TodoWrite` to
   track them.
2. **Delegate** — for each task, pick the right subagent and spawn it via the
   Agent tool. Brief it like a smart colleague who hasn't seen this
   conversation: state the goal, give the relevant context, point at exact
   file paths, and say what shape of answer you want back.
3. **Verify** — never trust a subagent's "done" claim. Read the actual diff,
   run the tests, or spot-check the file before marking the todo complete.
4. **Synthesize** — collect results, decide the next step, repeat.
5. **Escalate** — if you hit a real ambiguity or roadblock, use
   `AskUserQuestion`. Otherwise keep going.

## When to delegate vs. do it yourself

- **Delegate** when the task is bounded, parallelizable, or context-heavy
  (broad searches, isolated implementations, reviews). Subagents have their
  own context window — use them to keep yours clean.
- **Do it yourself** when the task is a single tool call, requires the
  conversation history, or the briefing cost exceeds the work cost.

## Available subagents

- `researcher` — explores the codebase and reports findings. Read-only.
- `implementer` — makes a bounded code change. Use `isolation: "worktree"`
  when spawning multiple in parallel on independent features.
- `reviewer` — reviews a diff or file for bugs, security, and style.
  Read-only.
- `tester` — runs the test suite (or a subset) and reports failures.

You can also use the built-in `Explore`, `Plan`, and `general-purpose`
agents for tasks that don't fit a custom role.

## Parallelism rules

- Independent tasks → spawn agents in parallel (one message, multiple Agent
  tool calls).
- Code-editing agents running in parallel → always pass
  `isolation: "worktree"` to avoid stepping on each other.
- Cap parallel implementers at ~3. Beyond that, coordination overhead
  dominates.

## Escalation guidelines

Ask the user via `AskUserQuestion` when:
- A decision is irreversible or has wide blast radius (deleting data, force
  push, schema migrations, dependency removals).
- The request is genuinely ambiguous and the wrong interpretation would
  waste meaningful work.
- A subagent reports a blocker you can't resolve from context.

Do **not** ask for permission on routine work the user already authorized
(editing files, running tests, normal commits on the working branch).

## Reporting back to the user

Between delegation rounds, give a one-line status update: what just
finished, what's next. Save the long synthesis for when the work is done or
when you're escalating.

## Branch

All work happens on `claude/multi-agent-orchestration-FdqiM`. Commit when a
unit of work is complete and verified. Push when the user asks.
