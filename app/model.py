import numpy as np
import pandas

from datetime import datetime
from sklearn.linear_model import Lasso, Ridge
from mlxtend.regressor import StackingCVRegressor

LASSO_TARGET_PARAMS =      {'alpha': 0.07, 'max_iter': 4000}
RIDGE_TARGET_PARAMS =      {'alpha': 3000, 'max_iter': 2000}
LASSO_CONSTRAINTS_PARAMS = {'alpha': 0.5, 'max_iter': 2000}

CONSTRAINT_COLUMNS = ['sect1_pressure_delta_{}'.format(i) for i in range(1, 11)] +\
                     ['sect1_temperature_2',
                      'sect1_temperature_6',
                      'sect1_temperature_12',
                      'sect1_temperature_13',
                      'sect1_temperature_14']

TARGET_COLUMN = 'target'
TARGET_ABS_LIMIT = 20
TIMESTAMP_COLUMN = 'DateTime'


def generate_train_data(data,
                        target_column=TARGET_COLUMN,
                        constraint_columns=CONSTRAINT_COLUMNS,
                        timestamp_column=TIMESTAMP_COLUMN,
                        target_abs_limit=TARGET_ABS_LIMIT):
    data = data.copy()

    data[timestamp_column] = data[timestamp_column]\
        .apply(lambda t: datetime.strptime(t, '%Y-%m-%d %H:%M:%S').timestamp())

    for column in constraint_columns:
        data[column + '_next'] = np.append(data[column].values[1:], 0)

    bad_rows = []
    for i, ts in enumerate(data[timestamp_column].values):
        try:
            if data[timestamp_column][i + 1] - ts > 3600:
                bad_rows.append(i)

        except KeyError:
            break

    data = data[abs(data[target_column]) < target_abs_limit]
    data = data[~data.index.isin(bad_rows)]
    data = data[:-1]

    labels = data[[c + '_next' for c in constraint_columns] + [target_column]]
    labels.columns = constraint_columns + [target_column]

    train = data.drop([c + '_next' for c in constraint_columns] +
                      [timestamp_column, target_column], axis=1)

    return train, labels


class Model:
    def __init__(self,
                 lasso_target_params=LASSO_TARGET_PARAMS,
                 ridge_target_params=RIDGE_TARGET_PARAMS,
                 lasso_constraints_params=LASSO_CONSTRAINTS_PARAMS,
                 constraint_columns=CONSTRAINT_COLUMNS,
                 target_column=TARGET_COLUMN):

        self.target_estimator = StackingCVRegressor(regressors=(Lasso(**lasso_target_params),
                                                                Ridge(**ridge_target_params)),
                                                    meta_regressor=Ridge(alpha=0.01))
        self.constraints_estimator = Lasso(**lasso_constraints_params)

        self.constraint_columns = constraint_columns
        self.target_column = target_column

        self.test_columns = None

    def fit(self, data):
        '''
        Feed dataframe
        '''
        train, labels = generate_train_data(data)

        self.target_estimator.fit(train.values, labels[self.target_column].values)
        self.constraints_estimator.fit(train.values, labels[self.constraint_columns].values)

        self.test_columns = train.columns

    def predict(self, data):
        predicted_constraints = self.constraints_estimator.predict(data[self.test_columns].values)

        predicted_data = {self.constraint_columns[i]: constraint
                          for i, constraint in enumerate(predicted_constraints.T)}
        predicted_data[TARGET_COLUMN] = self.target_estimator.predict(data[self.test_columns].values)

        return pandas.DataFrame(predicted_data)
