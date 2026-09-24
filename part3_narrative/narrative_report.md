# Part 3 — Narrative Report

## 3.2 Worked Narrative Report

### May — Ethnic Wear

#### Context

This measures the month-over-month revenue change for the Ethnic Wear category from April to May.

#### Insight

**Fact:** Ethnic Wear revenue increased from INR 104520.77 in April to INR 185107.61 in May, representing **77.1% MoM growth**. The Part 2 rule therefore classified the result as `"flagged"`.

#### Implication

**Hypothesis:** The increase may reflect stronger demand or a change in reseller activity, but the supplied revenue data does not establish the cause.

**Action:** The regional manager should compare May Ethnic Wear reseller-level orders and campaign activity with April before deciding whether the increase should be sustained or investigated further.

---

### June — Ethnic Wear

#### Context

This measures the month-over-month revenue change for the Ethnic Wear category from May to June.

#### Insight

**Fact:** Ethnic Wear revenue decreased from INR 185107.61 in May to INR 76371.53 in June, representing **-58.74% MoM growth**. The Part 2 rule therefore classified the result as `"flagged"`.

#### Implication

**Hypothesis:** The decrease may be associated with weaker demand or reduced reseller activity, but the supplied revenue data does not establish the cause.

**Action:** The regional manager should compare June Ethnic Wear reseller-level orders with May and check campaign or stock activity to identify what changed before taking corrective action.

---

## Self-Score Against the Four Refinement Criteria

### Specificity

Pass — The narratives use the exact category name, months, revenue values, and MoM percentages supplied by Parts 1 and 2.

### Audience Fit

Pass — The narratives are written as short business updates for a regional manager and avoid unnecessary technical implementation details.

### Completeness

Pass — Both narratives contain Context, Insight, and Implication sections.

### Actionability

Pass — Each implication gives a concrete next step: compare reseller-level orders and check campaign or stock activity for the affected period.

---

# 3.3 Chart-Choice Justification

## Question 1 — Which month had the highest total revenue?

Use a **bar chart** because this is a univariate comparison of total revenue across three discrete months. April, May, and June are independent categories for this comparison, so bars make the relative revenue levels easy to compare within 10 seconds. The y-axis should start at zero, and no 3D effects are needed. A legend is unnecessary because there is only one revenue series.

The values are April = INR 419417.43, May = INR 444594.25, and June = INR 398055.24.

## Question 2 — What percentage share does Ethnic Wear represent of April's total revenue?

Use a **pie chart** because this is a part-to-whole question involving Ethnic Wear's share of April's total revenue. Ethnic Wear contributes INR 104520.77 out of April's INR 419417.43, which is **24.92%**. A pie chart directly communicates the share of one component within the total. The chart should remain simple, avoid 3D effects, and does not require a legend if the slice is directly labeled.

## Question 3 — How do the four regions compare on total revenue?

Use a **bar chart** because this is a univariate comparison of revenue across four discrete regions. A bar chart makes the differences between North, West, South, and East easy to compare within 10 seconds. The y-axis should start at zero, 3D should be avoided, and a legend is unnecessary because there is only one revenue series.

# Top Reseller Narrative — Masked

The top-reseller result identifies five resellers whose total spend exceeded the Part 1 threshold.

For external-facing reporting, the resellers are referenced only by region and approved alias:

- West — ALIAS-19
- West — ALIAS-22
- South — ALIAS-12
- North — ALIAS-06
- North — ALIAS-05

**Fact:** These aliases correspond to the five resellers returned by the Part 1 top-reseller query.

Raw reseller names are intentionally excluded from this external-facing narrative.