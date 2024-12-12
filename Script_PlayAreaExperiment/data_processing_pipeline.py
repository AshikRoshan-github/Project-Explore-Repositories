import pandas as pd
from sqlalchemy import create_engine
import json

# Read CSV
df = pd.read_csv(r"D:\Desktop_Backup\XMLTAG\INTERMEDIATEOUTPUTCSVFILEFORXML\210_212_ParticipantsConfigurationAnswer.csv")

# Replace gender values
df['gender'] = df['gender'].replace({'f': 'female', 'm': 'male'})

# Read XML template
with open(r'D:\Desktop_Backup\XMLTAG\XMLTAGNOTEPAD++\210_PrimaryInformation_XMLPath_Aupair_OnboardingConfiguration (1).txt', 'r', encoding='utf-8') as file:
    xml_content = file.read()

xml_template = ' '.join(xml_content.split())

# Function to generate XML for a row
def generate_xml(row):
    return xml_template.format(
        FN=row['first_name'],
        LN=row['last_name'],
        DOB=row['dob'],
        GENDER=row['gender'],
        CLPR=row['country_of_citizenship_id']
    )

# Apply the function to each row to create the new column
df['XMLforParticipantForm'] = df.apply(generate_xml, axis=1)

# Display the resulting DataFrame with additional columns
final_df = df[['UserId', 'XMLforParticipantForm', 'CreatedOn', 'UpdatedOn']]
final_df['ConfigurationId'] = 210
final_df['IsSelfFundedUser'] = 0

# Save the final DataFrame to CSV
final_df.to_csv(r"D:\Desktop_Backup\XMLTAG\XMLCSVFILE\ParticipantConfigurationAnswers_210.csv", index=False)
print("File is created successfully on 'D:\XMLTAG\XMLCSVFILE\ParticipantConfigurationAnswers_210.csv'")

# Read the second CSV file
df = pd.read_csv(r'D:\Desktop_Backup\XMLTAG\XMLCSVFILE\ParticipantConfigurationAnswers_212.csv')

# Convert date columns to datetime format
df['CreatedOn'] = pd.to_datetime(df['CreatedOn'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
df['UpdatedOn'] = pd.to_datetime(df['UpdatedOn'], format='%Y-%m-%d %H:%M:%S', errors='coerce')

# SQL Server connection details
server   = 'xxx'
database = 'xxx'
username = 'xxx'
password = 'xxx'

conn_str = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server'
engine = create_engine(conn_str)

# Column mapping for database insertion
column_mapping = {
    'UserId': 'UserId',
    'XMLforParticipantForm': 'XMLforParticipantForm',
    'ConfigurationId': 'ConfigurationId',
    'IsSelfFundedUser': 'IsSelfFundedUser',
    'CreatedOn': 'CreatedOn',
    'UpdatedOn': 'UpdatedOn'
}

df_mapped = df.rename(columns=column_mapping)

# Insert data into SSMS table, mapping only the specified columns
df_mapped.to_sql('ParticipantConfigurationAnswers', con=engine, if_exists='append', index=False)
