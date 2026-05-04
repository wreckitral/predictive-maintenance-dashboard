import axios from 'axios';
import type { AiAnalysis, MachineSummary, SensorReading } from '../types';

const api = axios.create({
    baseURL: 'http://localhost:8000/',
    headers: {
        'Content-Type': 'application/json',
    },
});

async function getMachines() {
    try {
        const response = await api.get<MachineSummary[]>('/machines');

        return response.data;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            console.error('Axios error:', error.message);
        } else {
            console.error('Unexpected error:', error);
        }
    }
}

async function getReadings(machineId: string) {
   try {
    const response = await api.get<SensorReading[]>(`/readings/${machineId}`);

    return response.data;

   } catch (error) {
        if (axios.isAxiosError(error)) {
            console.error('Axios error:', error.message);
        } else {
            console.error('Unexpected error:', error);
        }
   } 
}

async function analyzeMachine(machineId: string) {
    try {
        const { data } = await api.post<AiAnalysis>(`/analyze/${machineId}`);

        return data;
    } catch (error) {
        if (axios.isAxiosError(error)) {
            console.error('Axios error:', error.message);
        } else {
            console.error('Unexpected error:', error);
        }
    }
}