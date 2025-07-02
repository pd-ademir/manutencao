def format_km(value):
    if value is None:
        return "-"
    try:
        return f"{int(value):,}".replace(",", ".") + " km"
    except (ValueError, TypeError):
        return str(value)
    

