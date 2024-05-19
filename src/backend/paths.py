"""UNIX paths for the backend. This will help with the file paths for the project."""
import os


ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

PROJECT_MLB_DATA_DIR = '/home/jbox/Desktop/mlb' # Is a gigabyte of data in parquet files

# Path to the data directory
DATA_DIR = os.path.join(ROOT_DIR, 'data')

# Path to the MLB data directory
MLB_DATA_DIR = os.path.join(DATA_DIR, 'mlb')

# Path to the NBA data directory
NBA_DATA_DIR = os.path.join(DATA_DIR, 'nba')

# Path to the NFL data directory
NFL_DATA_DIR = os.path.join(DATA_DIR, 'nfl')

# Path to the NHL data directory
NHL_DATA_DIR = os.path.join(DATA_DIR, 'nhl')

# Path to the NCAA Football data directory
NCAA_FOOTBALL_DATA_DIR = os.path.join(DATA_DIR, 'ncaa_football')