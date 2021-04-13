from flask import Flask, redirect, render_template, request, url_for, flash
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'csv', 'txt'}
app.config['UPLOAD_FOLDER'] = './'
app.config['SECRET_KEY'] = 'f3cfe9ed8fae309f02079dbf'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def welcome():
    return render_template('home.html')

@app.route('/solution_uni' ,methods=['GET','POST'])
def solution_uni():
    return render_template('solution_uni.html')

@app.route('/solution_multi',methods=['GET','POST'])
def solution_multi():
    return render_template('solution_multi.html')



@app.route('/uni_form', methods=['POST'])
def uni_form():#faire les cas d'erreur car pas de string
    data = request.form.to_dict(flat=False)
    print(data)
    coord_input = []
    for i in range(len(data)//2):
        coord_input.append((float(data.get('latitude'+str(i+1),[0])[0]),float(data.get('longitude'+str(i+1),[0])[0])))
    print(coord_input)
    return render_template('solution_uni.html')

@app.route('/uni_csv', methods=['POST','GET'])
def uni_csv():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(filename)
            flash('file successfully upload')
            return render_template('solution_uni.html')
    
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/multi_form', methods=['POST'])
def multi_form():#faire la récupération
    data = request.form.to_dict(flat=False)
    print(data)
    return render_template('solution_multi.html')

@app.route('/multi_csv', methods=['POST'])
def multi_csv():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(filename)
            return render_template('solution_multi.html')
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
if __name__ == "__main__":
    app.run()
