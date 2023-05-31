import csv
from jinja2 import Environment, FileSystemLoader
import sys
import yaml

def get_config(config_filename):
    with open(config_filename, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(f"Error reading {config_filename}:", exc)

def get_events(csv_filename):
    events = {}  # section : [event] 

    with open(csv_filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            event, section, speaker, speaker_role, date, time, link = row
            if section not in events:
                events[section] = []
            events[section].append({'event': event, 'speaker': speaker, 'speaker_role': speaker_role, 'date': date, 'time': time, 'link': link})
    
    return events

def render(events, header, subheader, section_order, output_html_filename):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('template.html')

    section_colors = {
        "Highlights": "#f8e0e6",
        "Politics": "#e0f0e6",
        "Tech": "#f8e6e0"
    }

    sections = [{"name": section, "color": section_colors[section]} for section in section_order]
    rendered_html = template.render(header=header, subheader=subheader, events=events, sections=sections)

    with open(output_html_filename, 'w') as file:
        file.write(rendered_html)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"usage: python3 {sys.argv[0]} config_filename")
        exit(1)

    config_filename = sys.argv[1]

    config = get_config(config_filename)

    csv_filename = config['events-csv']
    output_html_filename = config['html-output']
    header = config['header']
    subheader = config['subheader']
    section_order = config['section-order']

    events = get_events(csv_filename)
    render(events, header, subheader, section_order, output_html_filename)