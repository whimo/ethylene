from app import app
from flask import render_template, request
import pandas

def get_answer(params):
    manipulables = ['sect1_flow_16', 'sect1_flow_22', 'sect1_temperature_1',
                    'sect1_temperature_5', 'sect1_temperature_10',
                    'sect1_temperature_11']
    answer = {m: random.random() for m in manipulables}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('index'))
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('index'))

        if file:
            file.save('upload.csv')
            df = pandas.read_csv('upload.csv')
            params = dict(df.iloc[1])
            return render_template('index.html', answer=get_answer(params))

