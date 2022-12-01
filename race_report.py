import datetime
import os

ABBREVIATIONS_FILENAME = 'abbreviations.txt'
START_LOG = 'start.log'
END_LOG = 'end.log'
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, 'DataFiles')
best_drivers = {}


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
    start_logs = parse_log_file(START_LOG)
    end_logs = parse_log_file(END_LOG)
    if len(start_logs) != len(end_logs):
        raise Exception("Неправильное количество гоншиков в логе")
    abbreviations = parser_abbr_file(ABBREVIATIONS_FILENAME)
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
                best_drivers[str(best_time)] = f'{name[0]}_{name[1]}'
        count += 1


def build_report():
    best_time_lap()
    best_drivers_time = sorted(best_drivers.keys())
    for driver in best_drivers_time:
        for value in best_drivers.values():
            if best_drivers[driver] == value:
                best_drivers[driver] = value


def print_report(asc):
    build_report()
    number = 1
    print_table = []
    for timer, name in best_drivers.items():
        name = name.split('_')
        if number == 16:
            print_table.append(f'{"-" * len(print_table[1])}')
        print_table.append(f'{number:<2}| {name[0]:<5}| {name[1]:<20}| {name[2]:<30}| {timer}')
        number += 1
    if asc == False:
        print_table.reverse()
    print(f'{"№":<2}| {"Code":<5}| {"Racer Name":<20}| {"Team":<30}| Time\n{"-" * len(print_table[1])}')
    for i in print_table:
        print(i)


def main():
    print_report(asc=False)


if __name__ == "__main__":
    main()
