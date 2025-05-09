import math
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
        
        compound_growth = math.pow((1 + annualReturn/100/12), (expectedRetirementAge - age) * 12)
        
        user_match = annualSalary * contribution
        employer_match = min(contribution, matchLimit) * annualSalary
        
        monthly_contribution = (user_match + employer_match) / 12
        monthly_return = annualReturn / 100 / 12
        
        #calculates the growth of the 401k balance up to retirement
        for i in range(expectedRetirementAge - age):
            annualSalary *= (1 + salaryIncrease / 100)
            user_match = annualSalary * contribution
            employee_match = min(contribution, matchLimit) * annualSalary
            monthly_contribution = (user_match + employer_match) / 12

            balance_401k += monthly_contribution * 12
            balance_401k *= (1 + annualReturn / 100)

        total_balance = balance_401k

        inflation_adjustment = math.pow(1 + inflationRate / 100, expectedRetirementAge - age)
        purchasing_power = balance_401k / inflation_adjustment
        
        retirementYears = lifeExpectancy - expectedRetirementAge
        retirementReturn = annualReturn / 100
        retirementInflation = inflationRate / 100
        
        #calculates annual withdrawal if the retirement return equals the inflation rate, otehrwise does the bottom
        if abs(retirementReturn - retirementInflation) < 0.000001:
            annual_withdrawal = balance_401k / retirementYears
        else:
            annual_withdrawal = balance_401k * (retirementReturn - retirementInflation) / (1 - math.pow((1 + retirementInflation) / (1 + retirementReturn), retirementYears))
        
        monthly_withdrawal = annual_withdrawal / 12
        initial_monthly_withdrawal = monthly_withdrawal
        
        for year in range(retirementYears):
            monthly_withdrawal *= (1 + inflationRate / 100)
            balance_401k -= monthly_withdrawal * 12

        deducted_balance = balance_401k

        response = {
            "Fixed Purchasing Power Withdrawal": f"If withdrawing at fixed purchasing power monthly, ${monthly_withdrawal:,.2f} per month can be withdrawn from age {expectedRetirementAge} and increase 3% per year until {lifeExpectancy}. It is equivalent to ${purchasing_power:,.2f} in purchasing power today.",

            "Fixed Amount Monthly Withdrawal": f"If withdrawing at fixed amount monthly, ${deducted_balance:,.2f} per month can be withdrawn in retirement until {lifeExpectancy}. At {expectedRetirementAge}, this is equivalent to ${purchasing_power:,.2f} in purchasing power today, and at {lifeExpectancy}, is equivalent to ${purchasing_power:,.2f}.",

            "Fixed Amount Annual Withdrawal": f"If withdrawing at fixed amount annually, ${annual_withdrawal:,.2f} per year can be withdrawn in retirement until {lifeExpectancy}. At {age}, this is equivalent to ${purchasing_power:,.2f} in purchasing power today, and at {lifeExpectancy}, is equivalent to ${purchasing_power:,.2f}."
        }

        return render_template('index.html', message = response)

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port= 8080, debug=True)
