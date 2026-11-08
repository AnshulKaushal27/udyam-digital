import sys

def main():
    path = "prototype/app.py"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    target = "    # 6. Handle Quote Confirmation & Progression"
    addition = """    # 5B. Handle Quote Review via Natural Language
    is_direct_quote_query = (
        any(k in text_low for k in [
            "show me the quote", "show quote", "view quote", "monthly bill", "quote and monthly bill", "show me the bill", "what is the bill", "check quote", "see quote"
        ])
        or (text_low in ["quote", "bill", "view bill", "pricing"])
    ) and not any(w in text_low for w in ["how much is", "cctv", "camera", "cameras", "static ip", "whatsapp", "pos", "failover", "soundbox", "router", "billing software", "billing machine", "billing system"])

    if is_direct_quote_query:
        transition_workflow(sid, "GO_TO_STAGE", {"stage": "QUOTE_REVIEW"})
        sync_workflow_to_session(sid)
        reply = f"Here is your single transparent bill: \u20b9{wf['recommendation']['total_monthly']}/month (inclusive of 18% GST). Zero hidden fees."
        quick = ["Confirm Quote & Start Smart KYC", "Add Cloud CCTV (+₹800)", "Add Static IP (+₹300)"]
        wf["messages"].append({
            "sender": "bot",
            "text": reply,
            "quick_replies": quick
        })
        existing_qid = next((qid for qid, q in SHARED_QUOTES.items() if q.get("session_id") == sid), None)
        active_quote = SHARED_QUOTES.get(existing_qid) if existing_qid else None
        return jsonify({
            "status": "success",
            "session_id": sid,
            "quote_id": existing_qid,
            "reply": reply,
            "workflow": wf,
            "quote": active_quote,
            "quick_replies": quick,
            "profile": session["profile"],
            "identified_needs": session["identified_needs"],
            "discovery_status": "complete"
        })

    # 6. Handle Quote Confirmation & Progression"""

    if target not in content:
        print("Target not found in app.py")
        sys.exit(1)

    new_content = content.replace(target, addition, 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Successfully updated app.py with quote view intent")

if __name__ == "__main__":
    main()
