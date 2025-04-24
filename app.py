from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add')
def add():
    try:
        a = float(request.args.get('a'))
        b = float(request.args.get('b'))
        return {'result': a + b}
    except:
        return {'error': 'Invalid input'}, 400
    

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port= 8080)