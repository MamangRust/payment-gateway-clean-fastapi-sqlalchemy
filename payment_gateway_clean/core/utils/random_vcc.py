import random

def random_vcc() -> str:
    """
    Generate a random 16-digit Visa-like credit card number with a valid Luhn check digit.
    Returns:
        str: A Visa-like credit card number as a string.
    """
    # Generate a random 15-digit number
    random_number = ''.join(str(random.randint(0, 9)) for _ in range(15))

    # Prepend "4" to signify a Visa-like card
    partial_card_number = f"4{random_number}"

    # Calculate the Luhn check digit
    check_digit = calculate_check_digit(partial_card_number)

    # Final credit card number with the check digit
    credit_card_number = f"{partial_card_number}{check_digit}"
    return credit_card_number


def calculate_check_digit(number: str) -> int:
    """
    Calculate the Luhn check digit for a given number.
    Args:
        number (str): The partial card number (excluding the check digit).
    Returns:
        int: The Luhn check digit.
    """
    sum_ = 0
    alternate = False

    # Process digits from right to left
    for digit_char in reversed(number):
        digit = int(digit_char)

        if alternate:
            digit *= 2
            if digit > 9:
                digit -= 9

        sum_ += digit
        alternate = not alternate

    # Calculate the check digit
    return (10 - (sum_ % 10)) % 10


