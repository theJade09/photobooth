from flask import Flask, url_for, redirect
app = Flask(__name__, static_folder='static')

#url_for('static', filename='index.html')

@app.route('/')
def hello():
    return redirect(url_for('static', filename='index.html'))


if __name__ == '__main__':
    app.run(host='192.168.1.144', port=5000)
