import client from './client';

export const uploadResume = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await client.post('/resume/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const getResumeDetails = async (resumeId: number) => {
  const response = await client.get(`/resume/${resumeId}`);
  return response.data;
};
