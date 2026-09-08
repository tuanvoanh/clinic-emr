<template>
  <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
    <!-- Total Consultations -->
    <div class="bg-white p-5 rounded-2xl border border-slate-200/70 shadow-xs flex items-center gap-4">
      <div class="w-12 h-12 rounded-xl bg-teal-50 border border-teal-100 flex items-center justify-center text-teal-600">
        <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
      </div>
      <div>
        <p class="text-xs font-bold uppercase tracking-wider text-slate-400">Total Consultations</p>
        <p class="text-2xl font-extrabold text-slate-900 mt-0.5">{{ total }}</p>
      </div>
    </div>

    <!-- Current Page -->
    <div class="bg-white p-5 rounded-2xl border border-slate-200/70 shadow-xs flex items-center gap-4">
      <div class="w-12 h-12 rounded-xl bg-sky-50 border border-sky-100 flex items-center justify-center text-sky-600">
        <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
        </svg>
      </div>
      <div>
        <p class="text-xs font-bold uppercase tracking-wider text-slate-400">Current Page</p>
        <p class="text-2xl font-extrabold text-slate-900 mt-0.5">{{ page }} <span class="text-sm font-medium text-slate-400">/ {{ totalPages || 1 }}</span></p>
      </div>
    </div>

    <!-- Status -->
    <div class="bg-white p-5 rounded-2xl border border-slate-200/70 shadow-xs flex items-center gap-4">
      <div
        :class="[
          'w-12 h-12 rounded-xl border flex items-center justify-center transition-colors',
          syncStatus === 'error'
            ? 'bg-rose-50 border-rose-100 text-rose-600'
            : syncStatus === 'syncing'
            ? 'bg-sky-50 border-sky-100 text-sky-600'
            : 'bg-emerald-50 border-emerald-100 text-emerald-600',
        ]"
      >
        <svg v-if="syncStatus === 'error'" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <svg v-else-if="syncStatus === 'syncing'" class="w-6 h-6 animate-spin" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <svg v-else class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
      <div>
        <p class="text-xs font-bold uppercase tracking-wider text-slate-400">Database Status</p>
        <p
          :class="[
            'text-sm font-bold flex items-center gap-1.5 mt-1 transition-colors',
            syncStatus === 'error'
              ? 'text-rose-600'
              : syncStatus === 'syncing'
              ? 'text-sky-600'
              : 'text-emerald-600',
          ]"
        >
          <span
            :class="[
              'w-2 h-2 rounded-full',
              syncStatus === 'error'
                ? 'bg-rose-500'
                : syncStatus === 'syncing'
                ? 'bg-sky-500 animate-ping'
                : 'bg-emerald-500 animate-pulse',
            ]"
          ></span>
          {{ syncStatus === 'error' ? 'Connection Error' : syncStatus === 'syncing' ? 'Syncing...' : 'Live Synced' }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    total: number;
    page: number;
    totalPages: number;
    syncStatus?: 'synced' | 'syncing' | 'error';
  }>(),
  {
    syncStatus: 'synced',
  }
);
</script>
