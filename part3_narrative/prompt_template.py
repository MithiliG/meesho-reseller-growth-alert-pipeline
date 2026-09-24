def fill_prompt_template(
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