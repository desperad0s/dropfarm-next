// Core types for MVP
interface Routine {
    id: string;
    name: string;
    steps: AutomationStep[];
    status: 'idle' | 'recording' | 'playing' | 'completed';
    lastError?: string;
}

interface AutomationStep {
    type: 'click';
    x: number;
    y: number;
    time: number;  // timestamp relative to start
}

interface Schedule {
    id: string;
    name: string;
    routines: {
        routineId: string;
        intervalMinutes: number;
        enabled: boolean;
    }[];
}