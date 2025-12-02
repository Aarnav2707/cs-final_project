import unittest

import data_calculations as dc
from fish_landings import FishLandings
from PollutionRecord import PollutionRecord

Category = "California Waters Finfish"


class Tests(unittest.TestCase):
    def setUp(self):
        # Save originals so we can restore them in tearDown
        self.original_get_fish = dc.get_fish_landings_in_specified_year
        self.original_get_pollution = dc.get_pollution_data

        # ---- Fake fish landings ----
        # For any year Y between 1980 and 2002, we return one FishLandings
        # object whose pounds = Y - 1979.
        # So 1980 -> 1, 1981 -> 2, ..., 2002 -> 23.
        def fake_get_fish(year):
            pounds = year - 1979
            return [FishLandings(Category, year, "Fake Species", pounds)]

        # ---- Fake pollution data ----
        # We ignore the filename and just return fixed records:
        # two records for 1985 (DO 8.0 and 10.0) and one for 1986 (DO 5.0).
        def fake_get_pollution(_file):
            return [
                PollutionRecord("Santa Barbara", "1985-01-01", "8.0", "15.0"),
                PollutionRecord("Santa Barbara", "1985-06-01", "10.0", "16.0"),
                PollutionRecord("Santa Barbara", "1986-01-01", "5.0", "15.0"),
            ]

        dc.get_fish_landings_in_specified_year = fake_get_fish
        dc.get_pollution_data = fake_get_pollution

    def tearDown(self):
        # Restore original functions
        dc.get_fish_landings_in_specified_year = self.original_get_fish
        dc.get_pollution_data = self.original_get_pollution

    # -------- tests for fish landings calculations --------

    def test_average_fish_landings_per_year(self):
        # Pounds for years 1980..2002 are 1..23, average of 1..23 = 12
        avg = dc.average_fish_landings_per_year(Category)
        self.assertAlmostEqual(avg, 12.0)

    def test_total_fish_landings_in_year(self):
        # For year 1985, fake_get_fish returns pounds = 1985 - 1979 = 6
        total = dc.total_fish_landings_in_year(Category, 1985)
        self.assertEqual(total, 6)

    def test_compare_species_between_years(self):
        # 1980 -> 1, 1990 -> 11, so difference = 11 - 1 = 10
        diff = dc.compare_species_between_years(1980, 1990, Category)
        self.assertEqual(diff, 10)

    # -------- tests for oxygen / pollution calculations --------

    def test_average_oxygen_level_in_year(self):
        # From fake_get_pollution:
        # 1985 has two records: 8.0 and 10.0 => avg 9.0
        # 1986 has one record: 5.0 => avg 5.0
        avg_1985 = dc.average_oxygen_level_in_year(1985, Category)
        avg_1986 = dc.average_oxygen_level_in_year(1986, Category)
        self.assertAlmostEqual(avg_1985, 9.0)
        self.assertAlmostEqual(avg_1986, 5.0)

    # -------- tests for threshold interpretation --------

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

    # -------- test for pearson correlation --------

    def test_pearson_perfect_linear(self):
        # Here we override total_fish_landings_in_year and
        # average_oxygen_level_in_year to be perfectly linearly related
        # so Pearson correlation should be ~1.
        original_total = dc.total_fish_landings_in_year
        original_avg_oxy = dc.average_oxygen_level_in_year

        try:
            def fake_total(category_param, year_param):
                # 1..23
                return year_param - 1979

            def fake_avg_oxy(year_param, category_param):
                # exactly 2 * fake_total, so perfectly linear
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