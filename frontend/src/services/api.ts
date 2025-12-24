import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

export const api = axios.create({
  baseURL: API_URL,
});

export const uploadResume = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await api.post('/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  return response.data;
};

export const analyzeResume = async (resumeData: any, targetRole: string) => {
  const response = await api.post('/analyze', {
    resume_data: resumeData,
    target_role: targetRole
  });
  return response.data;
};

export const chatWithMentor = async (message: string, context?: string) => {
  const response = await api.post('/chat', {
    message,
    context
  });
  return response.data;
};
