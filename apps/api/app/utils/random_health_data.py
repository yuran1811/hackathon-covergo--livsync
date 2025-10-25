"""
Random Health Data Generator
Tạo dữ liệu sức khỏe ngẫu nhiên trong các ngưỡng cố định
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List

SPORT_OPTIONS = ("pickleball", "swim", "running")


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
    def generate_single_health_data(cls) -> Dict[str, Any]:
        """Generate a single health data"""
        data = {}
        
        for key, range_config in cls.HEALTH_RANGES.items():
            if key == "sleep_duration":
                data[key] = round(random.uniform(range_config["min"], range_config["max"]), 1)
            else:
                data[key] = random.randint(range_config["min"], range_config["max"])

        data["blood_pressure"] = f"{data['bp_systolic']}/{data['bp_diastolic']}"
        data["timestamp"] = datetime.now().isoformat()

        return data
    
    @classmethod
    def generate_multiple_health_data(cls, count: int = 10) -> List[Dict[str, Any]]:
        """Generate multiple health data"""
        return [cls.generate_single_health_data() for _ in range(count)]
    
    @classmethod
    def generate_health_data_with_trends(cls, days: int = 7) -> List[Dict[str, Any]]:
        data_list = []
        base_date = datetime.now() - timedelta(days=days)
        
        for i in range(days):
            data = cls.generate_single_health_data()
            
            trend_factor = i / days  # 0 to 1
            data["stress_score"] = int(data["stress_score"] * (0.8 + 0.4 * trend_factor))
            
            data["timestamp"] = (base_date + timedelta(days=i)).isoformat()
            
            data_list.append(data)
        
        return data_list
    
    @classmethod
    def generate_realistic_health_data(cls) -> Dict[str, Any]:
        data = {}
        
        data["steps"] = random.randint(3000, 15000)
        data["distance_meters"] = int(data["steps"] * 0.7)  # Correlated with steps
        data["calories_burned"] = int(data["steps"] * 0.1 + random.randint(500, 1000))
        
        data["sleep_duration"] = round(random.uniform(6.0, 9.0), 1)
        data["sleep_quality"] = random.randint(60, 95)
        
        base_heart_rate = 60
        activity_factor = data["steps"] / 10000  # 0.3 đến 1.5
        stress_factor = random.randint(10, 50)
        data["heart_rate"] = int(base_heart_rate + activity_factor * 20 + stress_factor * 0.3)
        
        data["stress_score"] = random.randint(20, 80)
        
        base_systolic = 110
        base_diastolic = 70
        stress_effect = (data["stress_score"] - 50) * 0.5
        
        data["bp_systolic"] = int(base_systolic + stress_effect + random.randint(-10, 10))
        data["bp_diastolic"] = int(base_diastolic + stress_effect * 0.6 + random.randint(-5, 5))
        
        data["blood_glucose"] = int(90 + (data["steps"] / 1000) * 5 + random.randint(-20, 20))
        
        data["blood_oxygen"] = random.randint(95, 100)

        data["blood_pressure"] = f"{data['bp_systolic']}/{data['bp_diastolic']}"
        data["timestamp"] = datetime.now().isoformat()
        data["weekly_workouts"] = _generate_weekly_workout_history()

        return data


def _generate_weekly_workout_history(days: int = 7) -> List[Dict[str, Any]]:
    today = datetime.now().date()
    workouts: List[Dict[str, Any]] = []
    calorie_burn_rate = {
        "pickleball": 9.0,
        "swim": 10.5,
        "running": 11.5,
    }

    for offset in range(days):
        day = today - timedelta(days=offset)
        sport = random.choice(SPORT_OPTIONS)
        duration = random.randint(30, 75)
        burn_rate = calorie_burn_rate[sport]
        calories = int(duration * burn_rate * random.uniform(0.85, 1.15))

        workouts.append(
            {
                "date": day.isoformat(),
                "sport": sport,
                "duration_minutes": duration,
                "calories_burned": calories,
            }
        )

    return list(reversed(workouts))


CACHE_FILE_PATH = Path(__file__).resolve().parent / "mock_health_data_cache.json"


def _load_cache() -> Dict[str, Any]:
    if not CACHE_FILE_PATH.exists():
        return {}

    try:
        with CACHE_FILE_PATH.open("r", encoding="utf-8") as cache_file:
            data = json.load(cache_file)
            if isinstance(data, dict):
                return data
    except (OSError, json.JSONDecodeError):
        return {}

    return {}


def _write_cache(cache: Dict[str, Any]) -> None:
    try:
        CACHE_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with CACHE_FILE_PATH.open("w", encoding="utf-8") as cache_file:
            json.dump(cache, cache_file)
    except OSError:
        # If persisting fails we still return in-memory data.
        pass


def _create_mock_health_data(data_type: str) -> Any:
    generator = HealthDataGenerator

    if data_type == "single":
        return generator.generate_single_health_data()
    if data_type == "multiple":
        return generator.generate_multiple_health_data(10)
    if data_type == "trends":
        return generator.generate_health_data_with_trends(7)
    if data_type == "realistic":
        return generator.generate_realistic_health_data()

    return generator.generate_single_health_data()


def get_persisted_mock_health_data(data_type: str = "realistic") -> Any:
    cache = _load_cache()
    cached_value = cache.get(data_type)

    if cached_value is not None:
        if data_type == "realistic" and isinstance(cached_value, dict) and "weekly_workouts" not in cached_value:
            data = _create_mock_health_data(data_type)
            cache[data_type] = data
            _write_cache(cache)
            return data
        return cached_value

    data = _create_mock_health_data(data_type)
    cache[data_type] = data
    _write_cache(cache)

    return data


def generate_mock_health_data(data_type: str = "single") -> Any:
    """
    
    Args:
        data_type: "single", "multiple", "trends", "realistic"
    
    Returns:
        Dict or List containing health data
    """
    return _create_mock_health_data(data_type)

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
        print(f"Data {i+1}: {data['steps']} steps, {data['heart_rate']} bpm")

if __name__ == "__main__":
    test_generator()
