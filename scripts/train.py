"""Convenience entry point: python scripts/train.py"""

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ml.train_model import train

if __name__ == "__main__":
    train()
