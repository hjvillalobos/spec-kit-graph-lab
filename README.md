# Spec-Driven Development Lab 2: Graphs and Topological Sorting

In the first lab you followed a step-by-step guide with ready-made prompts. **This time there are
no prompts.** You will take a short, incomplete description of a problem and drive the whole
Spec-Driven Development process yourself: write the constitution, write the specs, find the
ambiguities, make decisions, review every document, and only then let the agent implement.

- Spec Kit: <https://github.com/github/spec-kit>
- Spec Kit docs: <https://github.github.com/spec-kit/>
- How to approach this lab: [`docs/APPROACH.md`](docs/APPROACH.md) ← **read this before starting**

---

## Setup

Keep using **Spec Kit**, the same way you did in the first lab. You may use **any coding agent
that Spec Kit supports** (Gemini CLI, GitHub Copilot, Claude Code, Codex, …). Initialize a new
project with the integration for your agent of choice.

State which agent you used in your `REFLECTION.md`.

---

## The problem

Many real systems are graphs of dependencies:

- a university curriculum, where some courses are prerequisites of others;
- a software build, where packages depend on other packages;
- a project plan, where some tasks must finish before others start.

You will build a **command-line application in Python** that loads these kinds of dependency
graphs from a file, displays them, and computes a valid order in which to process them.

The work is split into **two features**, and each one goes through the **full** Spec Kit workflow
on its own branch.

### Feature 1 — Directed graphs

Users can **load a directed, unweighted graph** from a file and **display it**: its vertices and
its edges.

That's all the description you get. Everything else (the input format details, how the graph is
displayed, what happens with unusual or invalid data, what the CLI looks like) is for you to
specify, clarify and decide.

### Feature 2 — Topological sorting

Users can ask the application for a **topological order** of a loaded graph: an ordering of the
vertices in which every vertex comes before all the vertices it points to.

This feature **builds on Feature 1**. It is a separate spec, on a separate branch, written after
Feature 1 is finished and merged.

---

## Sample data

Three files are provided in [`data/`](data/). Each is a CSV with a header row `source,target`;
each row is a directed edge from `source` to `target`.

| File | What it represents |
|------|--------------------|
| [`small-dag.csv`](data/small-dag.csv) | Getting dressed in the morning: which garment must be put on before which. Small, for debugging. |
| [`cs-curriculum.csv`](data/cs-curriculum.csv) | A computer science curriculum: `source` is a prerequisite of `target`. |
| [`build-with-cycle.csv`](data/build-with-cycle.csv) | Packages in a software project: `source` must be built before `target`. |

These files reflect real-world data: **look at them carefully**. Not every row is as tidy as it
first appears, and your specs must say what the application does with everything it can find in
them. You may create additional data files for your tests.

---

## Constraints

1. **Python 3.11+**, command-line application.
2. **Implement the graph and the algorithms yourselves.** Do not use graph libraries
   (NetworkX, igraph, graph-tool, `graphlib`, `scipy.sparse.csgraph`, …) in the application code.
   Choosing how to represent the graph is part of your plan, and you must justify it.
3. **Graph libraries ARE allowed in tests**, as an oracle. For example, you may use NetworkX
   in a test to check that the order your application produces is a valid topological order.
   This is how professionals verify algorithm implementations.
4. **Automated tests are required** for every acceptance scenario in your specs.
5. Each feature **must go through every phase**: constitution (once, updated if needed) →
   specify → clarify → plan → tasks → analyze → implement.
6. **The spec and the code must agree.** If you find a bug, decide whether the code or the spec is
   wrong. Fix the spec first if needed, then the code. Never leave them disagreeing.

---

## Deliverables

Submit a link to your repository (all branches pushed). It must contain:

1. `.specify/memory/constitution.md`
2. `specs/001-*/` and `specs/002-*/`, each with `spec.md` (including a **Clarifications**
   section), `plan.md`, `research.md`, `data-model.md`, `tasks.md` and any other generated files
3. The working CLI and its tests, all passing
4. **A commit history that shows the process**: at least one commit per phase, per feature. A
   repository with one giant commit will be graded as if the process was skipped.
5. `REFLECTION.md` (1–2 pages) answering:
   - Which agent did you use? Did anything about it help or get in the way?
   - List the clarification questions for each feature and your decisions. Which decision
     was hardest, and why?
   - Which unusual things did you find in the sample data, and what does your application do
     with each one?
   - How did you represent the graph, and what alternatives did you reject? Did that choice
     hold up when you got to Feature 2, or did you have to change it?
   - What did `/speckit.analyze` report for each feature, and what did you change?
   - Describe one moment where the agent did something different from what you intended. Was
     the spec ambiguous, or did the agent ignore it?

> ❌ Do not commit API keys or any other secrets.

---

## Optional extension — Feature 3

Run a third feature through the full workflow: **weighted graphs with shortest paths
(Dijkstra)** or **minimum spanning trees (Kruskal/Prim)**. Before you start, ask yourself
whether your graph representation can support weights without rewriting Features 1 and 2. If it
can't, what would you change in your plan from Feature 1?
