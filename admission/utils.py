from datetime import date

def calculate_age(instance, date_of_birth) -> str:
    if date_of_birth:
        today = date.today()
        return today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    return 0