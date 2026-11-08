import sys

def main():
    path = "prototype/conversational_ai.py"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    target = "    # 2. Check for Ordinal Reference"
    addition = """    # 1B. Check for Quote / Bill / Pricing request
    is_quote_query = (
        any(k in text_low for k in ["quote", "bill", "monthly bill", "pricing", "charges"])
        and not any(k in text_low for k in ["how much is", "cctv", "camera", "static ip", "whatsapp", "soundbox", "pos", "billing machine", "billing software", "billing system"])
    )
    if is_quote_query:
        total_m = workflow.get("recommendation", {}).get("total_monthly", 1999)
        return {
            "intent": "view_quote",
            "interpreted_need": "Review quotation and transparent monthly bill",
            "target_product_ids": [],
            "target_addon_ids": [],
            "state_changes": {"stage": "QUOTE_REVIEW"},
            "needs_clarification": False,
            "clarification_question": None,
            "reply": f"Here is your transparent itemized quotation: \u20b9{total_m}/month (inclusive of 18% GST). Zero hidden fees.",
            "quick_replies": ["Confirm Quote & Start Smart KYC", "Add Cloud CCTV (+₹800)", "Add Static IP (+₹300)"]
        }

    # 2. Check for Ordinal Reference"""

    if target not in content:
        print("Target not found in conversational_ai.py")
        sys.exit(1)

    new_content = content.replace(target, addition, 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Successfully updated conversational_ai.py")

if __name__ == "__main__":
    main()
