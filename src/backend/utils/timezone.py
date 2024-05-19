import zoneinfo as tz
from datetime import datetime, timedelta
from backend.core.config import settings



class Timezone:
    def __init__(self, timezone: str = settings.TIMEZONE):
        self.tz_info = tz.ZoneInfo(timezone)

    def now(self) -> datetime:
        """
        Get the current time in the specified timezone.

        :return: The current time in the specified timezone.
        """

        return datetime.now(self.tz)
    

    def f_datetime(self, dt: datetime) -> datetime:
        """
        Format the given datetime in the specified timezone.

        :param dt: The datetime to format.
        :return: The formatted datetime.
        """

        return dt.astimezone(self.tz_info)
    

    def f_strftime(self, date_string: str, format_str: str) -> str:
        """
        Format the given datetime in the specified timezone using the given format.

        :param dt: The datetime to format.
        :param fmt: The format to use.
        :return: The formatted datetime string.
        """

        return self.f_datetime(datetime.strptime(date_string, format_str)).strftime(format_str)
    


timezone = Timezone()