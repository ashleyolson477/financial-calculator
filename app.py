from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

#Example for simple addition
#@app.route('/add')
#def add():
#    try:
#        a = float(request.args.get('a'))
#        b = float(request.args.get('b'))
#        return {'result': a + b}
#    except:
#        return {'error': 'Invalid input'}, 400

@app.route('/fillBlanks')
def fillBlanks():
    try:
        # Try to get and validate inputs
        age = request.args.get('age')
        annualSalary = request.args.get('annual_salary')
        balance_401k = request.args.get('balance_401k')
        contribution = request.args.get('contribution')
        employee_match = request.args.get('employee_match')  # Updated from 'match' to 'employee_match'
        matchLimit = request.args.get('matchLimit')
        expectedRetirementAge = request.args.get('expectedRetirementAge')
        lifeExepctancy = request.args.get('lifeExpectancy')
        salaryIncrease = request.args.get('salaryIncrease')
        annualReturn = request.args.get('annualReturn')
        inflationRate = request.args.get('inflationRate')

        # Check if any of the parameters are missing
        if not all([age, annualSalary, balance_401k, contribution, employee_match, matchLimit, expectedRetirementAge, lifeExepctancy, salaryIncrease, annualReturn, inflationRate]):
            return jsonify({'error': 'Missing required parameter(s).'}), 400

        # Convert inputs to proper types and handle invalid input types
        try:
            age = int(age)
            annualSalary = float(annualSalary)
            balance_401k = float(balance_401k)
            contribution = float(contribution)
            employee_match = float(employee_match)  # Updated to match the new name
            matchLimit = float(matchLimit)
            expectedRetirementAge = float(expectedRetirementAge)
            lifeExepctancy = float(lifeExepctancy)
            salaryIncrease = float(salaryIncrease)
            annualReturn = float(annualReturn)
            inflationRate = float(inflationRate)
        except ValueError:
            return jsonify({'error': 'One or more parameters have an invalid value.'}), 400
        
        # Logical checks on the values
        if age < 0:
            return jsonify({'error': 'Age must be 0 or older.'}), 400
        if not (0 <= contribution <= 100):
            return jsonify({'error': 'Contribution percentage must be between 0 and 100.'}), 400
        if not (0 <= employee_match <= 100):  # Updated here as well
            return jsonify({'error': 'Employee match percentage must be between 0 and 100.'}), 400
        if not (0 <= matchLimit <= 100):
            return jsonify({'error': 'Match limit percentage must be between 0 and 100.'}), 400
        if not (0 <= annualReturn <= 100):
            return jsonify({'error': 'Annual return percentage must be between 0 and 100.'}), 400
        if not (0 <= inflationRate <= 100):
            return jsonify({'error': 'Inflation rate percentage must be between 0 and 100.'}), 400
        
        # Calculate with the basic info (return a placeholder calculation)
        result = age + annualSalary  # Example calculation, you can modify based on actual requirements
        return jsonify({'result': result})

    except Exception as e:
        # Catch any unexpected errors
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port= 8080, debug=True)