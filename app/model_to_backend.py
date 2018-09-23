import numpy as np
from app import manipulated, predictor, non_manipulated, attrs, data
from scipy.optimize import minimize


def _prep_df(base, x):
    df = base.copy(True)
    for i, key in enumerate(manipulated):
        df[key] = np.array([x[i]])

    return df


def optimal_values(row):
    base_df = row.copy(True)

    def get_target(x):
        return -float(predictor.predict(_prep_df(base_df, x))['target'])

    def validate_min(x):
        print(x, get_target(x))
        res = np.e * 5
        pred = predictor.predict(_prep_df(base_df, x))
        for con in non_manipulated:
            m = float(attrs.loc[attrs['Variable'] == con]['Min'])
            res -= np.exp((m - float(pred[con])))

        return res

    def validate_max(x):
        res = np.e * 5
        pred = predictor.predict(_prep_df(base_df, x))
        for con in non_manipulated:
            M = float(attrs.loc[attrs['Variable'] == con]['Max'])
            res -= np.exp((float(pred[con]) - M))

        return res

    cons = ({'type': 'ineq', 'fun': validate_min},
            {'type': 'ineq', 'fun': validate_max},
            {'type': 'ineq', 'fun': lambda x: x[5] + 2},
            {'type': 'ineq', 'fun': lambda x: -x[5] + 4},
            {'type': 'ineq', 'fun': lambda x: -x[2] + 4},
           )

    init = [float(data.iloc[0][_]) for _ in manipulated]

    x = minimize(get_target,
                 init,
                 constraints=cons,
                 method='COBYLA',
                 options={'maxiter': 300, 'disp': True}).x

    return x, get_target(x)
