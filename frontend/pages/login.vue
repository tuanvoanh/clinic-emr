<template>
  <div class="min-h-[85vh] flex items-center justify-center p-4">
    <div class="w-full max-w-md">
      <!-- Outer Card -->
      <div class="bg-white rounded-3xl shadow-xl shadow-slate-200/70 border border-slate-100/80 p-8 sm:p-10 relative overflow-hidden">
        <!-- Subtle Top Glow -->
        <div class="absolute -top-24 -left-24 w-48 h-48 bg-teal-500/10 rounded-full blur-3xl pointer-events-none"></div>
        <div class="absolute -top-24 -right-24 w-48 h-48 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none"></div>

        <!-- Header -->
        <div class="text-center mb-8 relative">
          <div class="inline-flex w-16 h-16 rounded-2xl bg-gradient-to-tr from-teal-600 to-emerald-400 items-center justify-center text-white shadow-lg shadow-teal-500/30 mb-4 transform hover:rotate-3 transition duration-200">
            <svg class="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4.5v15m7.5-7.5h-15" />
            </svg>
          </div>
          <h1 class="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">Clinical Staff Login</h1>
          <p class="text-sm text-slate-500 mt-1.5 font-medium">Access patient records and electronic consultations</p>
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

        <!-- Doctor Setup Helper Info -->
        <div class="mt-8 pt-6 border-t border-slate-100 text-center">
          <p class="text-xs text-slate-400 leading-relaxed">
            Need an initial superuser? Run backend <code class="bg-slate-100 px-1.5 py-0.5 rounded text-slate-600 font-mono text-[11px]">POST /api/auth/setup</code>.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const email = ref('');
const password = ref('');
const isLoading = ref(false);
const errorMessage = ref('');

const { login } = useAuth();
const router = useRouter();

const handleLogin = async () => {
  errorMessage.value = '';
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
      errorMessage.value = 'Failed to sign in. Please verify your credentials.';
    }
  } finally {
    isLoading.value = false;
  }
};
</script>
