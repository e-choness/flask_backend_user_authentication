from flask import Flask

app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route('/')
def test():
    return "Welcome to the Flask Backend User Authentication System!"


if __name__ == "__main__":
    app.run(debug=True)
