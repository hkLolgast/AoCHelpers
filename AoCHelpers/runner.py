import argparse
import datetime
import importlib
import os
import time

import generator
import pywatch

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--day', help="Which day to run")
    parser.add_argument('-g', '--generate', action='store_true',  help="Whether todays files should be generated")
    parser.add_argument('-t', '--time', action='store_true')
    parser.add_argument('--debug', action='store_true')
    return parser.parse_args()

def run(year = None):
    args = parse_arguments()
    if year is None:
        year = datetime.datetime.today().year
    if args.day is None:
        day = datetime.datetime.today().day
    else:
        day = int(args.day)
    
    if not args.generate and not os.path.exists(f"day{day:0>2}.py"):
        raise ValueError(f"Generator parameter was not supplied and file doesn't exist: day{day:0>2}.py")
    if args.generate:
        generator.generate(day)
    elif args.time:
        module = importlib.import_module(f"day{day:0>2}")
        t0 = time.time()
        print(module.main())
        print(f'Done in {time.time() - t0} s')
    else:
        day = f'{day:0>2}'
        watcher = pywatch.Watcher(f'day{day}.py', 'main', f'day{day}example.txt', f'day{day}.txt')
        watcher.watch()