import csv
#Class containing all the pollution data
#Note: convert certain variables (date, dissolvedoxygen, and watertemp) to floats if needed because they are set as strings in the class.
class PollutionRecord:
    def __init__(self, location: str, date: str, dissolvedoxygen: str, watertemp: str):
        self.location = location
        self.date = date
        self.dissolvedoxygen = dissolvedoxygen
        self.watertemp = watertemp
    def __repr__(self):
        return f"location = {self.location}, " f"date = {self.date}, " f"dissolved oxygen = {self.dissolvedoxygen}, " f"water temp = {self.watertemp}\n"

#The function get_pollution_data takes the file field_results_sb.csv and returns a list of PollutionRecord objects made from each row of the file.
def get_pollution_data(file):
    results = []
    with open(file, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            for i in row:
                if row[8] == 'Santa Barbara':
                    water_pollution = PollutionRecord(row[8], row[10], row[5], row[15])
                    results.append(water_pollution)
    print(results)

#Prints results of get_pollution_data
get_pollution_data("field_results_sb.csv")
