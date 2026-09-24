# Part 3 — Reusable Prompt Pack

## Trigger

This prompt is triggered when a category's `is_flagged` result is `"flagged"`.

The purpose is to convert verified Part 1 and Part 2 numbers into a short stakeholder update for a regional manager.

## Input list

The prompt requires these verified input variables:

- `{category}` — category name
- `{previous_revenue}` — revenue in the previous month
- `{current_revenue}` — revenue in the current month
- `{mom_pct}` — month-over-month percentage change
- `{month}` — current month
- `{prev_month}` — previous month

Only supplied and verified values may be used in the narrative.

## Prompt

Write a concise stakeholder update for a regional manager using the following verified inputs:

- Category: [{category}]
- Previous month: [{prev_month}]
- Current month: [{month}]
- Previous revenue: [{previous_revenue}]
- Current revenue: [{current_revenue}]
- MoM percentage: [{mom_pct}]

Use exactly this structure:

### Context
Explain what category is being measured and compare [{month}] with [{prev_month}].

### Insight
State the verified MoM result as a fact. Use [{mom_pct}] exactly as supplied.

### Implication
Give one specific and actionable next step for the regional manager.

Rules:

1. Use only the numbers supplied in the input list.
2. Never invent revenue, order counts, causes, percentages, or other metrics.
3. Every numerical statement must match one of the supplied placeholder values.
4. Clearly distinguish verified facts from hypotheses.
5. If proposing a possible cause that is not proven by the supplied data, label it as a hypothesis.
6. Do not expose raw reseller names. Use only approved aliases when a reseller must be referenced.
7. Keep the language suitable for a regional manager rather than a technical/data-engineering audience.

## Checklist

Before using the generated narrative, verify:

- [ ] Every number in the draft matches a supplied placeholder value exactly.
- [ ] The category and month names match the supplied inputs.
- [ ] Verified observations are explicitly labeled as facts.
- [ ] Any unproven cause is explicitly labeled as a hypothesis.
- [ ] The implication contains a specific and actionable next step.
- [ ] No raw reseller name appears in the narrative.
- [ ] Any reseller reference uses the approved alias format.
- [ ] The narrative follows the Context → Insight → Implication structure.