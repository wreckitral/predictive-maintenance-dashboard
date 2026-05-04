import json
import os
import re
from groq import Groq

MODEL_NAME = "llama-3.3-70b-versatile"
NORMAL_RANGES = {
    "temperature": "15-75 °C",
    "vibration": "0-5 mm/s",
    "pressure": "0-10 bar",
    "humidity": "0-100 %",
    "rpm": "0-5000 rpm",
    "current": "0-100 A",
    "voltage": "0-480 V",
}


def analyze_machine(machine_summary):
    prompt = _build_prompt(machine_summary)
    response_text = _send_groq_prompt(prompt)
    return _parse_groq_response(response_text)


def _build_prompt(machine_summary):
    machine_name = machine_summary.get("machine_name", "Unknown machine")
    sensors = machine_summary.get("sensors", {})

    lines = [
        f"Machine name: {machine_name}",
        "Current sensor readings:",
    ]

    if not sensors:
        lines.append("No sensor readings were provided.")
    else:
        for sensor_type, sensor_data in sensors.items():
            value = sensor_data.get("value")
            unit = sensor_data.get("unit", "")
            is_anomaly = sensor_data.get("is_anomaly", False)
            normal_range = NORMAL_RANGES.get(sensor_type.lower(), "unknown")
            anomaly_text = "yes" if is_anomaly else "no"

            lines.append(
                f"- {sensor_type}: {value} {unit}. Normal range: {normal_range}. Anomalous: {anomaly_text}."
            )

    lines.extend([
        "\nPlease analyze the machine status and return JSON only with these exact fields:",
        "health_score — integer 0 to 100",
        "failure_probability — integer 0 to 100",
        "status — one of: \"healthy\", \"warning\", \"critical\"",
        "diagnosis — plain English explanation of what's wrong",
        "recommended_action — what the engineer should do right now",
        "estimated_time_to_failure — string like \"24-48 hours\" or \"No immediate risk\"",
        "Do not include any extra text or markdown. Return only a valid JSON object."
    ])

    return "\n".join(lines)


def _send_groq_prompt(prompt):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not set in the environment.")

    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": "You are a predictive maintenance AI for a cigarette factory. Return only valid JSON. No markdown, no extra text."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=400,
        temperature=0.2,
    )

    try:
        return response.choices[0].message.content
    except (AttributeError, IndexError) as exc:
        raise ValueError("Groq response did not contain a valid completion message.") from exc


def _parse_groq_response(response_text):
    json_text = _find_json_substring(response_text)
    if not json_text:
        raise ValueError("Unable to parse JSON from Groq response.")

    data = json.loads(json_text)
    result = {
        "health_score": int(data["health_score"]),
        "failure_probability": int(data["failure_probability"]),
        "status": str(data["status"]).lower(),
        "diagnosis": str(data["diagnosis"]).strip(),
        "recommended_action": str(data["recommended_action"]).strip(),
        "estimated_time_to_failure": str(data["estimated_time_to_failure"]).strip(),
    }

    if result["status"] not in {"healthy", "warning", "critical"}:
        raise ValueError("Groq response status must be one of: healthy, warning, critical.")

    for field in ["health_score", "failure_probability"]:
        if not 0 <= result[field] <= 100:
            raise ValueError(f"Groq response {field} must be between 0 and 100.")

    return result


def _find_json_substring(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else None
