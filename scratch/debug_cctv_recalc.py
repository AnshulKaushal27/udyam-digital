import sys
sys.path.append('e:/Airtel/prototype')
from customer_workflow_engine import get_or_create_workflow, transition_workflow

sid = "sess_debug_cctv_recalc"
transition_workflow(sid, "SELECT_USER_TYPE", {"user_type": "customer"})
transition_workflow(sid, "SELECT_CATEGORY", {"category": "kirana"})
wf = transition_workflow(sid, "TOGGLE_REQUIREMENT", {"requirement": "cctv_security"})

print("Discovery requirements:", wf["discovery"]["requirements"])
print("Active addons:", wf["recommendation"]["active_addons"])
print("Monthly base:", wf["recommendation"]["monthly_base"])
print("Monthly subtotal:", wf["recommendation"]["monthly_subtotal"])
print("Total monthly:", wf["recommendation"]["total_monthly"])
