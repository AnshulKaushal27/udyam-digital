import csv

with open('e:/Airtel/6ae1873397bc1_digital/YTL_TrackA_Udyam_Digital_Data/product_catalogue.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"{row['product_id']}: {row['product_name']} | {row['category']} | INR {row['price_min_inr_per_month']}-{row['price_max_inr_per_month']}/mo | setup: INR {row['one_time_setup_inr']} | req: {row['requires_one_of']}")
