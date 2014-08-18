from flask import Flask

app = Flask(__name__)
#add this so that flask doesn't swallow error messages
app.config['PROPAGATE_EXCEPTIONS'] = True


@app.route("/")
def base():
    return "<strong>hello from Flask and IDEA </strong>"

@app.route("/test")
def test():
    return "<strong>It actually worked</strong>"

if __name__ == "__main__":
    app.run()

