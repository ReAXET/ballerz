import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd
import numpy as np
import os
import requests
import json
import datetime
import time
import logging
from pathlib import Path





def read_mlb_data():
    """
    Read MLB data from parquet files
    """
    data_dir = Path(__file__).resolve().parent.parent.parent / 'data/mlb'
    data_files = [f for f in os.listdir(data_dir) if f.endswith('.parquet')]
    data = pd.DataFrame()
    for f in data_files:
        data = pd.concat([data, pd.read_parquet(data_dir / f)])
    return data