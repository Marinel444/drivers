import datetime
import os
from prettytable import PrettyTable

ABBREVIATIONS_FILENAME = 'abbreviations.txt'
START_LOG = 'start.log'
END_LOG = 'end.log'
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, 'DataFiles')
best_drivers = {}


def open_file_and_exception():
    try:
        with open(os.path.join(DATA_DIR, START_LOG), encoding='utf-8') as file:
            start_logs = file.read()
        start_logs = start_logs.strip().split('\n')
        start_logs.sort()
        with open(os.path.join(DATA_DIR, END_LOG), encoding='utf-8') as file:
            end_logs = file.read()
        end_logs = end_logs.strip().split('\n')
        end_logs.sort()
        with open(os.path.join(DATA_DIR, ABBREVIATIONS_FILENAME), encoding='utf-8') as file:
            abbreviations = file.read()
        abbreviations = abbreviations.strip().split('\n')
    except Exception as e:
        print(e)
    if len(start_logs) != len(end_logs):
        raise Exception("Неправильное количество гоншиков в логе")
    return start_logs, end_logs, abbreviations


def best_time_lap():
    start_logs, end_logs, abbreviations = open_file_and_exception()
    print(start_logs[1].split('_'))
    print(end_logs)
    print(abbreviations)
    count = 0
    while count <= len(start_logs) - 1:
        start_log = start_logs[count].split('_')
        time_start = datetime.datetime.strptime(start_log[1].strip(), '%H:%M:%S.%f')
        end_log = end_logs[count].split('_')
        time_end = datetime.datetime.strptime(end_log[1].strip(), '%H:%M:%S.%f')
        if time_end > time_start:
            best_time = time_end - time_start
        else:
            best_time = time_start - time_end
        for name in abbreviations:
            if start_log[0][:3] == name[:3]:
                name = name.split('_', maxsplit=1)
                best_drivers[str(best_time)] = name[1]
        count += 1


def build_report():
    best_time_lap()
    best_drivers_time = sorted(best_drivers.keys())
    for driver in best_drivers_time:
        for value in best_drivers.values():
            if best_drivers[driver] == value:
                best_drivers[driver] = value


def print_report():
    build_report()
    print_table = PrettyTable()
    print_table.field_names = ["№", "Racer Name", "Team", "Time"]
    number = 1
    for timer, name in best_drivers.items():
        name = name.split('_')
        if number == 16:
            print_table.add_row(['-', '-', '-', '-'])
        print_table.add_row([number, name[0], name[1], timer])
        number += 1
    print(print_table)


def main():
    print_report()


if __name__ == "__main__":
    main()
