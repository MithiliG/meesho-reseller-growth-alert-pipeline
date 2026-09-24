import csv


def mom_growth(previous: float, current: float) -> float:
    if previous == 0:
        return 0.0

    return round(((current - previous) / previous) * 100, 2)


def is_flagged(mom_pct: float, threshold: float = 8.0) -> str:
    if abs(mom_pct) == threshold:
        return "escalate_exact_boundary"

    if abs(mom_pct) >= threshold:
        return "flagged"

    return "not_flagged"


def validate_feed(csv_path: str) -> tuple[bool, list[str]]:
    errors = []

    with open(csv_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for line_number, row in enumerate(reader, start=2):

            category = row.get("category", "")
            revenue = row.get("revenue", "")

            if revenue != "":
                revenue_value = float(revenue)

                if revenue_value < 0:
                    errors.append(
                        f"line {line_number}: negative revenue "
                        f"({revenue_value}) for category={category}"
                    )

            if category == "":
                errors.append(
                    f"line {line_number}: missing category "
                    f"(month={row.get('month')})"
                )

            if revenue == "":
                errors.append(
                    f"line {line_number}: missing revenue "
                    f"(category={category})"
                )

    return len(errors) == 0, errors