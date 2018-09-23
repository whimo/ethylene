from flask import Flask
import pandas
from .model import Model

app = Flask(__name__)
app.config.from_object('config')

attrs = pandas.read_excel('mk_dict.xlsx')
data = pandas.read_csv('mk_data.csv')
predictor = Model()

data_train = data
predictor.fit(data_train)

constrained = list(attrs[attrs['Constraint'] < 2]['Variable'])
manipulated = list(attrs[attrs['Manipulated'] < 2]['Variable'])
non_constrained = [m for m in manipulated if m not in constrained]
non_manipulated = [c for c in constrained if c not in manipulated]

from . import views
