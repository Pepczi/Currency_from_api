import requests, csv

'''
Nie wiem czy był sens tworzenia funkcji poniżej, bo tak na prawde doszło więcej linijek kodu niż jak zmienne leżaly "wolne"
'''

# Zwraca słownik danych dot. walut oraz kursów ze strony banku.
def bank_info():
    response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
    all_info = response.json()
    for i in all_info:
        get_rates = i['rates']
    return get_rates

# Zwraca listę list wartości dot. kursu walut
def get_curr_values(data = bank_info()):
    currency_values = []
    for i in data:
        currency_values.append(list(i.values()))
    return currency_values

# Tworzenie pliku .csv z podanej wartosci
def save_to_csv(data = bank_info()):
    csv_file = open('kursy.csv', 'w', newline='')
    zapis_csv = csv.writer(csv_file, delimiter = ';')
    for i in data:
        zapis_csv.writerow(list(i.values()))
    csv_file.close()
    return

# Do Jinja
def for_jinja(data = get_curr_values()):
    currency_names = []
    for i in data:
        currency_names.append(i[0])
    return currency_names

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/currency/', methods = ['GET', 'POST'])
def currency_calculator():
    items = for_jinja()   # Do Jinja
    if request.method == "POST":
        post_data = request.form
        cash_to_exchange = float(post_data['value'])
        currency_purchase = post_data['currency']
        # Pętla bo zamota z wyświetleniem pełnej nazwy waluty np. "dolar" zamiast "dolar amerykański". Problem chyba z html?
        for i in bank_info():
            if i['currency'].startswith(str(currency_purchase)):
                currency = i['currency']
                currency_purchase = i['ask']
        total = round(cash_to_exchange * currency_purchase, 2)
        return f"Wymienisz {round(cash_to_exchange, 2)} {currency} na {total} PLN."

    return render_template('currency.html', items = items)

if __name__ == '__main__':
    save_to_csv()
    app.run(debug=True)