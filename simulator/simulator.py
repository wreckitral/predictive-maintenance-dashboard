import random
import datetime
import time
import requests

machine_1 = {
    "machine_id": "machine_01",
    "machine_name": "Cutting Machine",
    "sensors": {
        "temperature": {
            "normal_range": [30, 50],
            "threshold": [70],
            "unit": "C",
        },
        "vibration": {
            "normal_range": [0.5, 2.0],
            "threshold": [4.5],
            "unit": "mm/s",
        },
        "rpm": {
            "normal_range": [2800, 3200],
            "threshold": [2200, 3800],
            "unit": "RPM",
        },
        "pressure": {
            "normal_range": [1.0, 2.0],
            "threshold": [3.5],
            "unit": "bar",
        },
    }
}

machine_2 = {
    "machine_id": "machine_02",
    "machine_name": "Drying Oven",
    "sensors": {
        "temperature": {
            "normal_range": [60, 80],
            "threshold": [100],
            "unit": "C",
        },
        "vibration": {
            "normal_range": [0.1, 0.5],
            "threshold": [1.5],
            "unit": "mm/s",
        },
        "rpm": {
            "normal_range": [200, 400],
            "threshold": [150, 500],
            "unit": "RPM",
        },
        "pressure": {
            "normal_range": [0.5, 1.5],
            "threshold": [2.5],
            "unit": "bar",
        },
    }
}

machine_3 = {
    "machine_id": "machine_03",
    "machine_name": "Packaging Line",
    "sensors": {
        "temperature": {
            "normal_range": [40, 60],
            "threshold": [80],
            "unit": "C",
        },
        "vibration": {
            "normal_range": [0.3, 1.5],
            "threshold": [3.0],
            "unit": "mm/s",
        },
        "rpm": {
            "normal_range": [1500, 1800],
            "threshold": [1200, 2100],
            "unit": "RPM",
        },
        "pressure": {
            "normal_range": [2.0, 3.0],
            "threshold": [4.5],
            "unit": "bar",
        },
    }
}

machine_4 = {
    "machine_id": "machine_04",
    "machine_name": "Conveyor Belt",
    "sensors": {
        "temperature": {
            "normal_range": [25, 45],
            "threshold": [65],
            "unit": "C",
        },
        "vibration": {
            "normal_range": [0.2, 1.0],
            "threshold": [3.5],
            "unit": "mm/s",
        },
        "rpm": {
            "normal_range": [800, 1200],
            "threshold": [600, 1500],
            "unit": "RPM",
        },
        "pressure": {
            "normal_range": [0.8, 1.8],
            "threshold": [3.0],
            "unit": "bar",
        },
    }
}

machine_5 = {
    "machine_id": "machine_05",
    "machine_name": "Air Compressor",
    "sensors": {
        "temperature": {
            "normal_range": [70, 90],
            "threshold": [115],
            "unit": "C",
        },
        "vibration": {
            "normal_range": [1.0, 3.0],
            "threshold": [5.0],
            "unit": "mm/s",
        },
        "rpm": {
            "normal_range": [1400, 1600],
            "threshold": [1100, 1900],
            "unit": "RPM",
        },
        "pressure": {
            "normal_range": [6.0, 8.0],
            "threshold": [4.0, 10.0],
            "unit": "bar",
        },
    }
}

def generate_value(machine_config, sensor_type, drift_state):
    sensor = machine_config["sensors"].get(sensor_type)
    if sensor is None:
        raise KeyError(f"Sensor '{sensor_type}' not found in machine config")

    normal_low, normal_high = sensor["normal_range"]
    value = random.uniform(normal_low, normal_high)
    thresholds = sensor.get("threshold", [])

    drift = str(drift_state).lower() if drift_state is not None else "normal"
    nudge_strength = random.uniform(0.25, 0.6)

    if drift in {"high", "drift_high", "anomaly_high", "anomaly"}:
        if len(thresholds) == 1:
            target = thresholds[0]
        elif len(thresholds) == 2:
            target = thresholds[1]
        else:
            return value

        if target > normal_high:
            value += (target - value) * nudge_strength
        elif target < normal_low:
            value -= (value - target) * nudge_strength

    elif drift in {"low", "drift_low", "anomaly_low"}:
        if len(thresholds) == 1:
            target = thresholds[0]
        elif len(thresholds) == 2:
            target = thresholds[0]
        else:
            return value

        if target < normal_low:
            value -= (value - target) * nudge_strength
        elif target > normal_high:
            value += (target - value) * nudge_strength

    return value

def anomaly_checker(value, machine_config, sensor_type):
    sensor = machine_config["sensors"].get(sensor_type)
    if sensor is None:
        raise KeyError(f"Sensor '{sensor_type}' not found in machine config")

    normal_low, normal_high = sensor["normal_range"]
    thresholds = sensor.get("threshold", [])

    if value < normal_low:
        return "low"
    elif value > normal_high:
        return "high"
    elif len(thresholds) == 1:
        if value < thresholds[0]:
            return "drift_low"
        elif value > thresholds[0]:
            return "drift_high"
    elif len(thresholds) == 2:
        if value < thresholds[0]:
            return "drift_low"
        elif value > thresholds[1]:
            return "drift_high"
        
    return None

def build_payload(machine_id, machine_name, sensor_type, value, unit, is_anomaly):
    return {
        "machine_id": machine_id,
        "machine_name": machine_name,
        "sensor_type": sensor_type,
        "value": value,
        "unit": unit,
        "timestamp": datetime.datetime.now().isoformat(),
        "is_anomaly": is_anomaly,
    }

def update_drift(drift_state, machine_id):
    drift_states = [None, "high", "low", "drift_high", "drift_low", "anomaly_high", "anomaly_low"]
    if drift_state not in drift_states:
        raise ValueError(f"Invalid drift state: {drift_state}")

    if drift_state is None:
        new_state = random.choices(
            [None, "high", "low"],
            weights=[0.7, 0.15, 0.15],
            k=1
        )[0]
    elif drift_state in {"high", "low"}:
        new_state = random.choices(
            [drift_state, None],
            weights=[0.5, 0.5],
            k=1
        )[0]
    elif drift_state in {"drift_high", "drift_low"}:
        new_state = random.choices(
            [drift_state, None],
            weights=[0.6, 0.4],
            k=1
        )[0]
    elif drift_state in {"anomaly_high", "anomaly_low"}:
        new_state = random.choices(
            [drift_state, None],
            weights=[0.8, 0.2],
            k=1
        )[0]

    return new_state

def run_simulator():
    machines = [machine_1, machine_2, machine_3, machine_4, machine_5]

    drift_states = {
        machine["machine_id"]: {sensor_type: None for sensor_type in machine["sensors"].keys()}
        for machine in machines
    }

    while True:
        for machine in machines:
            machine_id = machine["machine_id"]
            machine_name = machine["machine_name"]

            for sensor_type in machine["sensors"].keys():
                drift_state = drift_states[machine_id][sensor_type]
                value = generate_value(machine, sensor_type, drift_state)
                unit = machine["sensors"][sensor_type]["unit"]
                is_anomaly = anomaly_checker(value, machine, sensor_type) is not None
                payload = build_payload(machine_id, machine_name, sensor_type, value, unit, is_anomaly)

                print(payload)
                requests.post("http://localhost:8000/readings", json=payload)

                drift_states[machine_id][sensor_type] = update_drift(drift_state, machine_id)

        time.sleep(3)

def main():
    run_simulator()

if __name__ == "__main__":
    main()