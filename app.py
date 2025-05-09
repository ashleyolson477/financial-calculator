import math
import os
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
            balance_401k = float(balance_401k) if balance_401k else 0
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
        
        #percents to decimals
        contribution = contribution / 100
        employee_match = employee_match / 100
        matchLimit = matchLimit / 100
        annualReturn = annualReturn / 100
        inflationRate = inflationRate / 100
        salaryIncrease = salaryIncrease / 100
        
        years_to_retirement = expectedRetirementAge - age
        retirement_years = lifeExpectancy - expectedRetirementAge

        annual_return = annualReturn
        monthly_return = annual_return / 12
        inflation_rate = inflationRate
        salary_growth = salaryIncrease

        #401k growth up to retirement age
        for year in range(years_to_retirement):
            annualSalary *= (1 + salary_growth)
            user_contrib = annualSalary * contribution
            employer_contrib = min(contribution, matchLimit) * employee_match * annualSalary
            total_annual_contrib = user_contrib + employer_contrib
            monthly_contrib = total_annual_contrib / 12

            #simulates compoudong of investments on monthly basis
            for i in range(12):
                balance_401k *= (1 + monthly_return)
                balance_401k += monthly_contrib

        #balance at retirement
        retirement_balance = balance_401k

        #current value of money
        purchasing_power = retirement_balance / ((1 + inflation_rate) ** years_to_retirement)

        # Withdrawal calculations
        #fixed real (purchasing power) monthly withdrawal
        if abs(annual_return - inflation_rate) < 0.000001:
            real_annual_withdrawal = retirement_balance / retirement_years
        else:
            real_annual_withdrawal = retirement_balance * (annual_return - inflation_rate) / (
                1 - ((1 + inflation_rate) / (1 + annual_return)) ** retirement_years)

        real_monthly_withdrawal = real_annual_withdrawal / 12
        
        #fixed nominal (non-inflation-adjusted) monthly withdrawal
        nominal_annual_withdrawal = retirement_balance * annual_return / (1 - (1 / (1 + annual_return) ** retirement_years))
        nominal_monthly_withdrawal = nominal_annual_withdrawal / 12

        #present value of first and last nominal monthly withdrawals
        pv_nominal_monthly_start = nominal_monthly_withdrawal / ((1 + inflation_rate) ** years_to_retirement)
        pv_nominal_monthly_end = nominal_monthly_withdrawal / ((1 + inflation_rate) ** (years_to_retirement + retirement_years - 1))

        #fixed nominal annual withdrawal
        pv_nominal_annual_start = nominal_annual_withdrawal / ((1 + inflation_rate) ** years_to_retirement)
        pv_nominal_annual_end = nominal_annual_withdrawal / ((1 + inflation_rate) ** (years_to_retirement + retirement_years - 1))

        response = {
            "Retirement Balance Summary": f"At the retirement age of {expectedRetirementAge}, the 401(k) balance will be ${retirement_balance:,.0f}, which is equivalent to ${purchasing_power:,.0f} in purchasing power today.",
            
            "Fixed Purchasing Power Withdrawal": f"If withdrawing at fixed purchasing power monthly, ${real_monthly_withdrawal:,.2f} per month can be withdrawn from age {expectedRetirementAge + 1} and increase 3% per year until {lifeExpectancy}. It is equivalent to ${real_monthly_withdrawal / ((1 + inflation_rate) ** years_to_retirement):,.2f} in purchasing power today.",

            "Fixed Amount Monthly Withdrawal": f"If withdrawing at fixed amount monthly, ${nominal_monthly_withdrawal:,.2f} per month can be withdrawn in retirement until {lifeExpectancy}. At {expectedRetirementAge + 1}, this is equivalent to ${pv_nominal_monthly_start:,.2f} in purchasing power today, and at {lifeExpectancy}, is equivalent to ${pv_nominal_monthly_end:,.2f}.",

            "Fixed Amount Annual Withdrawal": f"If withdrawing at fixed amount annually, ${nominal_annual_withdrawal:,.2f} per year can be withdrawn in retirement until {lifeExpectancy}. At {expectedRetirementAge}, this is equivalent to ${pv_nominal_annual_start:,.2f} in purchasing power today, and at {lifeExpectancy}, is equivalent to ${pv_nominal_annual_end:,.2f}."
        }


        return render_template('index.html', message = response)

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
