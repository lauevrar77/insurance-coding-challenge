import yaml
import csv

with open("nacebel.csv") as nacebel:
    nacebel.readline()  # Ignore header line
    nacebel.readline()  # Ignore Section line
    reader = csv.reader(nacebel, delimiter=";")
    codes = []
    for i, parts in enumerate(reader, start=1):
        try:
            data = {
                "model": "quotes.NacebelCode",
                "pk": i,
                "fields": {
                    "level": int(parts[0]),
                    "code": parts[1],
                    "parent_code": parts[2],
                    "label_nl": parts[3],
                    "label_fr": parts[4],
                    "label_de": parts[5],
                    "label_en": parts[6],
                },
            }
            codes.append(data)
        except Exception:
            print(f"Error on line {i}: {line}")
    with open("nacebel.yaml", "w") as f:
        yaml.dump(codes, f)
