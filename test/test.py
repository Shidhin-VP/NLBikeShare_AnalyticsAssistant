import pytest

@pytest.mark.parametrize("question,expected_keywords",[
    ("What was the average ride time for journeys that started at Congress Avenue in June 2025?", ["SELECT", "AVG", "ride_time", "Congress Avenue", "2025-06-01"]),
    ("Which docking point saw the most departures during the first week of June 2025?", ["SELECT", "COUNT", "docking_point", "2025-06-01"]),
    ("How many kilometres were ridden by women on rainy days in June 2025?", ["SELECT", "SUM", "distance", "women", "rainy", "2025-06-01"])
])

def test_sql_generation_real(question,expected_keywords):
    ""