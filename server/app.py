from flask import request, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    return 'Index Page'

@app.route('/products')
def products():
    return 'Products'

if if __name__ == "__main__":
    app.run(debug=True)