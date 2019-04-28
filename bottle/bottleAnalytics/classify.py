import numpy as np


def find_stable_points(w_raw, var_threshold=0.1, min_stable_samples=3):
    """Return list of stable weight points."""
    run_w = []
    run_t = []
    w_stable = []

    for v in w_raw:
        if len(run_w) == 0 or np.var(run_w + [v.weight]) <= var_threshold:
            run_w.append(v.weight)
            run_t.append(v.time)
        else:
            if len(run_w) >= min_stable_samples:
                w_stable.append((np.mean(run_t), np.mean(run_w)))
            run_w = [v.weight, ]
            run_t = [v.time, ]

    # Insert last
    if len(run_w) >= min_stable_samples:
        w_stable.append((np.mean(run_t), np.mean(run_w)))

    return w_stable


def get_consumptions(W_stable):
    consumptions = []
    # TODO

    return consumptions


def calculate_score(consumptions, temperatures):
    score = 0
    # TODO

    return score


def classify(data):
    w_stable = find_stable_points(data)
    consumptions = get_consumptions(w_stable)
    score = calculate_score(consumptions, data)

    return score
