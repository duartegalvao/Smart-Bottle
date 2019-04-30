import numpy as np

from .models import UserSettings


def classify(readings):
    """Get raw data and return the final score.

    Usage example: classify(BottleReading.objects.filter(time__gte=date_24h_ago).order_by('time'))
    """
    temperatures = readings.values_list('temp', flat=True)
    w_raw = readings.values_list('weight', flat=True)

    user_settings = UserSettings.get_solo()

    w_stable = find_stable_points(w_raw)
    consumption = get_consumption(w_stable)
    ideal_consumption = calculate_ideal_consumption(np.mean(temperatures),
                                                    user_settings.activity_level,
                                                    user_settings.get_age(),
                                                    user_settings.sex)
    score = calculate_score(consumption, ideal_consumption)

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


def calculate_score(consumption, ideal_consumption):
    """Return final score based on consumption and temperatures."""
    score = consumption - ideal_consumption

    return score
