import datetime
import os
import argparse

from dataclasses import dataclass

ABBREVIATIONS_FILENAME = 'abbreviations.txt'
START_LOG = 'start.log'
END_LOG = 'end.log'
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, 'DataFiles')


@dataclass
class Driver:
    driver_id: str
    name: str
    team: str
    lap_time: datetime.timedelta


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


def sorted_racer(racer_dict, desc=False):
    racer_print_sorted = {}
    best_drivers_time = sorted(racer_dict.keys())
    if desc != False:
        best_drivers_time.reverse()
    for driver in best_drivers_time:
        for value in racer_dict.values():
            if racer_dict[driver] == value:
                racer_print_sorted[driver] = value
    return racer_print_sorted


def build_report(desc=False):
    racer_print = {}

    abbreviations = parser_abbr_file(ABBREVIATIONS_FILENAME)
    best_drivers = best_time_lap()

    for name in abbreviations:
        for timer, driver_abbr in best_drivers.items():
            if driver_abbr in name:
                racer_print[timer] = name
    racer_print = sorted_racer(racer_print, desc)
    ready_list = []
    for timer, name in racer_print.items():
        name = name.split('_')
        ready_list.append(Driver(driver_id=name[0], name=name[1], team=name[2], lap_time=timer))
    return ready_list


def print_report(desc=False):
    ready_list = build_report(desc)
    if desc != False:
        count = len(ready_list)
    else:
        count = 1
    print(f'{"№":<2}| {"Code":<5}| {"Racer Name":<20}| {"Team":<30}| Time\n{"-" * 79}')
    for driver in ready_list:
        print(f'{count:<2}| {driver.driver_id:<5}| {driver.name:<20}| {driver.team:<30}| {driver.lap_time}')
        if count == 15:
            print(f'{"-" * 79}')
        if desc != False:
            count -= 1
        else:
            count += 1


def main():
    print_report(desc=False)


if __name__ == "__main__":
    main()
