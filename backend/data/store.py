from datetime import datetime

store = []

def append_reading(reading):
    store.append(reading)

def get_all_reading():
    return store

def get_latest_by_machine():
    machines = {}
    
    for reading in store:
        machine_id = reading["machine_id"]
        machine_name = reading["machine_name"]
        sensor_type = reading["sensor_type"]
        
        # initialize machine entry if not present
        if machine_id not in machines:
            machines[machine_id] = {
                "machine_id": machine_id,
                "machine_name": machine_name,
                "sensors": {}
            }
        
        # initialize sensor entry if not present
        if sensor_type not in machines[machine_id]["sensors"]:
            machines[machine_id]["sensors"][sensor_type] = reading
        else:
            # compare timestamps and keep the most recent
            current_timestamp = machines[machine_id]["sensors"][sensor_type]["timestamp"]
            new_timestamp = reading["timestamp"]
            
            # parse ISO format timestamps for comparison
            try:
                current_dt = datetime.fromisoformat(current_timestamp)
                new_dt = datetime.fromisoformat(new_timestamp)
                if new_dt > current_dt:
                    machines[machine_id]["sensors"][sensor_type] = reading
            except (ValueError, TypeError):
                machines[machine_id]["sensors"][sensor_type] = reading
    
    result = []
    for machine in machines.values():
        sensors_summary = {}
        for sensor_type, reading in machine["sensors"].items():
            sensors_summary[sensor_type] = {
                "value": reading["value"],
                "unit": reading["unit"],
                "is_anomaly": reading["is_anomaly"],
                "timestamp": reading["timestamp"]
            }
        result.append({
            "machine_id": machine["machine_id"],
            "machine_name": machine["machine_name"],
            "sensors": sensors_summary
        })
    
    return result
