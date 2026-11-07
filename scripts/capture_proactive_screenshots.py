"""Capture high-resolution screenshots with headless Chrome."""
import subprocess
import os

chrome_bin = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
out_dir = r"E:\Airtel\qa_screenshots"

viewports = [
    ("consumer_desktop_proactive.png", 1440, 900),
    ("consumer_tablet_proactive.png", 768, 1024),
    ("consumer_mobile_proactive.png", 375, 812),
]

for fname, w, h in viewports:
    target_path = os.path.join(out_dir, fname)
    cmd = [
        chrome_bin,
        "--headless=new",
        f"--screenshot={target_path}",
        f"--window-size={w},{h}",
        "--hide-scrollbars",
        "http://127.0.0.1:5000/"
    ]
    subprocess.run(cmd, check=True)
    size = os.path.getsize(target_path)
    print(f"Captured {fname} ({size} bytes)")

print("All screenshots captured successfully!")
