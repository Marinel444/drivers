import datetime
import os
import argparse

ABBREVIATIONS_FILENAME = 'abbreviations.txt'
START_LOG = 'start.log'
END_LOG = 'end.log'
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, 'DataFiles')


def parse_log_file(log_file):
    try:
        with open(os.path.join(DATA_DIR, log_file), encoding='utf-8') as file:
            list_file_log = file.read()
        list_file_log = list_file_log.strip().split('\n')
        list_file_log.sort()
        return list_file_log
    except Exception as e:
        print(e)


def parser_abbr_file(abbr_file):
    try:
        with open(os.path.join(DATA_DIR, abbr_file), encoding='utf-8') as file:
            abbreviations = file.read()
        abbreviations = abbreviations.strip().split('\n')
        return abbreviations
    except Exception as e:
        print(e)


def best_time_lap():
    best_drivers = {}
    start_logs = parse_log_file(START_LOG)
    end_logs = parse_log_file(END_LOG)
    if len(start_logs) != len(end_logs):
        raise Exception("Неправильное количество гоншиков в логе")
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
        best_drivers[str(best_time)] = start_log[0][:3]
        count += 1
    return best_drivers


def sorted_racer(racer_dict):
    racer_print_sorted = {}
    best_drivers_time = sorted(racer_dict.keys())
    for driver in best_drivers_time:
        for value in racer_dict.values():
            if racer_dict[driver] == value:
                racer_print_sorted[driver] = value
    return racer_print_sorted


def build_report():
    racer_print = {}

    abbreviations = parser_abbr_file(ABBREVIATIONS_FILENAME)
    best_drivers = best_time_lap()

    for name in abbreviations:
        for timer, driver_abbr in best_drivers.items():
            if driver_abbr in name:
                racer_print[timer] = name
    racer_print = sorted_racer(racer_print)
    print_table = []
    number = 1
    for timer, name in racer_print.items():
        name = name.split('_')
        if number == 16:
            print_table.append(f'{"-" * len(print_table[1])}')
        print_table.append(f'{number:<2}| {name[0]:<5}| {name[1]:<20}| {name[2]:<30}| {timer}')
        number += 1
    return print_table


def print_report(desc=False):
    print_table = build_report()

    if desc == True:
        print_table.reverse()
        
    print(f'{"№":<2}| {"Code":<5}| {"Racer Name":<20}| {"Team":<30}| Time\n{"-" * len(print_table[1])}')
    for i in print_table:
        print(i)


def main():
    print_report(desc=True)


if __name__ == "__main__":
    main()
