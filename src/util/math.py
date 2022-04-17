"""
math helpers
"""

import numpy as np


def round_up_to_odd(number: float) -> int:
    """Round up to an odd number."""
    return int(np.ceil(number) // 2 * 2 + 1)
