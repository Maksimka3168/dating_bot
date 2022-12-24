def check_name(name: str) -> bool:
    # выражение
    if len(name) >= 20:
        return False
    else:
        try:
            int(name)
            return True
        except:
            return False
