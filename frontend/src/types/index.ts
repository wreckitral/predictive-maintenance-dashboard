export interface SensorReading {
  machine_id: string;
  machine_name: string;
  sensor_type: string;
  value: number;
  unit: string;
  timestamp: string;
  is_anomaly: boolean;
}

export interface SensorLatest {
  value: number;
  unit: string;
  is_anomaly: boolean;
  timestamp: string;
}

export interface MachineSummary {
  machine_id: string;
  machine_name: string;
  sensors: Record<string, SensorLatest>;
}

export interface AiAnalysis {
  health_score: number;
  failure_probability: number;
  status: 'healthy' | 'warning' | 'critical';
  diagnosis: string;
  recommended_action: string;
  estimated_time_to_failure: string;
}