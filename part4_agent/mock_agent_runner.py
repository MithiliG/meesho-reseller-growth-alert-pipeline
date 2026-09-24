import csv
import json
import os
import sys
from part3_narrative.prompt_template import fill_prompt_template

# Allow Part 4 to import Part 2 and Part 3 modules.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PART2_DIR = os.path.join(PROJECT_ROOT, "part2_engine")
PART3_DIR = os.path.join(PROJECT_ROOT, "part3_narrative")

if PART2_DIR not in sys.path:
    sys.path.insert(0, PART2_DIR)

if PART3_DIR not in sys.path:
    sys.path.insert(0, PART3_DIR)


from part2_engine.growth_engine import validate_feed, mom_growth, is_flagged


def load_feed(csv_path):
    with open(csv_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        rows = []

        for row in reader:
            rows.append({
                "month": row["month"],
                "category": row["category"],
                "revenue": float(row["revenue"]),
                "n_orders": int(row["n_orders"]),
            })

        return rows


def build_lookup(rows):
    return {
        row["category"]: row["revenue"]
        for row in rows
    }


def draft_message(
    category,
    previous_revenue,
    current_revenue,
    mom_pct,
    month,
    prev_month,
):
    return (
        f"Context: {category} revenue changed from "
        f"{previous_revenue} in {prev_month} to "
        f"{current_revenue} in {month}.\n"
        f"Insight: MoM revenue growth is {mom_pct}% and the category is flagged.\n"
        f"Implication: Review category performance and investigate the drivers "
        f"of this movement before taking further action."
    )


def run(month: str, previous_month_csv: str, current_month_csv: str) -> dict:

    # 1. Validate current feed

    valid, validation_errors = validate_feed(current_month_csv)

    if not valid:
        result = {
            "run_month": month,
            "validation_status": "invalid",
            "validation_errors": validation_errors,
            "flagged_categories": [],
            "suppressed_categories": [],
            "escalated_categories": [],
            "action_taken": "hard_stop",
        }

        return result

    # 2. Load valid feeds
    
    previous_rows = load_feed(previous_month_csv)
    current_rows = load_feed(current_month_csv)

    previous_lookup = build_lookup(previous_rows)
    current_lookup = build_lookup(current_rows)

    # 3 + 4. Calculate MoM and classify
    
    flagged = []
    escalated = []

    for category, current_revenue in current_lookup.items():

        if category not in previous_lookup:
            continue

        previous_revenue = previous_lookup[category]

        mom_pct = mom_growth(
            previous_revenue,
            current_revenue
        )

        status = is_flagged(mom_pct)

        item = {
            "category": category,
            "mom_pct": mom_pct,
            "previous_revenue": previous_revenue,
            "current_revenue": current_revenue,
        }

        if status == "flagged":
            flagged.append(item)

        elif status == "escalate_exact_boundary":
            escalated.append(category)

    # 5. Sort flagged categories by absolute MoM descending
    
    flagged.sort(
        key=lambda item: abs(item["mom_pct"]),
        reverse=True
    )

    # 6. Draft at most top 3
    
    top_three = flagged[:3]
    remaining = flagged[3:]

    flagged_output = []

    for item in top_three:
        message = fill_prompt_template(
            category=item["category"],
            previous_revenue=item["previous_revenue"],
            current_revenue=item["current_revenue"],
            mom_pct=item["mom_pct"],
            month=month,
            prev_month=previous_rows[0]["month"],
        )

        flagged_output.append({
            "category": item["category"],
            "mom_pct": item["mom_pct"],
            "previous_revenue": item["previous_revenue"],
            "current_revenue": item["current_revenue"],
            "drafted": True,
            "message": message,
        })

    # 7. Suppress remaining flagged categories

    suppressed_categories = [
        item["category"]
        for item in remaining
    ]
    
    # 8. Structured JSON result
    
    result = {
        "run_month": month,
        "validation_status": "valid",
        "validation_errors": [],
        "flagged_categories": flagged_output,
        "suppressed_categories": suppressed_categories,
        "escalated_categories": escalated,
        "action_taken": "drafted_and_held_for_approval",
    }

    return result


if __name__ == "__main__":

    project_root = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    april_may_previous = os.path.join(
        project_root,
        "part2_engine",
        "fixtures",
        "monthly_category_revenue.csv"
    )
