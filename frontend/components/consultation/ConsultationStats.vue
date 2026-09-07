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
      <div class="w-12 h-12 rounded-xl bg-emerald-50 border border-emerald-100 flex items-center justify-center text-emerald-600">
        <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
      <div>
        <p class="text-xs font-bold uppercase tracking-wider text-slate-400">Database Status</p>
        <p class="text-sm font-bold text-emerald-600 flex items-center gap-1.5 mt-1">
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          Live Synced
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  total: number;
  page: number;
  totalPages: number;
}>();
</script>
