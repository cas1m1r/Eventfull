import random
import string
import json
import os

lets = list(string.ascii_letters)

def random_file():
    return ''.join(random.sample(lets, 4))

def run(cmd):
    tmp = random_file()
    os.system(f'{cmd} > {tmp}')
    with open(tmp,'r') as f:
        result = f.read()
    f.close()
    os.remove(tmp)
    return result

def non_empty(elmts):
    items = []
    for e in elmts:
        if len(e):
            items.append(e)
    return items


def load_event_types(ev_path):
    winevts = {}
    with open(ev_path, 'r') as f:
        lines = f.read().split('\n')
    f.close()
    for line in lines:
        fields = line.split('\t')
        id = fields[0].replace(' ', '')
        info = ' '.join(fields[3:])
        if id not in winevts.keys():
            winevts[id] = info
    return winevts


def get_events(category):
    events = []
    cmd = f'Get-EventLog "{category}"'
    for ln in run(f'powershell -command {cmd}').split('\n'):
        fields = non_empty(ln.split(' '))
        # index , time, entryType, source, id, message
        if len(fields) > 6:
            index = fields[0]
            tstamp = ' '.join(fields[1:4])
            eventType = fields[4]
            source = fields[5]
            message = ' '.join(fields[7:])
            events.append({'time': tstamp, 'type': eventType, 'source': source, 'info': message})
    open(f'{category}.json', 'w').write(json.dumps(events,indent=2))
    return events


def main():
    winevts = load_event_types('events.txt')
    apps = get_events('Application')
    system = get_events("System")
    get_events("Security")


if __name__ == '__main__':
    main()
