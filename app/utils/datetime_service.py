from datetime import datetime, timezone, timedelta
import traceback


def parse_from_date(date_str: str, format_pattern: str = "%Y-%m-%d") -> datetime:
    if not date_str:
        return None
    
    try:
        return datetime.strptime(date_str,format_pattern).replace(tzinfo=timezone.utc)
    except ValueError as err:
        traceback.print_exc()
        return None
    