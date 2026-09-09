export interface TokenResponse {
  access_token: string;
  token_type: string;
}

const TOKEN_KEY = 'clinic_auth_token';
const USER_EMAIL_KEY = 'clinic_user_email';

export const useAuth = () => {
  const token = useState<string | null>('auth_token', () => {
    if (process.client) {
      return localStorage.getItem(TOKEN_KEY);
    }
    return null;
  });

  const userEmail = useState<string | null>('auth_user_email', () => {
    if (process.client) {
      return localStorage.getItem(USER_EMAIL_KEY);
    }
    return null;
  });

  // Ensure client-side sync if initial state was undefined
  if (process.client) {
    if (token.value === null) {
      token.value = localStorage.getItem(TOKEN_KEY);
    }
    if (userEmail.value === null) {
      userEmail.value = localStorage.getItem(USER_EMAIL_KEY);
    }
  }

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
    if (process.client) {
      localStorage.setItem(TOKEN_KEY, response.access_token);
      localStorage.setItem(USER_EMAIL_KEY, username);
      // Clean up any legacy cookies if previously present
      const cookie = useCookie(TOKEN_KEY);
      cookie.value = null;
      const emailCookie = useCookie(USER_EMAIL_KEY);
      emailCookie.value = null;
    }
    return response;
  };

  const logout = () => {
    token.value = null;
    userEmail.value = null;
    if (process.client) {
      localStorage.removeItem(TOKEN_KEY);
      localStorage.removeItem(USER_EMAIL_KEY);
    }
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
