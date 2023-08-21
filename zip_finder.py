import pandas as pd
import re

df = pd.DataFrame()

csv_filename = "roasters"

def get_zip_code(address: str) -> str:
    zip_regex_pattern = "[0-9]{5}(?:-[0-9]{4})?"
    try:
        zip_code = re.findall(zip_regex_pattern, address)
    except TypeError:
        zip_code = None
    print(f"Orig Address: {address}\tZips Extracted: {zip_code}")
    try:
        return zip_code.pop()
    except (IndexError, AttributeError):
        return None

df = pd.read_csv(f'output/{csv_filename}.csv')
                            
addresses = df['Roaster Address'].to_numpy().tolist()
zip_codes = []
                            
for address in addresses:
    zip_codes.append(get_zip_code(address))

print(zip_codes)
    
df["Roaster Zip Code"] = zip_codes

df.to_csv(f'output/{csv_filename}-zip.csv')