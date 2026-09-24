# Part 4 — Agent Specification

## Goal

Keep Meesho category managers informed of categories whose month-on-month revenue moves beyond the 8% threshold, while requiring human approval before any drafted message is considered sent.

## Tools

The monitoring agent uses the following functions:

- `validate_feed` from Part 2 to validate the monthly revenue feed.
- `mom_growth` from Part 2 to calculate month-on-month revenue growth.
- `is_flagged` from Part 2 to classify each MoM percentage.
- Part 3 prompt-pack template-fill logic to create stakeholder messages.

The Part 2 growth functions are imported and used without modification.

## Memory / State

The agent uses the previous month's revenue per category as state for the next month.

For every category, the previous month's revenue is compared with the current month's revenue to calculate MoM growth.

The agent does not invent historical values. The previous-month and current-month CSV feeds provide the values used in each run.

## Planner

The agent executes the following ordered subtasks:

1. Load the monthly revenue feed and run `validate_feed`.
2. If validation fails, Hard Stop and report the validation errors.
3. If validation succeeds, compute `mom_growth` for every category against the previous month.
4. Run `is_flagged` on every category.
5. Sort flagged categories by absolute MoM percentage in descending order.
6. Draft messages for at most the top 3 flagged categories using the Part 3 template.
7. Log remaining flagged categories as `suppressed, review manually` without drafting messages.
7b. Separately log categories whose result is `escalate_exact_boundary` into `escalated_categories`, without drafting a message.
8. Emit one structured JSON object for the run.

## Feedback Loop

Drafted messages are never automatically sent.

Every drafted message is held for human approval.

The runner represents this state with:

`action_taken = "drafted_and_held_for_approval"`

There is no email, Gmail, SMTP, or external messaging integration.

## Guardrails

### Input Guardrail

`validate_feed` must pass before any MoM calculation or message drafting occurs.

If validation fails, the run immediately becomes a Hard Stop.

### Action Guardrail

The agent never automatically sends a message.

It only drafts messages and holds them for human approval.

### Output Guardrail

Every number in a drafted message must trace back to a Part 1 or Part 2 value.

The agent must not invent additional metrics or figures.

## Success Condition

A run is successful when:

- The input feed is valid.
- MoM calculations are completed.
- Flagged categories are correctly identified.
- At most the top 3 flagged categories are drafted.
- Remaining flagged categories are suppressed for manual review.
- Exact-boundary categories are recorded separately.
- Every drafted message contains traceable values.
- Drafts are held for human approval.

A valid run may also correctly produce zero drafted messages when no category crosses the threshold.

## Error Stopping Condition

If `validate_feed` returns `False`, the agent performs a Hard Stop.

The validation errors are surfaced in `validation_errors`.

No MoM computation is attempted.

No category is drafted.

No category is suppressed.

## Given-When-Then Specifications

### Scenario 1 — May Ethnic Wear

Given April Ethnic Wear revenue is 104520.77 and May Ethnic Wear revenue is 185107.61,

When the monitoring agent calculates MoM growth,

Then the result is 77.1% and the category is flagged.

### Scenario 2 — June Beauty & Personal Care

Given May Beauty & Personal Care revenue is 35542.11 and June Beauty & Personal Care revenue is 37559.07,

When the monitoring agent calculates MoM growth,

Then the result is 5.67% and the category is not flagged.

### Scenario 3 — Exact 8% Boundary

Given previous revenue is 100000 and current revenue is 108000,

When the monitoring agent calculates MoM growth and applies the threshold,

Then the result is 8.0% and the category is classified as `escalate_exact_boundary`.

### Scenario 4 — Corrupted Feed

Given the current-month feed contains the corrupted fixture,

When the monitoring agent validates the feed,

Then validation fails with exactly the three expected validation errors and the run Hard Stops.