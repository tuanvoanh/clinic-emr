export interface ApiError {
  error_code?: string;
  message?: string;
  details?: any;
}

export const useApi = () => {
  const config = useRuntimeConfig();
  const token = useCookie<string | null>('clinic_auth_token');
  const baseURL = config.public.apiBaseUrl;

  const request = async <T>(
    endpoint: string,
    options: Parameters<typeof $fetch>[1] = {}
  ): Promise<T> => {
    const headers: Record<string, string> = {
      ...(options.headers as Record<string, string> || {}),
    };

    if (token.value) {
      headers.Authorization = `Bearer ${token.value}`;
    }

    try {
      const response = await $fetch<T>(`${baseURL}${endpoint}`, {
        ...options,
        headers,
      });
      return response;
    } catch (err: any) {
      // Handle 401 Unauthorized globally
      if (err.statusCode === 401 || err.status === 401) {
        token.value = null;
        if (process.client) {
          const router = useRouter();
          router.push('/login');
        }
      }
      throw err;
    }
  };

  return {
    request,
    get: <T>(endpoint: string, query?: Record<string, any>) =>
      request<T>(endpoint, { method: 'GET', query }),
    post: <T>(endpoint: string, body?: any, headers?: Record<string, string>) =>
      request<T>(endpoint, { method: 'POST', body, headers }),
    put: <T>(endpoint: string, body?: any) =>
      request<T>(endpoint, { method: 'PUT', body }),
    delete: <T>(endpoint: string) =>
      request<T>(endpoint, { method: 'DELETE' }),
  };
};
