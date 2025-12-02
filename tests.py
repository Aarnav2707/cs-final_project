import unittest

import data_calculations as dc
from fish_landings import FishLandings
from PollutionRecord import PollutionRecord

Category = "California Waters Finfish"


class Tests(unittest.TestCase):
    def setUp(self):
        self.original_get_fish = dc.get_fish_landings_in_specified_year
        self.original_get_pollution = dc.get_pollution_data

        def fake_get_fish(year):
            pounds = year - 1979
            return [FishLandings(Category, year, "Fake Species", pounds)]

        def fake_get_pollution(_file):
            return [
                PollutionRecord("Santa Barbara", "1985-01-01", "8.0", "15.0"),
                PollutionRecord("Santa Barbara", "1985-06-01", "10.0", "16.0"),
                PollutionRecord("Santa Barbara", "1986-01-01", "5.0", "15.0"),
            ]

        dc.get_fish_landings_in_specified_year = fake_get_fish
        dc.get_pollution_data = fake_get_pollution

    def tearDown(self):
        dc.get_fish_landings_in_specified_year = self.original_get_fish
        dc.get_pollution_data = self.original_get_pollution


    def test_average_fish_landings_per_year(self):
        avg = dc.average_fish_landings_per_year(Category)
        self.assertAlmostEqual(avg, 12.0)

    def test_total_fish_landings_in_year(self):
        total = dc.total_fish_landings_in_year(Category, 1985)
        self.assertEqual(total, 6)

    def test_compare_species_between_years(self):
        diff = dc.compare_species_between_years(1980, 1990, Category)
        self.assertEqual(diff, 10)


    def test_average_oxygen_level_in_year(self):
        avg_1985 = dc.average_oxygen_level_in_year(1985, Category)
        avg_1986 = dc.average_oxygen_level_in_year(1986, Category)
        self.assertAlmostEqual(avg_1985, 9.0)
        self.assertAlmostEqual(avg_1986, 5.0)


    def test_threshold_messages(self):
        self.assertTrue(
            dc.threshold(0.8).startswith("Strong positive correlation")
        )
        self.assertTrue(
            dc.threshold(0.6).startswith("Moderately positive correlation")
        )
        self.assertTrue(
            dc.threshold(0.3).startswith("Weak positive correlation")
        )
        self.assertTrue(
            dc.threshold(0.1).startswith("Very weak positive correlation")
        )
        self.assertTrue(
            dc.threshold(0.0).startswith("no correlation")
        )
        self.assertTrue(
            dc.threshold(-0.1).startswith("Very weak negative correlation")
        )
        self.assertTrue(
            dc.threshold(-0.3).startswith("Weak negative correlation")
        )
        self.assertTrue(
            dc.threshold(-0.6).startswith("Moderately negative correlation")
        )
        self.assertTrue(
            dc.threshold(-0.8).startswith("Strong Negative correlation")
        )


    def test_pearson_perfect_linear(self):
        original_total = dc.total_fish_landings_in_year
        original_avg_oxy = dc.average_oxygen_level_in_year

        try:
            def fake_total(category_param, year_param):
                return year_param - 1979

            def fake_avg_oxy(year_param, category_param):
                return (year_param - 1979) * 2

            dc.total_fish_landings_in_year = fake_total
            dc.average_oxygen_level_in_year = fake_avg_oxy

            r = dc.pearson(Category)
            self.assertAlmostEqual(r, 1.0, places=6)
        finally:
            dc.total_fish_landings_in_year = original_total
            dc.average_oxygen_level_in_year = original_avg_oxy


if __name__ == "__main__":
    unittest.main()