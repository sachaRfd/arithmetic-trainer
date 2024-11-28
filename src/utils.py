import numpy as np
import time


def generate_random_nums(
    low: int = 2, high: int = 10, num_factors: int = 2, use_division: bool = False
):
    """
    Generate an array of random integers and their product.

    Args:
        low (int): Minimum value (inclusive).
        high (int): Maximum value (exclusive).
        num_factors (int): Number of random integers to generate.
        use_division (bool): Whether or not divisions should be used.

    Returns:
        tuple: A tuple containing the random integers and their product.
    """
    np.random.seed(int(time.time() * 1000) % (2**32))

    random_nums = np.random.randint(low=low, high=high, size=(num_factors))
    product = np.prod(random_nums)

    if use_division:
        return [product, random_nums[1]], random_nums[0]

    return random_nums, product


def format_equation(random_nums: np.array, use_division: bool) -> str:
    """
    Format the random numbers into a multiplication/division equation string.

    Args:
        random_nums (np.array): Array of random integers.
        use_division (bool): whether or not we use divisions.

    Returns:
        str: A string representing the multiplication equation.
    """
    if use_division:
        return " / ".join(map(str, random_nums)) + " = "
    return " x ".join(map(str, random_nums)) + " = "


def generate_sample(low, high, num_factors, use_division):
    """
    Generate a sample math problem.

    Args:
        low (int): Minimum value (inclusive).
        high (int): Maximum value (exclusive).
        num_factors (int): Number of factors to include in the problem.
        use_division (bool): Whether to include division problems. If None, randomly decide.

    Returns:
        tuple: The correct answer and the equation as a string.
    """
    if use_division:
        # randomly generate multiplications or divisions
        if np.random.randint(0, 2):
            use_division = True
        else:
            use_division = False

    random_nums, answer = generate_random_nums(low, high, num_factors, use_division)
    equation = format_equation(random_nums, use_division)

    return answer, equation


def reset_label(label, equation):
    """Reset the label text after an incorrect attempt"""
    label.config(text=equation)
