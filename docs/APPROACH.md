# How to Approach This Lab

There are no prompts this time. This guide gives you **recommendations and questions to ask
yourself** at each phase. The answers are yours to find and decide.

If you need a refresher on what each phase does and its best practices, go back to
`docs/WORKFLOW.md` from Lab 1, or the Spec Kit docs: <https://github.github.com/spec-kit/>

---

## The big picture

```
            ┌──────────────── once ────────────────┐
            │            constitution              │
            └──────────────────────────────────────┘
                   │                       │
   Feature 1 (branch 001)          Feature 2 (branch 002)
   specify → clarify → plan        specify → clarify → plan
   → tasks → analyze → implement   → tasks → analyze → implement
            │                              ▲
            └── merge into main ───────────┘
```

**Finish Feature 1 completely, and merge it, before you specify Feature 2.** Feature 2 must be
written against the application that actually exists, not the one you imagine. Discovering that
your Feature 1 design doesn't fit Feature 2 is not a failure. It's one of the things this lab is
meant to teach. Record it in your reflection.

**Before you write anything, open the three data files and read them line by line.** Write down
everything that seems unusual. Your specs must account for all of it.

---

## Constitution

The constitution applies to **both** features, so think about rules that should hold for any
feature you might add later.

Ask yourself:
- What language version, test framework, and project layout will you use? How is the CLI run?
- How strict is the rule on graph libraries? Where exactly are they allowed?
- What does "tested" mean in this project? What must every feature's tests cover?
- How should the CLI behave on errors? (Exit codes? Messages to stdout or stderr? Tracebacks?)
- How do you stop the agent from over-engineering a small CLI?

Recommendations:
- Write principles that can be **checked**. "Code must be clean" can't be checked. "Every
  acceptance scenario in a spec has at least one automated test" can.
- Keep it to a handful of principles. You'll be re-reading it for both features.

---

## Feature 1 — Specify

The spec describes **what** the user can do and **what** happens, never **how**.

Ask yourself:
- Who uses this CLI, and what do they want to know about a graph when they look at it?
- What does "display" mean to that user? What information must be shown, and in what form?
- What exactly is in the input file, and what is allowed to be in it? What isn't?
- What counts as a vertex? Can a vertex exist without any edges?
- What makes two vertex names "the same"?
- What happens with data that is unusual, but not obviously wrong? And with data that is
  clearly wrong (a missing file, a malformed row, an empty file)?
- Does the user need anything else to understand the graph, like counts or summaries?

Recommendations:
- Write **acceptance scenarios that use the provided data files**. "Given `small-dag.csv`, when
  the user displays it, then …" is concrete and testable.
- Check the spec for technology words: Python, dict, class, argparse, file paths. Remove them.
- Look for the `[NEEDS CLARIFICATION]` markers the agent leaves. Then look for the gaps it
  **didn't** mark. Those are more dangerous.

## Feature 1 — Clarify

This is where the important decisions are made. Don't just pick the agent's recommended answer.

Recommendations:
- Before running clarify, write your own list of open questions. After it finishes, compare. If
  something on your list wasn't asked, run clarify again with a focus, or update the spec
  directly.
- For each decision, ask: **would a user of this tool be surprised by this behavior?**
- Every decision must end up in the **requirements and acceptance scenarios**, not just in the
  Clarifications Q&A.

## Feature 1 — Plan

This is where you choose **how**. Since you can't use graph libraries, the most important
decision is **how to represent the graph in memory**.

Ask yourself:
- Which representations exist? What does each cost in memory, and in time for the operations
  you need?
- Which operations does Feature 1 need? Which will Feature 2 need? (You know Feature 2 is
  coming. A good plan doesn't implement it yet, but it shouldn't make it hard either.)
- How will you know the output for a data file is correct?

Recommendations:
- Make sure `research.md` records the alternatives you rejected and why. You'll need this for
  your reflection.
- Check the plan's constitution check. Push back on anything you didn't ask for.

## Feature 1 — Tasks, Analyze, Implement

Recommendations:
- In `tasks.md`, check that every functional requirement has at least one task, and that tests
  come before the code they test.
- Fix every CRITICAL and HIGH finding from analyze **in the document where it belongs**, then
  regenerate what depends on it.
- During implement, read every approval request. Stop the agent if it does something that isn't
  in `tasks.md`.
- After implementing, run the CLI yourself on **all three data files** and compare the output to
  your spec, scenario by scenario.
- Commit after each phase. Merge into `main` when Feature 1 is done.

---

## Feature 2 — Specify and Clarify

Topological sorting sounds simple to describe. The spec is where you find out it isn't.

Ask yourself:
- When does a topological order **not exist**? What does the user see then? What information
  would actually help them fix their data?
- Is there always **exactly one** valid order? If not, which one does your application output?
  Does it matter whether it's the same every time?
- How will your tests check correctness if more than one answer is valid?
- How does the user ask for a topological order? How does it fit with the CLI you built in
  Feature 1?
- Does anything from Feature 1 need to change? If so, is it a change to Feature 1's **spec**,
  or only to its code?

Recommendations:
- Try each data file in your head before writing scenarios. What should the output be for each
  one?
- Remember that the spec describes behavior, not an algorithm. "Uses Kahn's algorithm" belongs
  in the plan, not the spec.

## Feature 2 — Plan, Tasks, Analyze, Implement

Ask yourself:
- Which algorithms exist for topological sorting? How does each one detect that no valid order
  exists? Which one makes it easier to give the user the information your spec requires?
- What is the time complexity of your solution, given your graph representation?

Recommendations:
- Use a graph library as a **test oracle** (allowed only in tests): check that every order your
  application produces is valid, and that it reports a problem exactly when the library says
  there is one.
- Run analyze, fix findings, implement, and test manually on all three files again.

---

## Signs you're doing it wrong

| Sign | What it means |
|------|---------------|
| You ran `/speckit.implement` and haven't opened `spec.md` | The agent's guesses are now your requirements. |
| Your Clarifications section is empty or has one question | You didn't look hard enough at the data. |
| `spec.md` mentions dictionaries, classes or Python modules | Implementation leaked into the spec. |
| The CLI output for a data file surprises you | Either the spec didn't cover it, or the code doesn't follow the spec. Find out which. |
| You fixed a behavior in code but not in the spec | The spec is now wrong. Fix it. |
| One commit contains three phases | Nobody (including you) can see your process. |
