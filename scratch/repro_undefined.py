import requests

sid = "sess_repro_undefined_2"
# 1. Signup customer
res_signup = requests.post("http://127.0.0.1:5000/api/auth/customer/signup", json={
    "session_id": sid,
    "name": "anm",
    "mobile": "9876543210",
    "business_name": "kaushal tech",
    "password": "pass"
})
print("Signup response:", res_signup.json().get("status"))

# 2. Check workflow stage
res_wf = requests.get(f"http://127.0.0.1:5000/api/workflow/state/{sid}")
print("Workflow stage after signup:", res_wf.json().get("workflow", {}).get("stage"))

# 3. User message: "meri kapdo ki shop hai"
res1 = requests.post("http://127.0.0.1:5000/api/advisor/chat", json={
    "session_id": sid,
    "message": "meri kapdo ki shop hai",
    "language": "en"
})
print("Msg 1 reply:", res1.json().get("reply"))
print("Msg 1 QR:", res1.json().get("quick_replies"))

# 4. User message: "upi pe"
res2 = requests.post("http://127.0.0.1:5000/api/advisor/chat", json={
    "session_id": sid,
    "message": "upi pe",
    "language": "en"
})
print("Msg 2 reply:", res2.json().get("reply"))
print("Msg 2 QR:", res2.json().get("quick_replies"))

# 5. User message: "haan upi pd"
res3 = requests.post("http://127.0.0.1:5000/api/advisor/chat", json={
    "session_id": sid,
    "message": "haan upi pd",
    "language": "en"
})
data = res3.json()
print("Msg 3 reply:", data.get("reply"))
print("Msg 3 QR:", data.get("quick_replies"))
wf3 = data.get("workflow", {})
print("Msg 3 last message in wf:", wf3.get("messages", [])[-1])
