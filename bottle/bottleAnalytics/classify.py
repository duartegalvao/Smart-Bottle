import numpy as np


def classify(data):
    """Get raw data and return the final score."""
    w_stable = find_stable_points(data)
    consumption = get_consumption(w_stable)
    score = calculate_score(consumption, data)

    return score


# Auxiliary functions

def find_stable_points(w_raw, var_threshold=0.1, min_stable_samples=3):
    """Return list of stable weight points."""
    run_w = []
    w_stable = []

    for w in w_raw:
        if len(run_w) == 0 or np.var(run_w + [w]) <= var_threshold:
            run_w.append(w)
        else:
            if len(run_w) >= min_stable_samples:
                w_stable.append(np.mean(run_w))
            run_w = [w, ]

    # Insert last
    if len(run_w) >= min_stable_samples:
        w_stable.append(np.mean(run_w))

    return w_stable


def get_consumption(w_stable):
    """Return total consumption value."""
    consumption = 0
    prev_w = None

    for w in w_stable:
        if prev_w is not None and w < prev_w:
            consumption += prev_w - w
        prev_w = w

    return consumption


def calculate_score(consumption, temperatures):
    """Return final score based on consumption and temperatures"""
    score = 0

    def softmax(x):
        return np.exp(x) / np.sum(np.exp(x))

    temperature = np.mean(temperatures)
    score = softmax(consumption / temperature)

    return score
