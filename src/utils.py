import numpy as np


def generate_random_nums(low: int = 2, high: int = 10, num_factors: int = 2):
    """
    Generate an array of random integers and their product.

    Args:
        low (int): Minimum value (inclusive).
        high (int): Maximum value (exclusive).
        num_factors (int): Number of random integers to generate.

    Returns:
        tuple: A tuple containing the random integers and their product.
    """
    random_nums = np.random.randint(low=low, high=high, size=(num_factors))
    return random_nums, np.prod(random_nums)


def format_equation(random_nums: np.array) -> str:
    """
    Format the random numbers into a multiplication equation string.

    Args:
        random_nums (np.array): Array of random integers.

    Returns:
        str: A string representing the multiplication equation.
    """
    return " x ".join(map(str, random_nums)) + " = "


def reset_label(label, equation):
    """Reset the label text after an incorrect attempt"""
    label.config(text=equation)
