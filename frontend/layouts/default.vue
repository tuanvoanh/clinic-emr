<template>
  <div class="min-h-screen bg-slate-50/80 flex flex-col selection:bg-teal-500 selection:text-white font-sans">
    <!-- Top Professional Medical Navbar -->
    <header v-if="isAuthenticated" class="sticky top-0 z-40 bg-white/90 backdrop-blur-md border-b border-slate-200/80 shadow-xs">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">

          <!-- Logo & Brand identity -->
          <div class="flex items-center gap-8">
            <NuxtLink to="/" class="flex items-center gap-3 group">
              <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-teal-600 via-teal-500 to-emerald-400 flex items-center justify-center text-white shadow-md shadow-teal-500/25 group-hover:scale-105 transition-all duration-200">
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4.5v15m7.5-7.5h-15" />
                </svg>
              </div>
              <div>
                <div class="flex items-center gap-1.5 leading-none">
                  <span class="font-extrabold text-xl tracking-tight text-slate-900">Clinic</span>
                  <span class="font-extrabold text-xl tracking-tight bg-gradient-to-r from-teal-600 to-emerald-500 bg-clip-text text-transparent">EMR</span>
                </div>
                <span class="text-[10px] font-semibold text-slate-400 uppercase tracking-widest block mt-0.5">Clinical Portal</span>
              </div>
            </NuxtLink>

            <!-- Navigation Links -->
            <nav class="hidden md:flex items-center space-x-1.5">
              <NuxtLink
                to="/"
                class="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-medium transition-all duration-150"
                :class="$route.path === '/' ? 'bg-teal-50/80 text-teal-700 font-semibold shadow-xs' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100/80'"
              >
                <svg class="w-4 h-4 opacity-75" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <span>Consultations</span>
              </NuxtLink>

              <NuxtLink
                to="/consultations/new"
                class="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-medium transition-all duration-150"
                :class="$route.path === '/consultations/new' ? 'bg-teal-50/80 text-teal-700 font-semibold shadow-xs' : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100/80'"
              >
                <svg class="w-4 h-4 opacity-75" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                <span>New Consultation</span>
              </NuxtLink>
            </nav>
          </div>

          <!-- User controls & status -->
          <div class="flex items-center gap-4">
            <div class="hidden sm:flex items-center gap-3 py-1.5 pl-3 pr-4 rounded-full bg-slate-100/80 border border-slate-200 text-xs">
              <span class="relative flex h-2.5 w-2.5">
                <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
              </span>
              <span class="font-medium text-slate-700 truncate max-w-[180px]">{{ userEmail || 'Doctor' }}</span>
            </div>

            <button
              @click="logout"
              class="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl text-xs font-semibold text-slate-600 hover:text-rose-600 hover:bg-rose-50 border border-slate-200/80 hover:border-rose-200 transition-all duration-150 cursor-pointer"
            >
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              <span>Sign Out</span>
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Workspace Container -->
    <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <slot />
    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-slate-200/60 py-5 text-center text-xs text-slate-400">
      <div class="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
        <p>&copy; {{ new Date().getFullYear() }} Clinic EMR Healthcare Systems. High-conformance Electronic Health Records.</p>
        <p class="text-slate-400 font-mono text-[11px]">HIPAA & ICD-10 Compliant Interface</p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
const { isAuthenticated, userEmail, logout } = useAuth();
</script>
