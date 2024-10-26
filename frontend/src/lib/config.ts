export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
export const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL!;
export const SUPABASE_ANON_KEY = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;

// Validate environment variables
if (!SUPABASE_URL || !SUPABASE_ANON_KEY) {
  throw new Error('Missing Supabase environment variables');
}

// API endpoints
export const API_ENDPOINTS = {
  health: `${API_BASE_URL}/health`,
  automation: {
    startRecording: (routineId: string) => 
      `${API_BASE_URL}/api/automation/record/${routineId}/start`,
    stopRecording: (routineId: string) => 
      `${API_BASE_URL}/api/automation/record/${routineId}/stop`,
    startPlayback: (routineId: string) => 
      `${API_BASE_URL}/api/automation/play/${routineId}`,
    stopPlayback: (routineId: string) => 
      `${API_BASE_URL}/api/automation/play/${routineId}/stop`,
  }
};