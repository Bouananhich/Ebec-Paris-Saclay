from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)


@app.route('/')
def welcome():
    return render_template('home.html')


@app.route('/solution_multi')
def solution_multi():
    return render_template('solution_multi.html')


@app.route('/solution_uni')
def solution_uni():
    return render_template('solution_uni.html')


if __name__ == "__main__":
    app.run()
