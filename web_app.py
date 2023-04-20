from flask import Flask

app = Flask("web app, just for fun!")

@app.route('/')
def home():
    return 'Hello, World'

if __name__ == '__main__':
    app.run()