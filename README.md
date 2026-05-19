# good-habits-skill

[中文版 / Chinese README](./README_zh.md)

> A loadable Skill that injects "good working habits" into AI Agents (Claude / Claude Code etc.). It makes the Agent naturally follow a disciplined workflow in development scenarios, and uses a local Q&A archive to mitigate the **"every new chat starts from amnesia"** problem.

---

## Why does this Skill exist?

The session-level context of an LLM Agent is **volatile**:

- Close the IDE and reopen → context gone.
- Switch to a new chat → context gone.
- The user is forced to re-explain every time: "We previously decided …", "Last time we got bitten by XXX …".

This is not just a UX issue — it directly hurts output quality. Without past decisions in view, the Agent reinvents wheels, overturns settled designs, and steps on the same rakes again.

**This Skill's approach: let the Agent write its own work log, and read it back at the start of the next session.** The whole mechanism is purely local with zero external dependencies — the work log is just a few Markdown files inside the project, readable and editable by both humans and Agents, and travels with the repo.

---

## The six habits at a glance

| # | Habit | When it triggers | One-line description |
| - | --- | --- | --- |
| 1 | Plan first, code second | User asks for code change / hands over a PRD | Produce a Markdown implementation plan for review first; **wait for explicit approval** before coding |
| 2 | Multi-option comparison | A feature has multiple viable implementations | List pros and cons of every option in a table; let the user pick |
| 3 | Auto-record Q&A | After every code change | Persist a Q&A entry to `.good-habits/YYYY-MM-DD-HH-mm-ss.md` |
| 4 | Two-party publish ordering reminder | Anything involving 2nd-party packages / SDKs / starter version coupling | Spell out dependency order in a table + a standard Maven snippet |
| 5 | Recap history at session start | First substantive request about this project in a new session | Proactively scan the latest entries in `.good-habits/` to restore context before answering |
| 6 | Java comment standard | Creating a Java class / enum / interface / method / static field / instance field | Fill in Javadoc per the fixed `@author 鹤童 / @desc / @date` format |

> **Habits 3 and 5 form a pair**: the writer side accumulates knowledge, the reader side restores context across sessions — this is the core mechanism by which the Skill alleviates the "amnesia on new chat" problem.

---

## Directory layout

```
good-habits-skill/
├── SKILL.md                          # Skill entry point (YAML frontmatter + triggers/behaviors for the six habits)
├── README.md                         # This document (English, default)
├── README_zh.md                      # Chinese version
├── scripts/
│   ├── create-qa-record.sh           # Habit 3: Bash version of the auto-record script
│   └── create-qa-record.py           # Habit 3: Python version (when Bash is unavailable)
├── references/
│   ├── plan-template.md              # Habit 1: implementation plan template
│   ├── comparison-template.md        # Habit 2: multi-option comparison template
│   ├── maven-release-order.md        # Habit 4: detailed reference on 2nd-party publish order
│   └── java-comment-standard.md      # Habit 6: Java comment samples and self-check list
└── assets/
    └── qa-template.md                # Habit 3: Markdown template for a Q&A entry
```

---

## How to use

### 1. Load the Skill into your Agent

Place this directory wherever your Agent discovers Skills (the exact path depends on the host — for example, Claude Code's `~/.claude/skills/` or the project-level `.claude/skills/`). On startup, the Agent reads the `SKILL.md` frontmatter and uses the `description` to decide when to invoke it.

### 2. Just collaborate normally

Once loaded, **the user does nothing extra** — the Agent acts at these moments automatically:

- You state a requirement → Agent gives a plan for you to review (Habit 1).
- Multiple implementations exist → Agent lists them in a table for you to choose (Habit 2).
- Code change finished → Agent writes a Q&A entry to disk (Habit 3).
- 2nd-party package question → Agent provides a dependency table + Maven snippet (Habit 4).
- You start a new chat about the project → Agent reads `.good-habits/` first, then answers (Habit 5).
- You write Java code → Agent automatically lays down Javadoc/comments per the standard (Habit 6).

### 3. A `.good-habits/` directory appeared in my project — what now?

The first time Habit 3 triggers, the Agent creates `.good-habits/` in your project root. **Whether to put it under version control is up to you**:

- **Commit it**: team members (and their Agents) share the same project memory — suitable for multi-developer projects.
- **Add to `.gitignore`**: personal/local use only — keeps history clean.

The Agent will not make this choice for you; on first creation it asks once.

### 4. Manual script invocation (optional)

`scripts/create-qa-record.sh` also supports manual invocation:

```bash
./scripts/create-qa-record.sh /path/to/your/project \
  "Add login feature" \
  "JWT + Redis cache" \
  "src/auth.ts: new login endpoint" \
  "Need to configure JWT_SECRET in production"
```

This creates a timestamp-named Markdown file under `/path/to/your/project/.good-habits/` and prints the absolute path to stdout. The Python version works the same way:

```bash
python3 scripts/create-qa-record.py /path/to/your/project \
  --question "Add login feature" \
  --solution "JWT + Redis cache" \
  --files "src/auth.ts: new login endpoint" \
  --notes "Need to configure JWT_SECRET in production"
```

---

## What does a Q&A record file look like?

After every code change, a new file appears under `.good-habits/`, e.g. `2026-05-14-15-32-08.md`:

```markdown
# Q&A Record - 2026-05-14-15-32-08

> Auto-generated by good-habits-skill

## User Question
Add login functionality, supporting both account-password and SMS-code login.

## Implementation
JWT-based auth + Redis-cached SMS codes. Frontend split into two components: LoginForm / SmsLoginForm.

## Files Changed (summary)
- src/auth/jwt.ts: added issueToken / verifyToken
- src/auth/sms.ts: added SMS code dispatch and verification
- src/pages/Login.tsx: split into two login modes

## Notes
- JWT_SECRET and SMS gateway AK/SK must be configured in production.
- SMS code TTL tentatively 5 minutes; revisit after ops feedback.
```

In the next chat, the Agent automatically sees this — you don't have to re-explain.

---

## Relationship with platform-level Memory

If your Agent client (such as Claude Code) already enables platform-level memory, this Skill **runs in parallel without conflict**:

| Dimension | Platform Memory | `.good-habits/` (this Skill) |
| --- | --- | --- |
| Granularity | Cross-project, about "the user" | Single project, about "the work stream" |
| Storage | Platform account | Inside the project repo |
| Visibility | Yourself only | Team (if committed) |
| Content nature | User profile / preferences / long-term consensus | Requirements / decisions / changes / pitfalls |
| Travels with the project | No | Yes |

In short: **Memory remembers "who you are and how you work"; `.good-habits/` remembers "what happened in this project".**

---

## FAQ

**Q: Will the Agent really follow these habits automatically? Or do I have to remind it every time?**
A: Once the Skill is loaded, the Agent should proactively detect the trigger conditions and act. If you find it not following them, the most common cause is that the Skill was not loaded properly, or the host has limited Skill support — try saying "please follow good-habits-skill" at the start of the chat.

**Q: `.good-habits/` keeps growing — what should I do?**
A: Leave it as is. By default the Agent only reads the latest 3–5 entries; older entries stay as a "project archive" that humans can browse anytime. If it gets too large, archiving them to a subdirectory (e.g. `.good-habits/2025/`) is fine and won't affect the Skill.

**Q: Can I disable a particular habit?**
A: Yes. Either remove the relevant section in `SKILL.md`, or just tell the Agent at runtime: "skip Habit 1 this time, just code directly".

**Q: Won't Habit 5 slow down responses, since every new chat reads a bunch of files first?**
A: It only triggers **once per new chat, on the first substantive request**, and only the latest 3–5 entries are read. The cost is far less than re-explaining background to the Agent.

---

## Versions

- **v1.2.0** (2026-05-18): added Habit 6 (Java comment standard), covering the comment-format constraints for seven element categories: classes / enums / interfaces / methods / static fields / instance fields / method-local variables.
- **v1.1.0** (2026-05-14): added Habit 5 (session-start recap); clarified the "project memory layer" positioning.
- **v1.0.0**: initial release with Habits 1–4.

## License

MIT
