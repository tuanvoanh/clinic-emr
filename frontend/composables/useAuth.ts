export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export const useAuth = () => {
  const token = useCookie<string | null>('clinic_auth_token', {
    maxAge: 60 * 60 * 24 * 7, // 7 days
    sameSite: 'lax',
    path: '/',
  });

  const userEmail = useCookie<string | null>('clinic_user_email', {
    maxAge: 60 * 60 * 24 * 7,
    sameSite: 'lax',
    path: '/',
  });

  const isAuthenticated = computed(() => !!token.value);

  const login = async (username: string, password: string) => {
    const config = useRuntimeConfig();
    const baseURL = config.public.apiBaseUrl;

    // FastAPI OAuth2PasswordRequestForm expects x-www-form-urlencoded format
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    const response = await $fetch<TokenResponse>(`${baseURL}/api/auth/login/access-token`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData.toString(),
    });

    token.value = response.access_token;
    userEmail.value = username;
    return response;
  };

  const logout = () => {
    token.value = null;
    userEmail.value = null;
    const router = useRouter();
    router.push('/login');
  };

  return {
    token,
    userEmail,
    isAuthenticated,
    login,
    logout,
  };
};
