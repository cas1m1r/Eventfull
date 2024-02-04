from evtx import PyEvtxParser as pevt
import json
import time
import os

def log_read(evt):
    parser = pevt(evt)
    log_data = []
    windows_events = load_event_types()
    for record in parser.records():
        data = parse_xml(record['data'])
        if 'EventID' in data.keys():
            event_id = data['EventID']
        elif 'EventRecordID' in data.keys():
            event_id = data['EventRecordID']
        else:
            event_id = ''
        if event_id in windows_events.keys():
            print(f'[{record["timestamp"]}] {windows_events[event_id]}')
            log_data.append({'time': record['timestamp'], 'description': windows_events[event_id]})
    return log_data


def parse_xml(data):
    structure = {}
    for x in data.split('\n'):
        tag = x[x.find('<') + 1:x.find('>')].replace('/','')
        value = x[x.find('>')+1:x.find('</')]
        structure[tag] = value
    return structure

def load_event_types():
    winevts = {}
    with open("C:\\Users\\Casim\\Documents\\2023\\Eventful\\events.txt", 'r') as f:
        lines = f.read().split('\n')
    f.close()
    for line in lines:
        fields = line.split('\t')
        provider = fields[0]
        id = fields[1].replace(' ', '')
        info = f"{provider}: {' '.join(fields[2:])}"
        if id not in winevts.keys():
            winevts[id] = info
    return winevts


def main():
    event_log_dir = 'C:\\Windows\\System32\\winevt\\Logs'
    root = "C:\\Users\\Casim\\Documents\\2023\\Eventful"

    fout = f"{time.strftime('%m_%d_%y_%H%M%S')}"
    os.mkdir(os.path.join(root, fout))
    for log in os.listdir(event_log_dir):
        print(f'[-] Parsing {log}')
        parsed = log_read(os.path.join(event_log_dir,log))
        if len(parsed):
            print(f'\tsaving results')
            open(os.path.join(fout,f'parsed_{log.split(".")[0]}.json'), 'w').write(json.dumps(parsed, indent=2))


if __name__ == '__main__':
    main()

