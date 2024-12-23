import json
import csv
import os
from datetime import datetime

# User ID mapping
USER_MAP = {
    'U07JGC18B0': 'lukas@purpose.hr',
    'U07K56H4N9': 'shatabdi@purpose.hr',
    'U07FEPPJGN': 'kaouther@purpose.hr',
    'U0Q83UQBLK': 'ismail@purpose.hr',
    'U07A6KM9PT': 'gaby@purpose.hr',
    'U079B3HTE3': 'gregor@purpose.hr',
    'U084SLTJ79': 'dan@purpose.hr',
    'U078P177JA': 'mohib@purpose.hr',
    'U079A3046P': 'mieszko@purpose.hr',
    'U07AA0HY7K': 'wael@purpose.hr'


}

def get_channel_name(filename):
    # Map filename to channel name
    channel_mapping = {
        'lukas.json': 'lukas-greg',
        'shatabdi.json': 'shatabdi-greg',
        'kaouther.json': 'kaouther-greg',
        'ismail.json': 'ismail-greg',
        'gaby.json': 'gaby-greg',
        'dan.json': 'dan-greg',
        'mohib.json': 'mohib-greg',
        'mieszko.json': 'mieszko-greg',
        'wael.json': 'wael-greg',
        'backend.json': 'backend',
        'general.json': 'general',
        'be-fe.json': 'be-fe',
        'me-bl.json': 'me-bl',
        'be-fe.json': 'be-fe',
        'fe.json': 'fe',
        'design.json': 'design',
        'tech.json': 'tech'

        

    }
    return channel_mapping.get(filename, 'general')

def replace_user_mentions(text, user_map):
    # Replace <@USER_ID> with email addresses
    for user_id, email in user_map.items():
        text = text.replace(f'<@{user_id}>', email)
    return text

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
                
                # Replace @mentions in message text with email addresses
                text = replace_user_mentions(msg.get('text', ''), USER_MAP)
                
                row = [
                    msg.get('ts', ''),
                    channel,
                    user,
                    text
                ]
                writer.writerow(row)

# Directory containing JSON files
json_dir = 'exports/slack_export_2024-12-19_233201'


# Convert each JSON file to CSV
for filename in os.listdir(json_dir):
    if filename.endswith('.json'):
        json_path = os.path.join(json_dir, filename)
        csv_path = os.path.join(json_dir, filename.replace('.json', '.csv'))
        print(f"Converting {filename} to CSV...")
        json_to_csv(json_path, csv_path)

print("Conversion complete!")
