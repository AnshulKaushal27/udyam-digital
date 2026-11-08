import csv

catalogue_path = r"E:\Airtel\6ae1873397bc1_digital\YTL_TrackA_Udyam_Digital_Data\product_catalogue.csv"
with open(catalogue_path, "r", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        print(r['product_id'] + ": " + r['product_name'] + " | min: " + r['price_min_inr_per_month'] + " | max: " + r['price_max_inr_per_month'] + " | setup: " + r['one_time_setup_inr'] + " | contract: " + r['min_contract_months'] + " | req_one_of: " + r['requires_one_of'])
