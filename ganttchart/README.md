# iGanttChart Skill — create Gantt charts and project schedules with AI

English | [日本語](README.ja.md)

Use the **ganttchart** Skill to turn a project plan into tasks, dates, and dependencies, then generate a content-embedded URL that opens an editable preview in **iGanttChart**. The app ID is `ganttchart`; this Skill is separate from the `ganttchartai` app.

[Skill guide on tanaike.jp](https://tanaike.jp/app/ganttchart/skill/?hl=en) · [Open iGanttChart](https://ganttchart.tanaike.jp/) · [AI instructions](SKILL.md) · [All app Skills](../README.md)

## What you can create

- A website launch schedule with planning, design, implementation, and review tasks.
- An event preparation timeline with a deadline and fixed dates.
- A project work breakdown with parent and child tasks and task dependencies.

Review the proposed dates and dependencies before relying on the schedule. AI-generated plans may need corrections.

## Create through conversation

Start with what you want to make; you do not need a finished specification. For example: “I want a website launch schedule for next month. Ask me about anything missing.” Answer the assistant's questions, then request changes such as “split implementation into smaller tasks” or “allow another week for review.” When the plan is ready, ask for a URL that opens it in the app.

### Try it without installing a Skill

Paste the app's instructions URL into the prompt together with your request. Ask the assistant to follow the linked data reference and URL tool as well. For iGanttChart, use:

> Read https://github.com/y-tanaike/public_skills/blob/main/ganttchart/SKILL.md and follow its linked data reference and URL tool. I want a Gantt chart for launching a website next month. Help me organize tasks and dates through conversation, asking about missing information. Write the task names in English and return a URL I can open in iGanttChart when the plan is ready.

You can paste the instructions themselves instead. No Skill installation is required for this approach. Matching [English](examples/sample.en.json) and [Japanese](examples/sample.ja.json) examples are included.

Use an AI environment that can retrieve the instructions and reference files and run Python or equivalent code to generate the URL. If it cannot read URLs, provide the instructions and referenced files directly. Pasting a URL does not add browsing or code-execution capabilities to an assistant.

### Install the Skill for repeat use

Add the entire app directory to an AI environment that supports Skills, keeping `SKILL.md`, `scripts/`, `references/`, and `examples/` together. Installation depends on the environment. Once installed and available, you can ask:

> Use the ganttchart Skill to help me plan a website launch next month. Ask about anything missing and return a URL I can open in iGanttChart.

You do not need to paste the full instructions or URL each time. Keep describing and refining what you want through conversation. If your environment does not select the Skill automatically, name it explicitly.

## Generate a sample URL

From the repository root, with Python 3.10 or newer:

```bash
python3 ganttchart/scripts/create_url.py ganttchart/examples/sample.en.json --name "Website launch"
```

The tool runs offline using the Python standard library. Successful output is one URL. For your own content, follow the [data format](references/content-format.md); dates use seconds since 2001-01-01 UTC, and dependencies reference task IDs.

## Questions and limits

**Does the URL save a file?** No. It opens an unsaved, editable preview. Review and import it in the app to keep it. A newly generated URL does not update an existing link or saved file.

**Is Google Drive required?** No account or API is required to generate the URL. App-side saving is a separate action. This Skill does not share existing Google Drive files.

**Is the content private?** Anyone with the URL can recover its content. Compression is not encryption. Avoid including information you do not want to share. URLs over 8,000 characters are rejected; split a large plan if needed.

**What has been verified?** The English and Japanese samples pass offline URL round trips and the local Flutter receiving decoder. This does not verify the currently deployed UI, rendering, importing, or persistence. See [verification results](../apps.json).
