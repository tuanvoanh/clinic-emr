export interface ApiError {
  error_code?: string;
  message?: string;
  details?: any;
}

export const useApi = () => {
  const config = useRuntimeConfig();
  const { token, logout } = useAuth();
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
        logout();
      }
      throw err;
    }
  };

  return {
    request,
    get: <T>(endpoint: string, query?: Record<string, any>, options?: Parameters<typeof $fetch>[1]) =>
      request<T>(endpoint, { method: 'GET', query, ...options }),
    post: <T>(endpoint: string, body?: any, headers?: Record<string, string>, options?: Parameters<typeof $fetch>[1]) =>
      request<T>(endpoint, { method: 'POST', body, headers, ...options }),
    put: <T>(endpoint: string, body?: any, options?: Parameters<typeof $fetch>[1]) =>
      request<T>(endpoint, { method: 'PUT', body, ...options }),
    delete: <T>(endpoint: string, options?: Parameters<typeof $fetch>[1]) =>
      request<T>(endpoint, { method: 'DELETE', ...options }),
  };
};
