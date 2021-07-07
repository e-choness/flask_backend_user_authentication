from flask import Flask, render_template

app = Flask(__name__)

class Demo:
    def __init__(self):
        self.name = "My Demo"

@app.route("/")
def home():

    # return "<h1>hello flask </h1>"
    return render_template("index1.html")


@app.route("/greet/<name>")
def greet(name):
    demo = Demo()
    # return f"<h1>Hello, {name}"
    return render_template("user1.html", content=name, x=42, demo=demo)


if __name__ == "__main__":
    app.run()
