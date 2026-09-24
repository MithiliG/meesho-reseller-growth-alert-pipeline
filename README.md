# Meesho Reseller Growth Alert Pipeline

An end-to-end analytics and AI workflow for monitoring monthly reseller growth.

This project combines **SQL analytics, growth detection, data validation, AI-assisted narrative generation, and an agent workflow** to identify significant changes in monthly reseller category revenue.

---

## What This Project Does

* Generates a deterministic reseller dataset
* Analyzes revenue using SQL
* Calculates month-over-month (MoM) growth
* Detects significant revenue changes
* Validates incoming data feeds
* Detects corrupted data
* Generates stakeholder-friendly narratives
* Masks reseller names in narratives
* Uses an agent workflow with human approval
* Produces structured JSON output

---

## Tech Stack

* Python
* SQL / SQLite
* Pandas
* Pytest
* AI Prompt Engineering
* Agentic Workflow Design

---

## Project Structure

```text
meesho-reseller-growth-alert-pipeline/
│
├── data/
│   ├── generate_dataset.py
│   ├── orders.csv
│   ├── resellers.csv
│   └── meesho_reseller.db
│
├── part1_sql/
│   ├── queries.py
│   ├── queries.sql
│   └── output/
│
├── part2_engine/
│   ├── growth_engine.py
│   ├── fixtures/
│   └── test_growth_engine.py
│
├── part3_narrative/
│   ├── masking.py
│   ├── prompt_template.py
│   ├── prompt_pack.md
│   ├── narrative_report.md
│   └── test_masking.py
│
├── part4_agent/
│   ├── agent_spec.md
│   ├── mock_agent_runner.py
│   ├── fixtures/
│   └── test_mock_agent_runner.py
│
└── README.md
```

---

## How the Parts Connect

The project works as one connected pipeline:

```text
Dataset Generation
        ↓
Part 1 — SQL Analytics
        ↓
Monthly Category Revenue
        ↓
Part 2 — Growth Engine
        ↓
Verified Growth Results
        ├──────────────→ Part 3 — Narrative Generation
        │
        └──────────────→ Part 4 — Agent Runner
                                      ↓
                              Structured JSON
                                      ↓
                              Human Approval
```

### Part 1 → Part 2

Part 1 generates the monthly category revenue output:

```text
part1_sql/output/monthly_category_revenue(ques1).csv
```

This SQL output is used as the input feed for the Part 2 growth engine.

### Part 2 → Part 3

Part 2 calculates and verifies:

* Previous revenue
* Current revenue
* MoM growth percentage
* Flagged / not-flagged status

These verified results are used by Part 3's narrative templates to create stakeholder-friendly messages.

### Part 2 → Part 4

Part 4 uses the validated feed and Part 2 growth logic to:

* Validate the current-month data
* Calculate MoM growth
* Identify flagged categories
* Select the top 3 categories
* Suppress remaining flagged categories
* Escalate exact 8% boundary cases
* Generate drafts for human approval

---

# 1. Dataset Generation

The project uses a deterministic local dataset.

The dataset is generated using:

```text
data/generate_dataset.py
```

It creates:

```text
data/resellers.csv
data/orders.csv
data/meesho_reseller.db
```

### Regenerate the Dataset

Run from the project root:

```bash
python data/generate_dataset.py
```

The generated SQLite database is then used by Part 1.

---

# 2. Part 1 — SQL Analytics

Part 1 analyzes the SQLite database using SQL queries.

Main files:

```text
part1_sql/queries.py
part1_sql/queries.sql
```

The results are saved in:

```text
part1_sql/output/
```

### Run Part 1

```bash
python part1_sql/queries.py
```

The main outputs include:

```text
monthly_category_revenue(ques1).csv
region_revenue(ques2).csv
top_resellers(ques3).csv
zero_order_resellers(ques4.1).csv
zero_order_count_demo(ques4.2).csv
june_aov(ques5).csv
```

The monthly category revenue output is passed to Part 2.

---

# 3. Part 2 — Growth Engine

Part 2 performs:

* Month-over-month revenue calculation
* Threshold-based flagging
* Feed validation
* Corrupted-feed detection

Main file:

```text
part2_engine/growth_engine.py
```

Key functions:

```text
mom_growth(previous, current)
is_flagged(mom_pct, threshold=8.0)
validate_feed(csv_path)
```

### Run Part 2 Tests

```bash
python -m pytest part2_engine -v
```

Part 2 also contains a corrupted-feed fixture:

```text
part2_engine/fixtures/corrupted_feed.csv
```

This is used to test validation and error handling.

---

# 4. Part 3 — Narrative Generation

Part 3 converts verified analytics results into stakeholder-friendly narratives.

Main files:

```text
part3_narrative/
├── masking.py
├── prompt_template.py
├── prompt_pack.md
└── narrative_report.md
```

The narrative structure follows:

```text
Context → Insight → Implication
```

Part 3 also masks reseller names to prevent raw reseller names from appearing in stakeholder narratives.

### Run Part 3 Tests

```bash
python -m pytest part3_narrative -v
```

The tests verify reseller aliasing and raw-name leak protection.

---

# 5. Part 4 — Agent Workflow

Part 4 integrates the analytics, growth detection, and narrative workflow into a guarded mock monitoring agent.

Main files:

```text
part4_agent/agent_spec.md
part4_agent/mock_agent_runner.py
part4_agent/test_mock_agent_runner.py
```

The agent performs these steps:

1. Load the monthly revenue feed.
2. Validate the current-month feed.
3. Stop if validation fails.
4. Calculate MoM growth.
5. Identify flagged categories.
6. Sort flagged categories by absolute MoM percentage.
7. Draft messages for the top 3 flagged categories.
8. Suppress remaining flagged categories.
9. Escalate exact 8% boundary cases.
10. Return one structured JSON object.

The agent **does not send real messages**. Drafts are held for human approval.

### Run Part 4 Tests

```bash
python -m pytest part4_agent -v
```

---

# 6. Part 4 Scenarios

Part 4 includes fixtures for different monthly scenarios:

```text
part4_agent/fixtures/
├── april.csv
├── may.csv
├── june.csv
├── boundary_previous.csv
└── boundary_current.csv
```

These are used to test:

* April → May
* May → June
* Exact 8% boundary cases
* Corrupted-feed handling
* Top-3 drafting
* Suppression
* Escalation

---

# 7. Guardrails

The workflow includes several safeguards.

### Input Guardrail

The current-month feed must pass:

```text
validate_feed()
```

before growth calculations or message drafting begin.

If validation fails, the agent performs a **Hard Stop**.

### Action Guardrail

The agent never automatically sends messages.

It only creates drafts and holds them for human approval.

### Output Guardrail

Numbers in drafted messages must come from verified Part 1 or Part 2 values.

The agent must not invent additional metrics.

### Privacy Guardrail

Reseller names are masked before appearing in stakeholder narratives.

### Boundary Guardrail

An exact **8% MoM change** is handled separately as an escalation case rather than a normal flagged category.

---

# 8. Structured JSON Output

Every Part 4 run returns a structured JSON object containing:

```text
run_month
validation_status
validation_errors
flagged_categories
suppressed_categories
escalated_categories
action_taken
```

A drafted category contains:

```text
category
mom_pct
previous_revenue
current_revenue
drafted
message
```

---

# 9. Run the Complete Project

### Step 1 — Generate Dataset

```bash
python data/generate_dataset.py
```

### Step 2 — Run Part 1

```bash
python part1_sql/queries.py
```

### Step 3 — Run Part 2 Tests

```bash
python -m pytest part2_engine -v
```

### Step 4 — Run Part 3 Tests

```bash
python -m pytest part3_narrative -v
```

### Step 5 — Run Part 4 Tests

```bash
python -m pytest part4_agent -v
```

### Step 6 — Run All Tests

```bash
python -m pytest -v
```

---

# 10. Offline Execution

The project is designed to run locally and offline.

It does not require:

* External APIs
* API keys
* Gmail
* SMTP
* External databases
* Real message-sending services

Part 4 only creates message drafts and holds them for human approval.

---

## End-to-End Flow

```text
Dataset Generation
        ↓
SQLite Database
        ↓
Part 1 — SQL Analytics
        ↓
Monthly Category Revenue
        ↓
Part 2 — Growth Engine
        ↓
Verified MoM Results
        ├──────────────→ Part 3 — Narrative Templates
        │
        └──────────────→ Part 4 — Agent Runner
                                      ↓
                              Top 3 Drafts
                                      ↓
                              Structured JSON
                                      ↓
                              Human Approval
```

---

## Testing

Run the complete automated test suite:

```bash
python -m pytest -v
```

This covers:

* Part 2 — Growth Engine
* Part 3 — Narrative / Masking
* Part 4 — Agent Runner

Part 1 is executed separately with:

```bash
python part1_sql/queries.py
```

---

## Project Design Principles

* **Data validation before processing**
* **Verified numbers only**
* **Human approval before action**
* **Privacy-aware narrative generation**
* **Deterministic and reproducible dataset**
* **Automated testing**

---
