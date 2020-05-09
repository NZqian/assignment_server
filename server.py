from flask import Flask, request, redirect, render_template, url_for
import pandas as pd
import os

allowedTypes = ['md', 'MD', 'gz']
allowedNames = list(pd.read_csv("names.csv"))


class NameException(Exception):
    pass
class SuffixException(Exception):
    pass

app = Flask(__name__)

def filenameCheck(filename, allowedNames, allowedTypes):
    if filename == '' or (filename.split('.')[-1] not in allowedTypes):
        raise SuffixException
    if filename.split('.')[0] not in allowedNames:
        raise NameException

@app.route('/')
def index():
    return render_template("main.html")

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == "POST":
        f = request.files["file"]

        try:
            filenameCheck(f.filename, allowedNames, allowedTypes)
        except NameException:
            return redirect(url_for('fail_name'))
        except SuffixException:
            return redirect(url_for('fail_suffix'))
        else:   
            save_path = "/home/ning/assignment/week5/"
            path = os.path.join(save_path,f.filename)
            f.save(path)
            print(f.filename)
            return redirect(url_for('success'))

    return render_template("submit.html")

@app.route('/success')
def success():
    return render_template("success.html")

@app.route('/fail')
def fail():
    return render_template("fail.html")

@app.route('/fail_name')
def fail_name():
    return render_template("fail_name.html")

@app.route('/fail_suffix')
def fail_suffix():
    return render_template("fail_suffix.html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=433, ssl_context=("./ning.crt", "./ning.key"))
