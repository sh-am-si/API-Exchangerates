from flask import Flask, render_template, request
import csv

from exchangerates import read_request, write_rates

app = Flask(__name__)

def load_rates_from_csv():
    rates = {}
    items = []
    with open('exchangerates.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            currency = row['currency']
            code = row['code']
            bid = float(row['bid'])
            ask = float(row['ask'])
            if code not in items:
                items.append(code)
            rates[currency] = [code, bid, ask]

    return rates, items

def result_costs(amount, ask):
    return "%.2f" % (float(amount) * float(ask))

@app.route("/", methods=["GET", "POST"])
def calculate_currency():
    #costs = 0.0
    d = read_request()
    write_rates(d)
    rates, items = load_rates_from_csv()
    if request.method == "POST":
        data = request.form
        amount = data.get('amount')
        code = data.get('codes') 
        for rate in rates:
            if rates[rate][0] == code:
                name_currency = rate
                ask = float(rates[rate][2])
        costs = result_costs(amount, ask)
        result =  f"{amount} {name_currency} cost {costs} PLN"
        return render_template("calculator.html", items=items, result=result)
    #  
    return render_template("calculator.html", items=items)

if __name__ == "__main__":

    app.run(debug=True)

