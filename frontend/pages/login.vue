<template>
  <div class="min-h-[85vh] flex items-center justify-center p-4">
    <div class="w-full max-w-md">
      <!-- Outer Card -->
      <div class="bg-white rounded-3xl shadow-xl shadow-slate-200/70 border border-slate-100/80 p-8 sm:p-10 relative overflow-hidden">
        <!-- Subtle Top Glow -->
        <div class="absolute -top-24 -left-24 w-48 h-48 bg-teal-500/10 rounded-full blur-3xl pointer-events-none"></div>
        <div class="absolute -top-24 -right-24 w-48 h-48 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none"></div>

        <!-- Header -->
        <div class="text-center mb-6 relative">
          <div class="inline-flex w-16 h-16 rounded-2xl bg-gradient-to-tr from-teal-600 to-emerald-400 items-center justify-center text-white shadow-lg shadow-teal-500/30 mb-4 transform hover:rotate-3 transition duration-200">
            <svg class="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4.5v15m7.5-7.5h-15" />
            </svg>
          </div>
          <h1 class="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">Clinical Staff Login</h1>
          <p class="text-sm text-slate-500 mt-1 font-medium">Access patient records and electronic consultations</p>
        </div>

        <!-- Demo Account Banner Box -->
        <div class="mb-6 p-4 rounded-2xl bg-teal-50/90 border border-teal-200/80 text-xs text-teal-900 relative">
          <div class="flex items-center justify-between font-bold mb-2 text-teal-950">
            <span class="flex items-center gap-1.5 uppercase tracking-wider text-[11px]">
              <svg class="w-4 h-4 text-teal-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Demo Credentials
            </span>
            <button
              type="button"
              @click="fillDemoCredentials"
              class="px-2.5 py-1 rounded-lg bg-teal-600 hover:bg-teal-700 text-white font-bold transition shadow-xs cursor-pointer"
            >
              Fill into Form
            </button>
          </div>
          <div class="space-y-1 font-mono text-[12px] bg-white/70 p-2.5 rounded-xl border border-teal-100">
            <div class="flex items-center justify-between">
              <span class="text-slate-500 font-sans font-medium text-[11px]">Email:</span>
              <span class="font-bold text-slate-800">admin@clinic.com</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-slate-500 font-sans font-medium text-[11px]">Password:</span>
              <span class="font-bold text-slate-800">adminpassword</span>
            </div>
          </div>
        </div>

        <!-- Alert Error Message -->
        <div
          v-if="errorMessage"
          class="mb-6 p-4 rounded-2xl bg-rose-50/90 border border-rose-200/80 flex items-start gap-3 text-rose-700 text-sm animate-shake"
        >
          <svg class="w-5 h-5 flex-shrink-0 text-rose-500 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <div class="flex-1 font-medium leading-relaxed">{{ errorMessage }}</div>
        </div>

        <!-- Alert Setup Message -->
        <div
          v-if="setupMessage"
          class="mb-6 p-4 rounded-2xl bg-emerald-50/90 border border-emerald-200/80 flex items-start gap-3 text-emerald-800 text-sm"
        >
          <svg class="w-5 h-5 flex-shrink-0 text-emerald-600 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          <div class="flex-1 font-medium leading-relaxed">{{ setupMessage }}</div>
        </div>

        <!-- Form -->
        <form @submit.prevent="handleLogin" class="space-y-5 relative">
          <div>
            <label for="email" class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
              Staff Email Address
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207" />
                </svg>
              </div>
              <input
                id="email"
                v-model="email"
                type="email"
                required
                autocomplete="username"
                placeholder="doctor@clinic.com"
                class="w-full pl-10 pr-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-teal-500/20 focus:border-teal-500 outline-none transition duration-150 text-slate-800 placeholder-slate-400 text-sm bg-slate-50/60 focus:bg-white font-medium"
              />
            </div>
          </div>

          <div>
            <label for="password" class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
              Password
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <input
                id="password"
                v-model="password"
                type="password"
                required
                autocomplete="current-password"
                placeholder="••••••••"
                class="w-full pl-10 pr-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-teal-500/20 focus:border-teal-500 outline-none transition duration-150 text-slate-800 placeholder-slate-400 text-sm bg-slate-50/60 focus:bg-white font-medium"
              />
            </div>
          </div>

          <button
            type="submit"
            :disabled="isLoading"
            class="w-full mt-3 py-3.5 px-4 rounded-xl bg-gradient-to-r from-teal-600 to-emerald-600 hover:from-teal-700 hover:to-emerald-700 active:from-teal-800 active:to-emerald-800 text-white font-bold text-sm shadow-lg shadow-teal-600/25 transition-all duration-150 flex items-center justify-center gap-2 disabled:opacity-60 disabled:cursor-not-allowed cursor-pointer"
          >
            <svg
              v-if="isLoading"
              class="animate-spin h-4 w-4 text-white"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>{{ isLoading ? 'Verifying Credentials...' : 'Authenticate & Sign In' }}</span>
          </button>
        </form>

        <!-- One-click Demo Account Creation -->
        <div class="mt-8 pt-6 border-t border-slate-100 text-center">
          <p class="text-xs text-slate-500">
            Cannot sign in?
            <button
              type="button"
              @click="handleCreateDemoAccount"
              :disabled="isSettingUp"
              class="font-bold text-teal-600 hover:text-teal-700 hover:underline inline-flex items-center gap-1 cursor-pointer disabled:opacity-50"
            >
              <svg v-if="isSettingUp" class="animate-spin h-3 w-3 text-teal-600" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span>Click here to create demo account</span>
            </button>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const email = ref('admin@clinic.com');
const password = ref('adminpassword');
const isLoading = ref(false);
const isSettingUp = ref(false);
const errorMessage = ref('');
const setupMessage = ref('');

const { login } = useAuth();
const router = useRouter();
const config = useRuntimeConfig();

const fillDemoCredentials = () => {
  email.value = 'admin@clinic.com';
  password.value = 'adminpassword';
};

const handleLogin = async () => {
  errorMessage.value = '';
  setupMessage.value = '';
  isLoading.value = true;

  try {
    await login(email.value, password.value);
    router.push('/');
  } catch (err: any) {
    if (err.data?.message) {
      errorMessage.value = err.data.message;
    } else if (err.data?.detail) {
      errorMessage.value = typeof err.data.detail === 'string' 
        ? err.data.detail 
        : 'Invalid credentials or validation failed';
    } else {
      errorMessage.value = 'Failed to sign in. Please check if the demo account has been initialized.';
    }
  } finally {
    isLoading.value = false;
  }
};

const handleCreateDemoAccount = async () => {
  errorMessage.value = '';
  setupMessage.value = '';
  isSettingUp.value = true;

  try {
    const baseURL = config.public.apiBaseUrl;
    await $fetch(`${baseURL}/api/auth/setup`, {
      method: 'POST',
    });
    setupMessage.value = 'Demo account initialized successfully! You can now click "Sign In".';
    fillDemoCredentials();
  } catch (err: any) {
    if (err.data?.message?.includes('already been completed') || err.data?.message) {
      setupMessage.value = err.data.message || 'Demo account is already created. Please sign in directly.';
      fillDemoCredentials();
    } else {
      errorMessage.value = 'Could not create demo account. Backend server might not be running.';
    }
  } finally {
    isSettingUp.value = false;
  }
};
</script>
