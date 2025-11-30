from typing import Any
#Python library that makes it easier to read Excel files.
import pandas as panda

class FishLandings:
    def __init__(self, category: str, year: int, species: str, pounds: int):
        self.category = category
        self.year = year
        self.species = species
        self.pounds = pounds
    def __repr__(self):
        return f"category = {self.category}, "f"year = {self.year}, "f"species = {self.species}, "f"pounds = {self.pounds}\n"

# get_fish_landings_in_specified_year takes a year and sorts through the corresponding excell file from that year and returns a list of FishLandings objects.
# NOTE: Any fish species that have missing data or "confidential" data are omitted for accuracy purposes.
# Uses a python library called 'Pandas' which makes it easier to read Excel files.
def get_fish_landings_in_specified_year(year) -> list[FishLandings] | None:
    results = []
    if year < 1980 or year > 2002:
        print("invalid year")
        return None
    data_table = panda.read_excel(f"MonthlyPoundsSantaBarbara_{year}.xlsx")
    for index, row in data_table.iterrows():
        category = row["Category"]
        species = row["Species"]
        total_pounds = 0
        valid_row = True
        for month in data_table.columns[2:]:
            if row[month] == 'Confidential' or row[month] == 0:
                valid_row = False
                break
            else:
                total_pounds += row[month]
        if valid_row:
            results.append(FishLandings(category, year, species, total_pounds))
    return results

print(get_fish_landings_in_specified_year(1981))

