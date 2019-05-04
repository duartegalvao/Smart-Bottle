import numpy as np

from .models import UserSettings


def classify(readings, user_settings):
    """
    Get raw data and return the final score.
    :param readings: Queryset of reading objects
    :param user_settings: User settings object (singleton)
    :return score: Score value (A to D, E and O)
    """
    temperatures = readings.values_list('temp', flat=True)
    w_raw = readings.values_list('weight', flat=True)

    w_stable = find_stable_points(w_raw)
    consumption = get_consumption(w_stable)

    if consumption < 0.1:
        return 'E'

    ideal_consumption = calculate_ideal_consumption(np.mean(temperatures),
                                                    user_settings.activity_level,
                                                    user_settings.get_age(),
                                                    user_settings.sex)
    score = get_score(consumption, ideal_consumption)

    return score, consumption, ideal_consumption


def smooth_readings(readings, var_threshold=0.1, min_stable_samples=3, min_w=0, max_w=1):
    """Return list of stable weight points."""
    run_w = []
    run_t = []
    w_stable = []

    for r in readings:
        if len(run_w) == 0 or np.var(run_w + [r.weight]) <= var_threshold:
            run_w.append(np.clip(r.weight, min_w, max_w))
            run_t.append(r.timestamp())
        else:
            if len(run_w) >= min_stable_samples:
                w_stable.append({
                    't': np.median(run_t),
                    'w': np.median(run_w),
                })
            run_w = [r.weight, ]
            run_t = [r.timestamp(), ]

    # Insert last
    if len(run_w) >= min_stable_samples:
        w_stable.append({
                    't': np.median(run_t),
                    'w': np.median(run_w),
                })

    return w_stable


# Auxiliary functions

def find_stable_points(w_raw, var_threshold=0.1, min_stable_samples=3, min_w=0, max_w=1):
    """Return list of stable weight points."""
    run = []
    w_stable = []

    for w in w_raw:
        if len(run) == 0 or np.var(run + [w]) <= var_threshold:
            run.append(np.clip(w, min_w, max_w))
        else:
            if len(run) >= min_stable_samples:
                w_stable.append(np.median(run))
            run = [w, ]

    # Insert last
    if len(run) >= min_stable_samples:
        w_stable.append(np.median(run))

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


def calculate_ideal_consumption(temperature, activity_level, age, sex):
    """Return ideal consumption value for given parameters."""
    # Pre-fit curves
    def fit_log(x):
        return 0.42601839 * np.log(1.18624985 * x) + 1.01016475

    def fit_sigmoid(x):
        return ((-1.0012868804199015) / (
                    1 + np.exp(x - 12.094927039206933) ** 0.7676654429522934)) + 0.9989052541075444

    # Known constants
    TA_POLY = {
        'SE': [-2.01666667e+00, 4.47962963e-01, -1.68888889e-02, 2.59259259e-04],
        'LA': [-1.93809524e+00, 4.57248677e-01, -1.56031746e-02, 2.59259259e-04],
        'AC': [-4.41190476e+00, 8.49021164e-01, -3.06349206e-02, 4.51851852e-04],
        'VA': [-2.21904762e+00, 6.20211640e-01, -1.93492063e-02, 3.18518519e-04]
    }
    SEX_VAL = {
        'M': 1,
        'F': 0
    }
    AVG_CONSUMPTION = 3

    # Clip inputs avoid meaningless data outside normal values
    tmp_c = np.clip(temperature, 15, 40)
    age_c = np.clip(age, 5, 35)
    # We start with an average value
    w_cons = AVG_CONSUMPTION
    # Now we add the temperature+activity level roughly normalized data
    w_cons += np.polynomial.polynomial.polyval(tmp_c, TA_POLY[activity_level]) - AVG_CONSUMPTION
    # Then, the sex+age roughly normalized data
    w_cons += fit_log(age_c) + SEX_VAL[sex] * fit_sigmoid(age) - AVG_CONSUMPTION

    return w_cons


def get_score(consumption, ideal_consumption):
    var = np.var([consumption, ideal_consumption])

    if consumption > ideal_consumption:
        if var > 0.6:
            score = 'O'
        else:
            score = 'A'
    elif var < 0.2:
        score = 'A'
    elif var < 0.5:
        score = 'B'
    elif var < 1:
        score = 'C'
    else:
        score = 'D'

    return score
