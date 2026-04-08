import client from "./client";

export interface JobCompany {
  company_id: number;
  name: string;
  website?: string | null;
}

export interface JobSkill {
  id: number;
  skill: {
    skill_id: number;
    name: string;
  };
  is_required: boolean;
}

export interface JobResponse {
  job_id: number;
  title: string;
  description: string;
  location: string;
  job_type: string;
  experience_min: number;
  experience_max: number;
  salary_min: number;
  salary_max: number;
  posted_at: string;
  company: JobCompany;
  job_skills: JobSkill[];
}

export const getJobs = async (
  skip = 0,
  limit = 100,
): Promise<JobResponse[]> => {
  const response = await client.get(`/jobs/?skip=${skip}&limit=${limit}`);
  return response.data;
};

export const searchJobs = async (query: string): Promise<JobResponse[]> => {
  const response = await client.get(`/jobs/search?q=${query}`);
  return response.data;
};

export const getJobById = async (id: number): Promise<JobResponse> => {
  const response = await client.get(`/jobs/${id}`);
  return response.data;
};
