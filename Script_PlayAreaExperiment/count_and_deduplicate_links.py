import os
import pandas as pd

folder_path = r"D:\Webscraping\Txt file"

files = os.listdir(folder_path)

length_of_file = len(files)

links_list = []

for i in range(length_of_file):
    file_path = f"D:\\Webscraping\\Txt file\\{files[i]}"

    with open(file_path, 'r') as file:
        for line in file:
           
            links_list.append(line.strip())

data ={
    "links":links_list
}

df = pd.DataFrame(data)

df_rows = df.shape[0]

distinct_values = df.drop_duplicates()

distinct_values_rows = distinct_values.shape[0]

duplicates_present = df_rows - distinct_values_rows

print(f"\n\n Indistinct_Count:{df_rows} || Distinct_Count:{distinct_values_rows} || Duplicates_Present:{duplicates_present}\n\n")

distinct_values.to_excel("D:\Webscraping\Excelfile\Link_output.xlsx",index=False)
