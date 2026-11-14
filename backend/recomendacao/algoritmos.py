from pathlib import Path
import pandas as pd
from pandas.core.frame import DataFrame
import ast
from decimal import Decimal
import sqlite3
import time
import random
import os
import sys
from pathlib import Path
import numpy as np

BASE_DIR_DJANGO = Path(__file__).resolve().parents[1]
DJANGO_DIR = BASE_DIR_DJANGO / "PratoMatch"

sys.path.insert(0, str(DJANGO_DIR))

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "configs.settings"
)