import os
import sys
import importlib.util

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PROTOTYPE_DIR = os.path.join(ROOT_DIR, "prototype")

if PROTOTYPE_DIR not in sys.path:
    sys.path.insert(0, PROTOTYPE_DIR)

os.chdir(PROTOTYPE_DIR)

spec = importlib.util.spec_from_file_location("prototype_app", os.path.join(PROTOTYPE_DIR, "app.py"))
prototype_app = importlib.util.module_from_spec(spec)
sys.modules["prototype_app"] = prototype_app
spec.loader.exec_module(prototype_app)

app = prototype_app.app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
