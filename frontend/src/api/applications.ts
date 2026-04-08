import client from "./client";

export interface ApplicationCreate {
  job_id: number;
  resume_id?: number;
  cover_letter?: string;
}

export interface ApplicationResponse {
  application_id: number;
  job_id: number;
  user_id: number;
  cover_letter?: string;
  status: string;
  applied_at: string;
}

export const applyToJob = async (
  data: ApplicationCreate,
): Promise<ApplicationResponse> => {
  const response = await client.post("/applications/apply", data);
  return response.data;
};
