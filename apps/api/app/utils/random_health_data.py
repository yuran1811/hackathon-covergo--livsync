"""
Random Health Data Generator
Tạo dữ liệu sức khỏe ngẫu nhiên trong các ngưỡng cố định
"""

import json
import random
from datetime import datetime, timedelta
from typing import Any


class HealthDataGenerator:
    """Generator for random health data"""

    HEALTH_RANGES = {
        "steps": {"min": 3000, "max": 15000},
        "distance_meters": {"min": 2000, "max": 12000},
        "calories_burned": {"min": 800, "max": 3000},
        "sleep_duration": {"min": 4.0, "max": 10.0},
        "sleep_quality": {"min": 30, "max": 100},
        "heart_rate": {"min": 50, "max": 120},
        "stress_score": {"min": 10, "max": 100},
        "bp_systolic": {"min": 90, "max": 180},
        "bp_diastolic": {"min": 60, "max": 110},
        "blood_glucose": {"min": 70, "max": 200},
        "blood_oxygen": {"min": 85, "max": 100},
    }

    @classmethod
    def generate_single_health_data(cls) -> dict[str, Any]:
        """Generate a single health data"""
        data = {}

        for key, range_config in cls.HEALTH_RANGES.items():
            if key == "sleep_duration":
                data[key] = round(
                    random.uniform(range_config["min"], range_config["max"]), 1
                )
            else:
                data[key] = random.randint(range_config["min"], range_config["max"])

        data["blood_pressure"] = f"{data['bp_systolic']}/{data['bp_diastolic']}"

        data["timestamp"] = datetime.now().isoformat()

        return data

    @classmethod
    def generate_multiple_health_data(cls, count: int = 10) -> list[dict[str, Any]]:
        """Generate multiple health data"""
        return [cls.generate_single_health_data() for _ in range(count)]

    @classmethod
    def generate_health_data_with_trends(cls, days: int = 7) -> list[dict[str, Any]]:
        data_list = []
        base_date = datetime.now() - timedelta(days=days)

        for i in range(days):
            data = cls.generate_single_health_data()

            trend_factor = i / days  # 0 to 1
            data["stress_score"] = int(
                data["stress_score"] * (0.8 + 0.4 * trend_factor)
            )

            data["timestamp"] = (base_date + timedelta(days=i)).isoformat()

            data_list.append(data)

        return data_list

    @classmethod
    def generate_realistic_health_data(cls) -> dict[str, Any]:
        data = {}

        data["steps"] = random.randint(3000, 15000)
        data["distance_meters"] = int(data["steps"] * 0.7)  # Correlated with steps
        data["calories_burned"] = int(data["steps"] * 0.1 + random.randint(500, 1000))

        data["sleep_duration"] = round(random.uniform(6.0, 9.0), 1)
        data["sleep_quality"] = random.randint(60, 95)

        base_heart_rate = 60
        activity_factor = data["steps"] / 10000  # 0.3 đến 1.5
        stress_factor = random.randint(10, 50)
        data["heart_rate"] = int(
            base_heart_rate + activity_factor * 20 + stress_factor * 0.3
        )

        data["stress_score"] = random.randint(20, 80)

        base_systolic = 110
        base_diastolic = 70
        stress_effect = (data["stress_score"] - 50) * 0.5

        data["bp_systolic"] = int(
            base_systolic + stress_effect + random.randint(-10, 10)
        )
        data["bp_diastolic"] = int(
            base_diastolic + stress_effect * 0.6 + random.randint(-5, 5)
        )

        data["blood_glucose"] = int(
            90 + (data["steps"] / 1000) * 5 + random.randint(-20, 20)
        )

        data["blood_oxygen"] = random.randint(95, 100)

        data["blood_pressure"] = f"{data['bp_systolic']}/{data['bp_diastolic']}"

        data["timestamp"] = datetime.now().isoformat()

        return data


def generate_mock_health_data(
    data_type: str = "single",
) -> dict[Any, Any]:
    """

    Args:
        data_type: "single", "multiple", "trends", "realistic"

    Returns:
        dict or list containing health data
    """
    generator = HealthDataGenerator()

    if data_type == "single":
        return generator.generate_single_health_data()
    elif data_type == "multiple":
        return {i: d for i, d in enumerate(generator.generate_multiple_health_data(10))}
    elif data_type == "trends":
        return {
            i: d for i, d in enumerate(generator.generate_health_data_with_trends(7))
        }
    elif data_type == "realistic":
        return generator.generate_realistic_health_data()
    else:
        return generator.generate_single_health_data()


def test_generator():
    """Test function to test the generator"""
    print("=== Test Health Data Generator ===")

    print("\n1. Single Health Data:")
    single_data = generate_mock_health_data("single")
    print(json.dumps(single_data, indent=2))

    print("\n2. Realistic Health Data:")
    realistic_data = generate_mock_health_data("realistic")
    print(json.dumps(realistic_data, indent=2))

    print("\n3. Multiple Health Data (first 2):")
    multiple_data = generate_mock_health_data("multiple")
    for i, data in enumerate(multiple_data[:2]):
        print(f"Data {i + 1}: {data['steps']} steps, {data['heart_rate']} bpm")


if __name__ == "__main__":
    test_generator()
