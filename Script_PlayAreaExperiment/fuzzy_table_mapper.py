import json
from fuzzywuzzy import fuzz

# Load file names and table names from JSON files
with open(r'D:\JIFFY_PROJECT\Json_file\file_names_json.txt', 'r') as file:
    file_names_data = json.load(file)

with open(r'D:\JIFFY_PROJECT\Json_file\table_names_json.txt', 'r') as file:
    table_names_data = json.load(file)

# Preprocess file names and table names
preprocessed_file_names = [name.lower().replace('_', ' ') for name in file_names_data]
preprocessed_table_names = [name.lower().replace('_', ' ') for name in table_names_data]

# Initialize mapping dictionary
mapping_result = {}

# Perform column matching
for file_name in preprocessed_file_names:
    best_score = -1
    best_table_name = None
    for table_name, table_columns in table_names_data.items():
        if table_name.lower().replace('_', ' ') in preprocessed_table_names:
            for column in table_columns:
                column_score = fuzz.partial_ratio(file_name, column.lower().replace('_', ' '))
                if column_score > best_score:
                    best_score = column_score
                    best_table_name = table_name
    mapping_result[file_name] = best_table_name

# Output the mapping
for file_name, table_name in mapping_result.items():
    print(f"{file_name} --> {table_name}")
