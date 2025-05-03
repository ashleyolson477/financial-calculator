from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/fillBlanks')
def fillBlanks():
    try:
        age = request.args.get('age')
        annualSalary = request.args.get('annual_salary')
        balance_401k = request.args.get('balance_401k')
        contribution = request.args.get('contribution')
        employee_match = request.args.get('employee_match')
        matchLimit = request.args.get('matchLimit')
        expectedRetirementAge = request.args.get('expectedRetirementAge')
        lifeExpectancy = request.args.get('lifeExpectancy')
        salaryIncrease = request.args.get('salaryIncrease')
        annualReturn = request.args.get('annualReturn')
        inflationRate = request.args.get('inflationRate')

        if not all([age, annualSalary, balance_401k, contribution, employee_match, matchLimit, expectedRetirementAge, lifeExpectancy, salaryIncrease, annualReturn, inflationRate]):
            return jsonify({'error': 'Missing required parameter(s).'}), 400

        try:
            age = int(age)
            annualSalary = float(annualSalary)
            balance_401k = float(balance_401k)
            contribution = float(contribution)
            employee_match = float(employee_match)
            matchLimit = float(matchLimit)
            expectedRetirementAge = int(expectedRetirementAge)
            lifeExpectancy = int(lifeExpectancy)
            salaryIncrease = float(salaryIncrease)
            annualReturn = float(annualReturn)
            inflationRate = float(inflationRate)
        except ValueError:
            return jsonify({'error': 'One or more parameters have an invalid value.'}), 400
        
        if age < 0:
            return jsonify({'error': 'Age must be 0 or older.'}), 400
        if expectedRetirementAge <= age:
            return jsonify({'error': 'Retirement age must be greater than age.'}), 400
        if lifeExpectancy < expectedRetirementAge:
            return jsonify({'error': 'Life expectancy age must be greater than or equal to retirement age.'}), 400
        if not annualSalary > 0:
            return jsonify({'error': 'Annual salary must be greater than 0.'}), 400
        if not balance_401k > 0:
            return jsonify({'error': '401k balance must be greater than 0.'}), 400
        if not (0 <= contribution <= 100):
            return jsonify({'error': 'Contribution percentage must be between 0 and 100.'}), 400
        if not (0 <= employee_match <= 100):
            return jsonify({'error': 'Employee match percentage must be between 0 and 100.'}), 400
        if not (0 <= matchLimit <= 100):
            return jsonify({'error': 'Match limit percentage must be between 0 and 100.'}), 400
        if not (0 <= annualReturn <= 100):
            return jsonify({'error': 'Annual return percentage must be between 0 and 100.'}), 400
        if not (0 <= inflationRate <= 100):
            return jsonify({'error': 'Inflation rate percentage must be between 0 and 100.'}), 400
        
        result = age + annualSalary
        return jsonify({'result': result})

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port= 8080, debug=True)
