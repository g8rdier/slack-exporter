import json
import csv
import os
from datetime import datetime

# User ID mapping
USER_MAP = {
    'U079JGC18B0': 'l.faber@purpose.hr',
    'U07KM56H4N9': 's.biswas@purpose.hr',
    'U07FNEPPJGN': 'k.mefteh@purpose.hr',
    'U07Q83UQBLK': 'i.cherri@purpose.hr',
    'U07A6SKM9PT': 'g.tatters@purpose.hr',
    'U079BG3HTE3': 'g.kobilarov@purpose.hr'
}

def get_channel_name(filename):
    # Map filename to channel name
    channel_mapping = {
        'greg.json': 'lukas-greg',
        'shatabdi.json': 'lukas-shatabdi',
        'kaouther.json': 'lukas-kaouther',
        'ismail.json': 'lukas-ismail',
        'gaby.json': 'lukas-gaby'
    }
    return channel_mapping.get(filename, 'general')

def json_to_csv(json_file, csv_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Get channel name from filename
    channel = get_channel_name(os.path.basename(json_file))
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        for msg in data:
            if msg.get('type') == 'message':
                # Skip USLACKBOT messages
                if msg.get('user') == 'USLACKBOT':
                    continue
                    
                # Replace user ID with email if it exists in mapping
                user = USER_MAP.get(msg.get('user', ''), msg.get('user', ''))
                
                row = [
                    msg.get('ts', ''),
                    channel,  # Use the channel name from filename
                    user,
                    msg.get('text', '')
                ]
                writer.writerow(row)

# Directory containing JSON files
json_dir = 'exports/slack_export_2024-12-18_000628'

# Convert each JSON file to CSV
for filename in os.listdir(json_dir):
    if filename.endswith('.json'):
        json_path = os.path.join(json_dir, filename)
        csv_path = os.path.join(json_dir, filename.replace('.json', '.csv'))
        print(f"Converting {filename} to CSV...")
        json_to_csv(json_path, csv_path)

print("Conversion complete!")