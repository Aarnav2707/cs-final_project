from fish_landings import *
from PollutionRecord import *
from scipy.stats import pearsonr
category = "California Waters Finfish"
def average_fish_landings_per_year(category):
    total = 0
    for i in range(1980, 2003):
        lst = get_fish_landings_in_specified_year(i)
        for j in lst:
            if j.category == category:
                total+=j.pounds
    return total/23

average = average_fish_landings_per_year(category)
print(f"average {category} landings per year for {category} is {average_fish_landings_per_year(category)}")

total_fish_landings_year = 1985

def total_fish_landings_in_year(category, year):
    total = 0
    lst = get_fish_landings_in_specified_year(year)
    for i in lst:
        if i.category == category:
            total += i.pounds
    return total

print(f"total {category} pounds in {total_fish_landings_year} for {category} is {total_fish_landings_in_year(category, 1985)}")


def compare_species_between_years(year1, year2, category):
    difference = 0
    if 1980 <= year1 <= 2002 and 1980 <= year2 <= 2002:
        difference = total_fish_landings_in_year(category, year2) - total_fish_landings_in_year(category, year1)
    return difference

value = compare_species_between_years(1980, 1999, category)
print(f"the difference in {category} landings is {value}")

average_oxygen_level_year = 1985

def average_oxygen_level_in_year(year, category):
    total = 0
    count = 0
    year_record = 0
    lst = get_pollution_data("field_results_sb.csv")
    for i in lst:
        if "-" in i.date:
            year_record = float(i.date.split("-")[0])
        if year_record == year:
            total += float(i.dissolvedoxygen)
            count += 1

    if count == 0:
        return 0

    return total/count



average_oxygen = average_oxygen_level_in_year(1985, category)
print(f"the average oxygen level in {average_oxygen_level_year} is {average_oxygen}")

def pearson(category):
    fish_values = []
    oxygen_values = []
    for year in range(1980, 2003):
        fish_values.append(total_fish_landings_in_year(category, year))
        oxygen_values.append(average_oxygen_level_in_year(year, category))
    r, _ = pearsonr(fish_values, oxygen_values)
    return r

print(f"the pearson correlation coefficient is {pearson(category)}")

correlation_co = pearson(category)

def threshold(correlation) -> str:
    interpretation = ""
    if 0.75 < correlation <= 1:
        interpretation += "Strong positive correlation"
    elif 0.5 < correlation <= 0.75:
        interpretation += "Moderately positive correlation"
    elif 0.25 < correlation <= 0.5:
        interpretation += "Weak positive correlation"
    elif 0 < correlation <= 0.25:
        interpretation += "Very weak positive correlation"
    elif correlation == 0:
        interpretation += "no correlation"
    elif -0.25 < correlation < 0:
        interpretation += "Very weak negative correlation"
    elif -0.5 < correlation <= -0.25:
        interpretation += "Weak negative correlation"
    elif -0.75 < correlation <= -0.5:
        interpretation += "Moderately negative correlation"
    elif -1 < correlation <= -0.75:
        interpretation += "Strong Negative correlation"
    else:
        return "Error: invalid parameter (must be between -1 and 1 inclusive)"

    interpretation += f". Its important to not that correlation does not equal causation. \nThere are many other factors that could lead to changes in fish population. For example, fishing effort, species migration, seasonal cycles, habitat changes, and more.\nAlthough our data suggests a {interpretation}, it does not mean that lower oxygen levels cause a lower fish population even though lower oxygen levels are indicative of higher pollution."
    return interpretation

print(threshold(correlation_co))

