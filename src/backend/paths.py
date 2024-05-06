"""UNIX paths for the backend. This will help with the file paths for the project."""
import os


ROOT_DIR = os.path.dirname(os.path.realpath(__file__))


# Path to the data directory
DATA_DIR = os.path.join(ROOT_DIR, 'data')

# Path to the raw data directory
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')

# Path to the processed data directory
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')

# Path to the MLB data directory
MLB_DATA_DIR = os.path.join(DATA_DIR, 'mlb')

# Path to the raw MLB data directory
RAW_MLB_DATA_DIR = os.path.join(MLB_DATA_DIR, 'raw')

# Path to the NBA data directory
NBA_DATA_DIR = os.path.join(DATA_DIR, 'nba')

# Path to the NFL data directory
NFL_DATA_DIR = os.path.join(DATA_DIR, 'nfl')

# Path to the NHL data directory
NHL_DATA_DIR = os.path.join(DATA_DIR, 'nhl')

# Path to the raw NBA data directory
RAW_NBA_DATA_DIR = os.path.join(NBA_DATA_DIR, 'raw')

# Path to the NCAA Football data directory
NCAA_FOOTBALL_DATA_DIR = os.path.join(DATA_DIR, 'ncaa_football')