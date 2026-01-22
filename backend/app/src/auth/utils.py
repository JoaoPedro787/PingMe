from datetime import datetime, timedelta, timezone
from typing import Literal


def format_to_datetime(type: Literal["MINUTE", "DAY"], exp):
    exp_date = datetime.now(tz=timezone.utc)

    match type:
        case "MINUTE":
            exp_date += timedelta(minutes=exp)
        case "DAY":
            exp_date += timedelta(days=exp)

    return exp_date
