from . import app
from .forms import CSV_Form
from flask import render_template, request, flash, redirect, url_for
import pandas
import random

def get_answer(params):
    manipulables = ['sect1_flow_16', 'sect1_flow_22', 'sect1_temperature_1',
                    'sect1_temperature_5', 'sect1_temperature_10',
                    'sect1_temperature_11']
    answer = {m: random.random() for m in manipulables}
    return answer

@app.route('/', methods=['GET', 'POST'])
def index():
    csv_form = CSV_Form()
    if csv_form.validate_on_submit():
        file = csv_form.file.data
        if file:
            filename = file.filename
            if filename == '' or filename is None:
                flash('Invalid filename.', 'error')
            else:
                filename = filename.split('.')
                extension = filename[-1]

                if extension not in app.config['ALLOWED_FORMATS']:
                    flash('Invalid file format.', 'error')
                else:
                    file.save('upload.csv')
                    df = pandas.read_csv('upload.csv')
                    try:
                        params = dict(df.iloc[0])
                        return render_template('index.html', form=csv_form, optimized=get_answer(params))
                    except:
                        flash('Invalid CSV file.', 'error')
        else:
            flash('Failed to fetch the file. Please try again.', 'error')
    else:
        for _, err_list in csv_form.errors.items():
            for err in err_list:
                flash(err, 'error')

    return render_template('index.html', form=csv_form)
