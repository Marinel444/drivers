import datetime

best_drivers = {}


def best_time():
    with open('DataFiles/abbreviations.txt', encoding='utf-8') as file:
        abbreviations = file.read()
    abbreviations = abbreviations.strip().split('\n')
    with open('DataFiles/start.log', encoding='utf-8') as file:
        start_logs = file.read()
    start_logs = start_logs.strip().split('\n')
    with open('DataFiles/end.log', encoding='utf-8') as file:
        end_logs = file.read()
    end_logs = end_logs.strip().split('\n')
    start_logs.sort()
    end_logs.sort()
    count = 0
    while count <= 14:
        start_log = start_logs[count].split('_')
        time_start = datetime.datetime.strptime(start_log[1].strip(), '%H:%M:%S.%f')
        end_log = end_logs[count].split('_')
        time_end = datetime.datetime.strptime(end_log[1].strip(), '%H:%M:%S.%f')
        timer = time_end - time_start
        if '-1' in str(timer):
            timer = time_start - time_end
        for name in abbreviations:
            if start_log[0][:3] == name[:3]:
                name = name.split('_', maxsplit=1)
                best_drivers[str(timer)] = name[1]
        count += 1
    return best_drivers
