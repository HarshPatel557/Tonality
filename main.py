#library imports
import os
from pathlib import Path
from random import randint
from flask import Flask, render_template, request, redirect, url_for
from backend.pitch_detection import analysis

#specifying the app
app = Flask(__name__)

# Define the folder where uploaded files will be stored
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define a global variable to store the selected option
selected_option = None

#list of final messages
final_messages_list = ["that sounded amazing", "you played that so well", "what a great recording"]

#analysis values
percent_score = None
errors = None

#MAIN FLASK CODE

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/selection', methods=['GET', 'POST'])
def selection():
    global selected_option, percent_score, errors

    musicxml_file = None
    audio_file = None

    if request.method == 'POST':

        #delete all the existing contents of upload
        [f.unlink() for f in Path("uploads").glob("*") if f.is_file()]

        selected_option = request.form.get('selected_option')

        if 'mxl_file' in request.files:
            mxl_file = request.files['mxl_file']
            if mxl_file.filename != '':
                mxl_filename = os.path.join(app.config['UPLOAD_FOLDER'], mxl_file.filename)
                musicxml_file = mxl_filename
                mxl_file.save(mxl_filename)
                
        if 'audio_video_file' in request.files:
            audio_video_file = request.files['audio_video_file']
            if audio_video_file.filename != '':
                audio_video_filename = os.path.join(app.config['UPLOAD_FOLDER'], audio_video_file.filename)
                audio_file = audio_video_filename
                audio_video_file.save(audio_video_filename)

        #do calculations for the analysis
        percent_score, errors = analysis(selected_option, audio_file, musicxml_file)
        print(percent_score)
        print(errors)

        return redirect(url_for('result'))

    return render_template('selection.html')

@app.route('/result')
def result():
    global selected_option
    selected_final_message = final_messages_list[randint(0, 2)]

    return render_template('result.html', selected_option=selected_option, selected_final_message=selected_final_message, errors=errors)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
