from . import app
from .forms import CSV_Form
from flask import render_template, flash
import pandas
from .model_to_backend import optimal_values
import sys, traceback


def get_answer(params):
    manipulables = ['sect1_flow_16', 'sect1_flow_22', 'sect1_temperature_1',
                    'sect1_temperature_5', 'sect1_temperature_10',
                    'sect1_temperature_11']

    x, target = optimal_values(params)
    predictions = {m: x[i] for i, m in enumerate(manipulables)}
    answer = {m: [params[m], predictions[m]] for m in manipulables}
    return answer, -target


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
                        params = df
                        optimized, target = get_answer(params)
                        return render_template('index.html',
                                               form=csv_form,
                                               optimized=optimized,
                                               target=target)
                    except Exception as err:
                        exc_info = sys.exc_info()
                        traceback.print_exception(*exc_info)
                        del exc_info
                        flash('Invalid CSV file.', 'error')
        else:
            flash('Failed to fetch the file. Please try again.', 'error')
    else:
        for _, err_list in csv_form.errors.items():
            for err in err_list:
                flash(err, 'error')

    return render_template('index.html', form=csv_form)
