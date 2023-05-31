import csv
from jinja2 import Environment, FileSystemLoader
import sys

# Let's suppose your csv has columns: section, event, date, location


def get_events(csv_filename):
    events = {}  # We use a dictionary to store events by section

    with open(csv_filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            event, section, speaker, speaker_role, date, time, link = row
            if section not in events:
                events[section] = []
            events[section].append({'event': event, 'speaker': speaker, 'speaker_role': speaker_role, 'date': date, 'time': time, 'link': link})
    
    return events

def render(events, output_html_filename):
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('template.html')

    section_colors = {
        "Highlights": "#f8e0e6",
        "Politics": "#e0f0e6",
        "Tech": "#f8e6e0"
    }

    rendered_html = template.render(events=events, section_colors=section_colors)

    # Write the HTML output
    with open(output_html_filename, 'w') as file:
        file.write(rendered_html)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"usage: python3 {sys.argv[0]} csv_filename, output_html_filename")
        exit(1)

    csv_filename = sys.argv[1]
    output_html_filename = sys.argv[2]

    events = get_events(csv_filename)
    render(events, output_html_filename)