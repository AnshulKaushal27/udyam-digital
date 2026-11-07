"""Test SSE streaming endpoint for proactive salesperson and language synchronization."""
import sys
import json
import requests
import uuid

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_URL = "http://127.0.0.1:5000"

def test_stream_billing_flow():
    sid = f"stream_test_{uuid.uuid4().hex[:8]}"
    
    # Message 1
    resp1 = requests.post(f"{BASE_URL}/api/advisor/chat/stream", json={
        "session_id": sid,
        "messages": [{"role": "user", "content": "I need a digital billing system."}],
        "language": "en"
    }, stream=True)
    
    assert resp1.status_code == 200
    accum1 = ""
    meta1 = None
    for line in resp1.iter_lines():
        if not line: continue
        dec = line.decode("utf-8")
        if dec.startswith("data: "):
            chunk = json.loads(dec[6:])
            if chunk.get("type") == "chunk":
                accum1 += chunk.get("text", "")
            elif chunk.get("type") == "meta":
                meta1 = chunk.get("data")

    print(f"Stream 1 text: {accum1.strip()}")
    assert meta1 is not None
    assert meta1.get("discovery_status") == "in_progress"

    # Message 2
    resp2 = requests.post(f"{BASE_URL}/api/advisor/chat/stream", json={
        "session_id": sid,
        "messages": [
            {"role": "user", "content": "I need a digital billing system."},
            {"role": "assistant", "content": accum1},
            {"role": "user", "content": "Currently on paper."}
        ],
        "language": "en"
    }, stream=True)
    
    assert resp2.status_code == 200
    accum2 = ""
    meta2 = None
    for line in resp2.iter_lines():
        if not line: continue
        dec = line.decode("utf-8")
        if dec.startswith("data: "):
            chunk = json.loads(dec[6:])
            if chunk.get("type") == "chunk":
                accum2 += chunk.get("text", "")
            elif chunk.get("type") == "meta":
                meta2 = chunk.get("data")

    print(f"Stream 2 text: {accum2.strip()}")
    assert meta2 is not None

    # Message 3
    resp3 = requests.post(f"{BASE_URL}/api/advisor/chat/stream", json={
        "session_id": sid,
        "messages": [
            {"role": "user", "content": "I need a digital billing system."},
            {"role": "assistant", "content": accum1},
            {"role": "user", "content": "Currently on paper."},
            {"role": "assistant", "content": accum2},
            {"role": "user", "content": "Yes, I need proper GST invoicing."}
        ],
        "language": "en"
    }, stream=True)
    
    assert resp3.status_code == 200
    accum3 = ""
    meta3 = None
    for line in resp3.iter_lines():
        if not line: continue
        dec = line.decode("utf-8")
        if dec.startswith("data: "):
            chunk = json.loads(dec[6:])
            if chunk.get("type") == "chunk":
                accum3 += chunk.get("text", "")
            elif chunk.get("type") == "meta":
                meta3 = chunk.get("data")

    print(f"Stream 3 text: {accum3.strip()}")
    assert meta3 is not None

    # Message 4: Volume (300-400)
    resp4 = requests.post(f"{BASE_URL}/api/advisor/chat/stream", json={
        "session_id": sid,
        "messages": [
            {"role": "user", "content": "I need a digital billing system."},
            {"role": "assistant", "content": accum1},
            {"role": "user", "content": "Currently on paper."},
            {"role": "assistant", "content": accum2},
            {"role": "user", "content": "Yes, I need proper GST invoicing."},
            {"role": "assistant", "content": accum3},
            {"role": "user", "content": "300–400."}
        ],
        "language": "en"
    }, stream=True)
    
    assert resp4.status_code == 200
    accum4 = ""
    meta4 = None
    for line in resp4.iter_lines():
        if not line: continue
        dec = line.decode("utf-8")
        if dec.startswith("data: "):
            chunk = json.loads(dec[6:])
            if chunk.get("type") == "chunk":
                accum4 += chunk.get("text", "")
            elif chunk.get("type") == "meta":
                meta4 = chunk.get("data")

    print(f"Stream 4 text: {accum4.strip()}")
    assert meta4 is not None
    assert meta4.get("discovery_status") == "complete" or meta4.get("recommend_bundle") is not None
    assert meta4.get("recommend_bundle") in ["bundle_kirana", "bundle_clinic"]
    print("Stream test PASSED: Real-time streaming generates proactive billing recommendation!")

if __name__ == "__main__":
    test_stream_billing_flow()
