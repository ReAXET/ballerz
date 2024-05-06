import os
from time import sleep
from urllib.error import
import pandas as pd
from tqdm import tqdm





# Create @retry decorator
def retry(ExceptionToCheck, tries=4, delay=3, backoff=2):
    """
    Decorator to retry a function multiple times if it fails.

    Parameters:
    -----------

        ExceptionToCheck: Exception
            The exception to check for.
        tries: int
            The number of times to try the function.
        delay: int
            The delay between each try.
        backoff: int
            The backoff factor for the delay.

    Returns:
    --------

        function
            The function to be retried.

    Example:
    --------

            @retry(Exception, tries=4, delay=3, backoff=2)
            def get_data():
                pass
    """

    def deco_retry(f):
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck:
                    sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry

    return deco_retry










def savant_data(season, team, home_away, csv=False, sep=';'):
    """
    Return detailed Baseball Savant data.

    Breaks down the data into the following categories:
    - pitch_type
    - pitch_velocity
    - launch_speed
    - launch_angle
    - exit_velocity
    - distance
    - hit_distance_sc
    - launch_speed_angle
    - effective_speed
    - release_spin_rate
    - release_extension
    - release_pos_x
    - release_pos_z
    - release_pos_y
    - release_speed
    - release_spin_dir
    - pitch_type
    - zone
    - hit_location
    - balls
    - strikes
    - game_date
    - player_name
    - batter
    - pitcher
    - events
    - description
    - spin_dir
    - spin_rate_deprecated
    - break_angle_deprecated
    - break_length_deprecated
    - zone_deprecated
    - des
    - pitch_name
    - pitch_type
    - type
    - id

    Team, year, and home/away status are broken down as well.

    Parameters:
    ------------

        season: int 
            The year of the season you want to scrape data from.
        team: str
            The team you want to scrape data from in 3-letter abbreviation.
        home_away: str
            The home/away status of the team. Away status can also be listed as 'away' or 'road'.
        csv: bool
            If True, the data will be saved as a CSV file in the current directory.
        sep: str
            The separator for the CSV file. Default is a semicolon.


    Returns:
    --------

        DataFrame
            A DataFrame containing the data from Baseball Savant and optional CSV file.

    
    Example:
    --------
    
            savant_data(2021, 'LAD', 'home', csv=True)


    Raises:
    -------

        HTTPError
            If the URL request fails multiple times.
    """

    # Retry decorator
    @retry
    def 