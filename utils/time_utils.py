from datetime import datetime

try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo  # Windows fix

def convert_to_timezone(dt_str, to_tz="Asia/Kolkata"):
    dt = datetime.fromisoformat(dt_str)
    ist = dt.replace(tzinfo=ZoneInfo("Asia/Kolkata"))
    return ist.astimezone(ZoneInfo(to_tz)).isoformat()
