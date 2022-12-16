import datetime
import os
import argparse

from dataclasses import dataclass

ABBREVIATIONS_FILENAME = 'abbreviations.txt'
START_LOG = 'start.log'
END_LOG = 'end.log'
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, '../../DataFiles')


@dataclass
class Driver:
    driver_id: str
    name: str
    team: str
    lap_time: datetime.timedelta


def parse_log_file(log_file):
    time_dict = {}
    with open(os.path.join(DATA_DIR, log_file)) as file:
        for line in file.readlines():
            if len(line) > 1:
                driver_id = line[:3].strip()
                time_str = line[3:].strip().split('_')[1]
                time_obj = datetime.datetime.strptime(time_str.strip(), '%H:%M:%S.%f')
                time_dict[driver_id] = time_obj
    return time_dict


def parse_abbreviations(abbr_file):
    drivers_dict = {}
    with open(os.path.join(DATA_DIR, abbr_file)) as file:
        for line in file.readlines():
            if len(line) > 1:
                driver_id, name, team = line.strip().split('_')
                drivers_dict[driver_id] = (name, team)
    return drivers_dict


def get_normal_time(start_time, finish_time):
    if start_time > finish_time:
        start_time, finish_time = finish_time, start_time
    return finish_time - start_time


def sorted_time_racer(lap_time, desc=False):
    sorted_best_time_dict = {}
    racer_best_time = sorted(lap_time.values())
    if desc:
        racer_best_time.reverse()
    for timer in racer_best_time:
        for abbr, best_time in lap_time.items():
            if timer == best_time:
                sorted_best_time_dict[abbr] = best_time
    return sorted_best_time_dict


def build_report(start_log, end_log, drivers_dict, desc=False):
    lap_time = {}
    drivers_list = []
    for start_abbr, start_time in start_log.items():
        for end_abbr, end_time in end_log.items():
            if start_abbr == end_abbr:
                lap_time[start_abbr] = str(get_normal_time(start_time, end_time))
    lap_time = sorted_time_racer(lap_time, desc)
    for abbr, timer in lap_time.items():
        for key, driver_info in drivers_dict.items():
            if abbr == key:
                drivers_list.append(Driver(driver_id=abbr, name=driver_info[0], team=driver_info[1], lap_time=timer))
    return drivers_list


def print_report(ready_list, desc=False, args_driver=None):
    if desc:
        count = len(ready_list)
    else:
        count = 1
    if args_driver is not None:
        for driver in ready_list:
            if driver.driver_id == args_driver:
                print(f'{"№":<2}| {"Code":<5}| {"Racer Name":<20}| {"Team":<30}| Time\n{"-" * 79}')
                print(f'{count:<2}| {driver.driver_id:<5}| {driver.name:<20}| {driver.team:<30}| {driver.lap_time}')
                break
            count += 1
    else:
        print(f'{"№":<2}| {"Code":<5}| {"Racer Name":<20}| {"Team":<30}| Time\n{"-" * 79}')
        for driver in ready_list:
            print(f'{count:<2}| {driver.driver_id:<5}| {driver.name:<20}| {driver.team:<30}| {driver.lap_time}')
            if count == 15:
                print(f'{"-" * 79}')
            if desc:
                count -= 1
            else:
                count += 1
                

def main():
    parser = argparse.ArgumentParser(description='F1 Report builder')
    parser.add_argument('--driver', help='Driver ID', required=False)
    parser.add_argument('--desc', action='store_true', help='Sorting in descending order', required=False)
    args = parser.parse_args()

    drivers_dict = parse_abbreviations(ABBREVIATIONS_FILENAME)
    start_times = parse_log_file(START_LOG)
    end_times = parse_log_file(END_LOG)

    drivers = build_report(start_times, end_times, drivers_dict, args.desc)
    # print_report(drivers, args.desc, args.driver)
    return drivers


if __name__ == "__main__":
    main()
