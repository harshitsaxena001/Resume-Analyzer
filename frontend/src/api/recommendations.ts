import client from "./client";

export interface JobRecommendationResponse {
  resume_id: number;
  job_id: number;
  title: string;
  company_name?: string | null;
  location?: string | null;
  job_type?: string | null;
  score: number;
  matched_skills: string[];
  missing_skills: string[];
  match_reasons: string[];
}

export const getMyRecommendations = async (
  limit = 10,
): Promise<JobRecommendationResponse[]> => {
  const response = await client.get(`/recommendations/user/me?limit=${limit}`);
  return response.data;
};
