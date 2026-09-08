<template>
  <div class="bg-white rounded-3xl border border-slate-200/70 shadow-xs overflow-hidden">
    <!-- Loading Indicator -->
    <div v-if="isLoading" class="py-20 text-center">
      <div class="inline-flex items-center justify-center p-3 rounded-2xl bg-teal-50 text-teal-600 mb-3">
        <svg class="animate-spin h-8 w-8" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      </div>
      <p class="text-sm font-semibold text-slate-600">Retrieving patient records from clinical database...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="errorMessage" class="py-16 text-center px-4">
      <div class="w-16 h-16 rounded-3xl bg-rose-50 border border-rose-100 flex items-center justify-center mx-auto text-rose-500 mb-4 shadow-inner">
        <svg class="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
      </div>
      <h3 class="text-lg font-bold text-slate-800">Failed to load consultation records</h3>
      <p class="text-sm text-slate-500 mt-1 max-w-md mx-auto leading-relaxed">
        {{ errorMessage }}
      </p>
      <div class="mt-6 flex items-center justify-center gap-3">
        <button
          type="button"
          @click="$emit('retry')"
          class="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-teal-600 text-white text-sm font-bold hover:bg-teal-700 shadow-md shadow-teal-500/20 transition cursor-pointer"
        >
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Retry Connection
        </button>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else-if="items.length === 0" class="py-20 text-center">
      <div class="w-16 h-16 rounded-3xl bg-slate-100 flex items-center justify-center mx-auto text-slate-400 mb-4 shadow-inner">
        <svg class="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.8" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
      </div>
      <h3 class="text-lg font-bold text-slate-800">No consultation records match</h3>
      <p class="text-sm text-slate-500 mt-1 max-w-sm mx-auto leading-relaxed">
        {{ hasActiveFilters ? 'No records correspond to the provided phone number or diagnosis code filter.' : 'There are currently no recorded patient visits in the EMR repository.' }}
      </p>
      <div class="mt-5" v-if="!hasActiveFilters">
        <NuxtLink
          to="/consultations/new"
          class="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-teal-600 text-white text-sm font-bold hover:bg-teal-700 shadow-md shadow-teal-500/20 transition"
        >
          + Create First Consultation
        </NuxtLink>
      </div>
    </div>

    <!-- Table View -->
    <div v-else class="overflow-x-auto">
      <table class="w-full text-left border-collapse text-sm">
        <thead>
          <tr class="border-b border-slate-200/80 bg-slate-50/75 text-xs font-bold text-slate-500 uppercase tracking-wider">
            <th class="py-4 px-6">Patient</th>
            <th class="py-4 px-4">Contact</th>
            <th class="py-4 px-4">Date of Birth</th>
            <th class="py-4 px-4">ICD-10 Diagnosis</th>
            <th class="py-4 px-6">Treatment Notes</th>
            <th class="py-4 px-6 text-right">Consultation Date</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-100">
          <tr
            v-for="item in items"
            :key="item.id"
            class="hover:bg-teal-50/30 transition-colors group"
          >
            <!-- Patient Info -->
            <td class="py-4 px-6 whitespace-nowrap">
              <div class="flex items-center gap-3">
                <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-teal-500 to-emerald-400 text-white font-bold flex items-center justify-center text-xs shadow-xs">
                  {{ getInitials(item.full_name) }}
                </div>
                <div>
                  <span class="font-bold text-slate-900 group-hover:text-teal-700 transition">{{ item.full_name }}</span>
                  <span class="text-[11px] text-slate-400 block">ID: #{{ item.patient_id }}</span>
                </div>
              </div>
            </td>

            <!-- Phone -->
            <td class="py-4 px-4 text-slate-700 whitespace-nowrap font-mono text-xs font-semibold">
              <span class="px-2.5 py-1 rounded-lg bg-slate-100 text-slate-800 border border-slate-200/60">
                +65 {{ item.phone }}
              </span>
            </td>

            <!-- DOB -->
            <td class="py-4 px-4 text-slate-600 whitespace-nowrap text-xs font-medium">
              {{ item.dob }}
            </td>

            <!-- Diagnosis -->
            <td class="py-4 px-4">
              <div class="flex flex-col items-start gap-1">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-lg text-xs font-mono font-bold bg-teal-50 text-teal-700 border border-teal-200">
                  {{ item.diagnosis_code }}
                </span>
                <span class="text-xs text-slate-600 font-medium line-clamp-1 max-w-[220px]" :title="item.diagnosis_desc">
                  {{ item.diagnosis_desc }}
                </span>
              </div>
            </td>

            <!-- Notes -->
            <td class="py-4 px-6 text-slate-700 max-w-xs">
              <p class="line-clamp-2 text-xs leading-relaxed bg-slate-50/70 p-2 rounded-xl border border-slate-100" :title="item.treatment_notes">
                {{ item.treatment_notes }}
              </p>
            </td>

            <!-- Created At -->
            <td class="py-4 px-6 text-right whitespace-nowrap">
              <span class="text-xs font-semibold text-slate-700 block">{{ formatDate(item.created_at) }}</span>
              <span class="text-[11px] text-slate-400 block">{{ formatTime(item.created_at) }}</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination Footer -->
    <div
      v-if="totalPages > 1"
      class="border-t border-slate-200/80 px-6 py-4 bg-slate-50/80 flex flex-col sm:flex-row items-center justify-between gap-4"
    >
      <div class="text-xs font-medium text-slate-500">
        Showing <span class="font-bold text-slate-800">{{ (page - 1) * pageSize + 1 }}</span> to
        <span class="font-bold text-slate-800">{{ Math.min(page * pageSize, total) }}</span> of
        <span class="font-bold text-slate-800">{{ total }}</span> records
      </div>

      <div class="flex items-center gap-2">
        <button
          :disabled="page <= 1"
          @click="$emit('page-change', page - 1)"
          class="px-3.5 py-1.5 rounded-xl border border-slate-200 bg-white text-xs font-bold text-slate-700 hover:bg-slate-50 shadow-2xs disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer"
        >
          &larr; Previous
        </button>
        
        <div class="flex items-center gap-1">
          <span class="px-3 py-1 rounded-xl bg-teal-600 text-white text-xs font-bold shadow-2xs">
            {{ page }}
          </span>
          <span class="text-xs text-slate-400 font-bold px-1">/ {{ totalPages }}</span>
        </div>

        <button
          :disabled="page >= totalPages"
          @click="$emit('page-change', page + 1)"
          class="px-3.5 py-1.5 rounded-xl border border-slate-200 bg-white text-xs font-bold text-slate-700 hover:bg-slate-50 shadow-2xs disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer"
        >
          Next &rarr;
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Consultation } from '~/types';

withDefaults(
  defineProps<{
    items: Consultation[];
    isLoading: boolean;
    hasActiveFilters: boolean;
    page: number;
    pageSize: number;
    total: number;
    totalPages: number;
    errorMessage?: string | null;
  }>(),
  {
    errorMessage: null,
  }
);

defineEmits<{
  (e: 'page-change', newPage: number): void;
  (e: 'retry'): void;
}>();

const getInitials = (name: string) => {
  if (!name) return 'PT';
  return name
    .split(' ')
    .map((n) => n[0])
    .slice(0, 2)
    .join('')
    .toUpperCase();
};

const formatDate = (isoString: string) => {
  if (!isoString) return '-';
  const date = new Date(isoString);
  return date.toLocaleDateString('en-GB', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  });
};

const formatTime = (isoString: string) => {
  if (!isoString) return '';
  const date = new Date(isoString);
  return date.toLocaleTimeString('en-GB', {
    hour: '2-digit',
    minute: '2-digit',
  });
};
</script>
