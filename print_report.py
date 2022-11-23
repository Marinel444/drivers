from build_report import best_time

best_drivers = {}


def print_drivers():
    drivers = best_time()
    best_drivers_time = sorted(drivers.keys())
    for driver in best_drivers_time:
        for value in drivers.values():
            if drivers[driver] == value:
                best_drivers[driver] = value
    for timer, name in best_drivers.items():
        name = name.split('_')
        print(f"{name[0]} | {name[1]} | {timer}")


def main():
    print_drivers()


if __name__ == '__main__':
    main()
