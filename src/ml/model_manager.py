"""
Small wrapper around joblib load/save so the rest of the codebase never
touches file paths directly, and so a future model-registry / versioning
scheme can be dropped in here without changing any calling code.
"""

import os
import shutil
import time
import joblib
from config import settings


def save_model_bundle(bundle: dict, path: str = settings.MODEL_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(bundle, path)


def load_model_bundle(path: str = settings.MODEL_PATH):
    return joblib.load(path)


def archive_current_model():
    """Copies the current model file to a timestamped backup before overwriting."""
    if not os.path.exists(settings.MODEL_PATH):
        return None
    stamp = time.strftime("%Y%m%d_%H%M%S")
    archive_path = settings.MODEL_PATH.replace(".pkl", f"_{stamp}.pkl")
    shutil.copy2(settings.MODEL_PATH, archive_path)
    return archive_path
