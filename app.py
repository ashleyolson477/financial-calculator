from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

#Example for simple addition
@app.route('/add')
def add():
    try:
        a = float(request.args.get('a'))
        b = float(request.args.get('b'))
        return {'result': a + b}
    except:
        return {'error': 'Invalid input'}, 400

@app.route('/basicInfo')
def basicInfo():
    try:
        age = int(request.args.get('age'))        #age must be 0 or older?
        annualSalary = float(request.args.get('annual_salary'))        #make srue its in dollar amount
        balance_401k = float(request.args.get('balance_401k'))        #make srue its in dollar amount
        contribution = float(request.args.get('contribution'))  #percentage
        match = float(request.args.get('match'))    #percentage
        matchLimit = float(request.args.get('matchLimit'))      #percentage
        return {'result': age + annualSalary}        #calculate with the basic info
    except:
        return {'error': 'Invalid input'}, 400      #checking for valid inputs for each


@app.route('/printWithdrawal')
def printWithdrawl(balance):
    print("If withdrawinf at fixed purchase power monthly ..." + balance)


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port= 8080)