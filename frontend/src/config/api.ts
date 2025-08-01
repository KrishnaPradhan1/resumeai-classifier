// API Configuration
export const API_CONFIG = {
  // Railway backend URL - update this with your actual Railway URL
  BASE_URL: process.env.REACT_APP_API_URL || 'https://your-railway-app-name.railway.app',
  
  // API endpoints
  ENDPOINTS: {
    // Auth endpoints
    LOGIN: '/api/v1/auth/login',
    REGISTER: '/api/v1/auth/register',
    REFRESH: '/api/v1/auth/refresh',
    LOGOUT: '/api/v1/auth/logout',
    ME: '/api/v1/auth/me',
    
    // Resume endpoints
    RESUMES: '/api/v1/resumes',
    UPLOAD_RESUME: '/api/v1/resumes/upload',
    
    // Job endpoints
    JOBS: '/api/v1/jobs',
    
    // Match endpoints
    MATCHES: '/api/v1/matches',
    
    // User endpoints
    USER_PROFILE: '/api/v1/users/profile',
  },
  
  // Request timeout
  TIMEOUT: 30000,
  
  // Retry configuration
  RETRY_ATTEMPTS: 3,
  RETRY_DELAY: 1000,
};

// Helper function to get full API URL
export const getApiUrl = (endpoint: string): string => {
  return `${API_CONFIG.BASE_URL}${endpoint}`;
};

// API response types
export interface ApiResponse<T = any> {
  data?: T;
  message?: string;
  error?: string;
  status: number;
}

// Auth types
export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  full_name: string;
  company?: string;
  role?: string;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user_id: string;
  email: string;
  full_name: string;
}

// User types
export interface User {
  id: string;
  email: string;
  full_name: string;
  company?: string;
  role: string;
  phone?: string;
  location?: string;
  bio?: string;
  is_active: boolean;
  is_verified: boolean;
  subscription_plan: string;
  monthly_uploads: string;
  current_month_uploads: string;
  created_at: string;
  last_login_at?: string;
}

// Resume types
export interface Resume {
  id: string;
  original_filename: string;
  candidate_name?: string;
  candidate_email?: string;
  candidate_phone?: string;
  candidate_location?: string;
  summary?: string;
  skills?: string[];
  experience_years?: number;
  education?: any[];
  work_experience?: any[];
  certifications?: any[];
  status: string;
  confidence_score?: number;
  created_at: string;
}

// Job types
export interface Job {
  id: string;
  title: string;
  company: string;
  description: string;
  requirements: string[];
  location?: string;
  salary_range?: string;
  job_type: string;
  experience_level?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

// Match types
export interface Match {
  id: string;
  resume_id: string;
  job_id: string;
  overall_score: number;
  skills_score?: number;
  experience_score?: number;
  education_score?: number;
  culture_score?: number;
  skill_matches?: string[];
  missing_skills?: string[];
  experience_gap?: number;
  match_explanation?: string;
  strengths?: string[];
  weaknesses?: string[];
  recommendations?: string[];
  bias_score?: number;
  fairness_adjustment?: number;
  created_at: string;
} 