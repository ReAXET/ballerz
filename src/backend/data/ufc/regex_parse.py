"""Part of the Sherdog data scraper for the UFC dataset."""
import re
from typing import List, Tuple
import csv


def parse_fighter_name(fighter_name: str) -> Tuple[str, str]:
    """Parse the fighter name into first and last name."""
    # Split the name into first and last name
    name_parts = fighter_name.split()
    first_name = name_parts[0]
    last_name = " ".join(name_parts[1:])
    return first_name, last_name


def parse_fighter_record(record: str) -> Tuple[int, int, int]:
    """Parse the fighter record into wins, losses, and draws."""
    # Use regex to extract the wins, losses, and draws
    record_pattern = re.compile(r"(\d+)-(\d+)-(\d+)")
    record_match = record_pattern.match(record)
    wins = int(record_match.group(1))
    losses = int(record_match.group(2))
    draws = int(record_match.group(3))
    return wins, losses, draws


def parse_fighter_height(height: str) -> int:
    """Parse the fighter height into inches."""
    # Use regex to extract the height in inches
    height_pattern = re.compile(r"(\d+)'(\d+)")
    height_match = height_pattern.match(height)
    feet = int(height_match.group(1))
    inches = int(height_match.group(2))
    return feet * 12 + inches


def parse_fighter_weight(weight: str) -> int:
    """Parse the fighter weight into pounds."""
    # Use regex to extract the weight in pounds
    weight_pattern = re.compile(r"(\d+)")
    weight_match = weight_pattern.match(weight)
    return int(weight_match.group(1))


def parse_fighter_reach(reach: str) -> int:
    """Parse the fighter reach into inches."""
    # Use regex to extract the reach in inches
    reach_pattern = re.compile(r"(\d+)")
    reach_match = reach_pattern.match(reach)
    return int(reach_match.group(1))


def parse_fighter_stance(stance: str) -> str:
    """Parse the fighter stance into orthodox or southpaw."""
    # Use regex to extract the stance
    stance_pattern = re.compile(r"(Orthodox|Southpaw)")
    stance_match = stance_pattern.match(stance)
    return stance_match.group(1)


def parse_fighter_dob(dob: str) -> str:
    """Parse the fighter date of birth."""
    return dob


# Cleaning of scraped data for the UFC dataset
def clean_ufc_data(filename: str) -> None:
    """Clean the scraped UFC data and save it to a new file."""
    with open(filename, "r") as file:
        reader = csv.reader(file)
        header = next(reader)
        data = list(reader)


    # use regex to parse the data and remove any unwanted characters ", and '" from the data
    