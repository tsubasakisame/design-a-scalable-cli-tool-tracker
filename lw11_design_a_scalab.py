import argparse
import json
import os
from datetime import datetime

class Tracker:
    def __init__(self, data_file):
        self.data_file = data_file
        self.data = self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        else:
            return {}

    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=4)

    def add_tracker(self, tracker_name):
        if tracker_name not in self.data:
            self.data[tracker_name] = []
            self.save_data()

    def add_entry(self, tracker_name, entry):
        if tracker_name in self.data:
            self.data[tracker_name].append({'timestamp': datetime.now().isoformat(), 'entry': entry})
            self.save_data()

    def get_entries(self, tracker_name):
        return self.data.get(tracker_name, [])

def main():
    parser = argparse.ArgumentParser(description='Scalable CLI tool tracker')
    parser.add_argument('command', choices=['add_tracker', 'add_entry', 'get_entries'])
    parser.add_argument('--tracker_name', required=True)
    parser.add_argument('--entry', required=False)
    parser.add_argument('--data_file', default='tracker_data.json', help='Data file to store tracker data')

    args = parser.parse_args()

    tracker = Tracker(args.data_file)

    if args.command == 'add_tracker':
        tracker.add_tracker(args.tracker_name)
        print(f'Tracker {args.tracker_name} added successfully')
    elif args.command == 'add_entry':
        if not args.entry:
            print('Error: --entry is required for add_entry command')
            return
        tracker.add_entry(args.tracker_name, args.entry)
        print(f'Entry {args.entry} added to tracker {args.tracker_name} successfully')
    elif args.command == 'get_entries':
        entries = tracker.get_entries(args.tracker_name)
        if not entries:
            print(f'Tracker {args.tracker_name} has no entries')
        else:
            print('Entries:')
            for entry in entries:
                print(f'Timestamp: {entry["timestamp"]}, Entry: {entry["entry"]}')

if __name__ == '__main__':
    main()