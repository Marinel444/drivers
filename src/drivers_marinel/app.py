from flask import Flask, render_template, request
import race_report

app = Flask(__name__)


def get_build_report():
    drivers_dict = race_report.parse_abbreviations(race_report.ABBREVIATIONS_FILENAME)
    start_times = race_report.parse_log_file(race_report.START_LOG)
    end_times = race_report.parse_log_file(race_report.END_LOG)
    racers = race_report.build_report(start_times, end_times, drivers_dict)
    return racers


@app.route("/report", methods=['GET'])
def report_driver():
    racers = get_build_report()
    numbers = list(range(1, len(racers) + 1))
    if request.args.get('order'):
        racers.reverse()
        numbers.reverse()
    return render_template('report.html', drivers=racers, numbers=numbers)


@app.route("/drivers")
@app.route("/drivers/<racer_id>")
def drivers(racer_id=False):
    racers = get_build_report()
    if racer_id:
        for racer in racers:
            if racer.driver_id == racer_id:
                return render_template('driver_id.html', racer=racer)
    else:
        return render_template('drivers.html', title='Drivers', drivers=racers)


if __name__ == "__main__":
    app.run(debug=True)
