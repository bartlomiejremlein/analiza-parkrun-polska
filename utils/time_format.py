def string_to_seconds(value: str) -> int | None:
    """Converts string value of result, e.g. 1725,
    which corresponds to 17:25 (17 minutes and 25 seconds)
    to total number of seconds.
    """
    if value:
        if len(value) == 5:
            hours = int(value[0])
            minutes = int(value[1:3])
            seconds = int(value[-2:])
            return int(hours * 3600 + minutes * 60 + seconds)
        else:
            minutes = int(value[:2])
            seconds = int(value[-2:])
            return int(minutes * 60 + seconds)
    return None


def string_to_seconds_results(value: str | None) -> int | None:
    """Converts result time string to seconds, e.g. 20:00 to 1200 seconds"""
    if value:
        if len(value) > 5:
            hours = int(value[0])
            minutes = int(value[2:4])
            seconds = int(value[-2:])
            return int(hours * 3600 + minutes * 60 + seconds)
        else:
            minutes = int(value[:2])
            seconds = int(value[-2:])
            return int(minutes * 60 + seconds)
    return None


def format_result_mm_ss(value: str) -> str | None:
    """
    Converts result string e.g. 1725 to time 17:25 (17 minutes and 25 seconds).
    """
    if value:
        if len(value) == 5:
            hours = value[0]
            minutes = value[1:3]
            seconds = value[-2:]
            return f'{hours.rjust(2, "0")}:{minutes}:{seconds.rjust(2, "0")}'
        elif len(value) == 4:
            minutes = value[:2]
            seconds = value[-2:]
            return f'{minutes}:{seconds.rjust(2, "0")}'
    return None
