import client from "./client";

export interface ResumeParsedData {
  full_name: string;
  email: string;
  phone?: string | null;
  current_role: string;
  experience_years: number;
  education_level: string;
  skills: string[];
  certifications: string[];
  overall_score: number;
  resume_upgrade_suggestions?: string[];
}

export interface ResumeUploadResponse {
  resume_id: number;
  user_id: number;
  file_name: string;
  parsed_json: ResumeParsedData;
  experience_yrs?: number | null;
  education_level?: string | null;
  current_role?: string | null;
  overall_score?: number | null;
  uploaded_at: string;
}

export const uploadResume = async (
  file: File,
): Promise<ResumeUploadResponse> => {
  const formData = new FormData();
  formData.append("file", file);

  const response = await client.post("/resume/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
  return response.data;
};

export const getResumeDetails = async (resumeId: number) => {
  const response = await client.get(`/resume/${resumeId}`);
  return response.data;
};

export const getUserResumes = async (
  userId: number,
): Promise<ResumeUploadResponse[]> => {
  const response = await client.get(`/resume/user/${userId}`);
  return response.data;
};
