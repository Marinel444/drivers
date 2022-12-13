from flask import Flask, render_template, request
from src.drivers_marinel.race_report import main

app = Flask(__name__)

menu = ['Установка', "Новое приложение", 'Обратная связь']


@app.route("/")
def index():
    return render_template('report.html', title="Report")


@app.route("/report", methods=['POST', 'GET'])
def report_driver():
    drivers = main()
    numbers = list(range(1,len(drivers)+1))
    if request.method == 'POST':
        drivers.reverse()
        numbers.reverse()
    return render_template('report.html', drivers=drivers, numbers=numbers)


@app.route("/drivers")
@app.route("/drivers/<racer_id>")
def drivers(racer_id=False):
    drivers = main()
    if racer_id:
        for racer in drivers:
            if racer.driver_id == racer_id:
                return render_template('driver_id.html', racer=racer)
    else:
        return render_template('drivers.html', title='Drivers', drivers=drivers)


@app.route("/profile")
@app.route("/profile/<username>")
def profile(username=False):
    return f"Пользователь: {username}"


if __name__ == "__main__":
    app.run(debug=True)
