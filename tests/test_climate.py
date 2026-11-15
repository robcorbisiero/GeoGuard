import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import requests

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
from services.climate import get_elevation, get_historical_climate


class ClimateDataTests(unittest.TestCase):
    @patch("services.climate.requests.get")
    def test_sea_level_is_valid_data(self, get):
        get.return_value = Mock(json=lambda: {"elevation": [0.0]})
        self.assertEqual(get_elevation(0, 0), 0.0)
        self.assertEqual(get.call_args.kwargs["timeout"], 15)

    @patch("services.climate.requests.get")
    def test_http_error_is_not_sea_level(self, get):
        get.return_value.raise_for_status.side_effect = requests.HTTPError("upstream error")
        self.assertIsNone(get_elevation(0, 0))

    @patch("services.climate.requests.get", side_effect=requests.Timeout)
    def test_timeout_is_not_climate_data(self, get):
        self.assertIsNone(get_historical_climate(0, 0))

    @patch("services.climate.requests.get")
    def test_missing_payload_is_not_zero_rainfall(self, get):
        get.return_value = Mock(json=lambda: {"error": True})
        self.assertIsNone(get_historical_climate(0, 0))

    @patch("services.climate.requests.get")
    def test_all_missing_measurements_are_unavailable(self, get):
        get.return_value = Mock(json=lambda: {"daily": {
            "temperature_2m_max": [None], "precipitation_sum": [None]}})
        self.assertIsNone(get_historical_climate(0, 0))

    @patch("services.climate.requests.get")
    def test_real_zero_rainfall_remains_valid(self, get):
        get.return_value = Mock(json=lambda: {"daily": {
            "temperature_2m_max": [20.0, 25.0], "precipitation_sum": [0.0, 0.0]}})
        self.assertEqual(get_historical_climate(0, 0),
                         {"avg_yearly_rainfall": 0.0, "max_temp": 25.0})


if __name__ == "__main__":
    unittest.main()
