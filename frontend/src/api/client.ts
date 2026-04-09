import axios from "axios";

const configuredApiUrl = import.meta.env.VITE_API_URL?.trim();
const inferredApiUrl = `${window.location.protocol}//${window.location.hostname}:8000`;

const isLocalHostName = (host: string) =>
  host === "localhost" || host === "127.0.0.1";

const shouldUseConfiguredUrl = (() => {
  if (!configuredApiUrl) return false;

  try {
    const configuredHost = new URL(configuredApiUrl).hostname;
    const currentHost = window.location.hostname;

    if (!isLocalHostName(currentHost) && isLocalHostName(configuredHost)) {
      return false;
    }

    return true;
  } catch {
    return false;
  }
})();

const API_BASE_URL = shouldUseConfiguredUrl ? configuredApiUrl : inferredApiUrl;

const client = axios.create({
  baseURL: API_BASE_URL,
});

client.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default client;
