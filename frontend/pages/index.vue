<template>
  <div class="space-y-6">
    <!-- Page Header & Action -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 bg-white p-6 rounded-3xl border border-slate-200/70 shadow-xs">
      <div>
        <div class="flex items-center gap-2">
          <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold bg-teal-50 text-teal-700 border border-teal-200/60">
            EMR System
          </span>
          <span class="text-xs text-slate-400">•</span>
          <span class="text-xs font-semibold text-slate-500">Live Database</span>
        </div>
        <h1 class="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight mt-1">Consultation History</h1>
        <p class="text-sm text-slate-500 mt-0.5">Review, filter, and inspect past patient diagnoses and clinical treatments</p>
      </div>

      <NuxtLink
        to="/consultations/new"
        class="inline-flex items-center justify-center gap-2 px-5 py-3 rounded-2xl bg-gradient-to-r from-teal-600 to-emerald-600 hover:from-teal-700 hover:to-emerald-700 text-white font-bold text-sm shadow-md shadow-teal-500/25 hover:shadow-lg hover:shadow-teal-500/30 transition-all duration-150 transform hover:-translate-y-0.5"
      >
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4" />
        </svg>
        <span>+ Record New Consultation</span>
      </NuxtLink>
    </div>

    <!-- Quick Stats Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <div class="bg-white p-5 rounded-2xl border border-slate-200/70 shadow-xs flex items-center gap-4">
        <div class="w-12 h-12 rounded-xl bg-teal-50 border border-teal-100 flex items-center justify-center text-teal-600">
          <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
        </div>
        <div>
          <p class="text-xs font-bold uppercase tracking-wider text-slate-400">Total Consultations</p>
          <p class="text-2xl font-extrabold text-slate-900 mt-0.5">{{ totalItems }}</p>
        </div>
      </div>

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

      <div class="bg-white p-5 rounded-2xl border border-slate-200/70 shadow-xs flex items-center gap-4">
        <div class="w-12 h-12 rounded-xl bg-emerald-50 border border-emerald-100 flex items-center justify-center text-emerald-600">
          <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <div>
          <p class="text-xs font-bold uppercase tracking-wider text-slate-400">System Status</p>
          <p class="text-sm font-bold text-emerald-600 flex items-center gap-1.5 mt-1">
            <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            Online & Synced
          </p>
        </div>
      </div>
    </div>

    <!-- Search & Filter Bar -->
    <div class="bg-white rounded-3xl border border-slate-200/70 p-6 shadow-xs">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-sm font-bold uppercase tracking-wider text-slate-700 flex items-center gap-2">
          <svg class="w-4 h-4 text-teal-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
          </svg>
          Filter Consultations
        </h2>
        <span v-if="hasActiveFilters" class="text-xs font-bold text-teal-600 bg-teal-50 px-2.5 py-1 rounded-full border border-teal-200">
          Filter Active
        </span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-12 gap-4">
        <!-- Search by Phone -->
        <div class="sm:col-span-5">
          <label class="block text-xs font-bold text-slate-600 mb-1.5">
            Patient Mobile Number
          </label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
              </svg>
            </div>
            <input
              v-model="filters.phone"
              type="text"
              placeholder="e.g. 81234567 or 91234567"
              @keyup.enter="handleSearch"
              class="w-full pl-10 pr-4 py-2.5 text-sm rounded-xl border border-slate-200 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 outline-none transition bg-slate-50/50 focus:bg-white"
            />
          </div>
        </div>

        <!-- Filter by Diagnosis Code -->
        <div class="sm:col-span-5">
          <label class="block text-xs font-bold text-slate-600 mb-1.5">
            ICD-10 Disease Code
          </label>
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
              </svg>
            </div>
            <input
              v-model="filters.diagnosis_code"
              type="text"
              placeholder="e.g. A00.0, R51.9"
              @keyup.enter="handleSearch"
              class="w-full pl-10 pr-4 py-2.5 text-sm rounded-xl border border-slate-200 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 outline-none transition bg-slate-50/50 focus:bg-white"
            />
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="sm:col-span-2 flex items-end gap-2">
          <button
            @click="handleSearch"
            class="flex-1 py-2.5 px-4 bg-slate-900 hover:bg-slate-800 text-white text-sm font-bold rounded-xl transition shadow-xs cursor-pointer"
          >
            Filter
          </button>
          <button
            @click="handleReset"
            class="py-2.5 px-3 border border-slate-200 hover:bg-slate-100 text-slate-600 text-sm font-semibold rounded-xl transition cursor-pointer"
            title="Reset filters"
          >
            Reset
          </button>
        </div>
      </div>
    </div>

    <!-- Data Table Container -->
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

      <!-- Empty State -->
      <div v-else-if="consultations.length === 0" class="py-20 text-center">
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
              v-for="item in consultations"
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
          <span class="font-bold text-slate-800">{{ Math.min(page * pageSize, totalItems) }}</span> of
          <span class="font-bold text-slate-800">{{ totalItems }}</span> records
        </div>

        <div class="flex items-center gap-2">
          <button
            :disabled="page <= 1"
            @click="changePage(page - 1)"
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
            @click="changePage(page + 1)"
            class="px-3.5 py-1.5 rounded-xl border border-slate-200 bg-white text-xs font-bold text-slate-700 hover:bg-slate-50 shadow-2xs disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer"
          >
            Next &rarr;
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Consultation {
  id: number;
  patient_id: number;
  full_name: string;
  dob: string;
  phone: string;
  diagnosis_code: string;
  diagnosis_desc: string;
  treatment_notes: string;
  created_at: string;
}

interface PaginatedResponse {
  items: Consultation[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

const api = useApi();

const consultations = ref<Consultation[]>([]);
const totalItems = ref(0);
const totalPages = ref(0);
const page = ref(1);
const pageSize = ref(10);
const isLoading = ref(false);

const filters = reactive({
  phone: '',
  diagnosis_code: '',
});

const hasActiveFilters = computed(() => !!filters.phone.trim() || !!filters.diagnosis_code.trim());

const fetchConsultations = async () => {
  isLoading.value = true;
  try {
    const query: Record<string, any> = {
      page: page.value,
      page_size: pageSize.value,
    };

    if (filters.phone.trim()) {
      query.phone = filters.phone.trim();
    }
    if (filters.diagnosis_code.trim()) {
      query.diagnosis_code = filters.diagnosis_code.trim();
    }

    const res = await api.get<PaginatedResponse>('/api/consultation/', query);
    consultations.value = res.items || [];
    totalItems.value = res.total;
    totalPages.value = res.total_pages;
  } catch (err) {
    console.error('Failed to load consultations', err);
  } finally {
    isLoading.value = false;
  }
};

const handleSearch = () => {
  page.value = 1;
  fetchConsultations();
};

const handleReset = () => {
  filters.phone = '';
  filters.diagnosis_code = '';
  page.value = 1;
  fetchConsultations();
};

const changePage = (newPage: number) => {
  if (newPage >= 1 && newPage <= totalPages.value) {
    page.value = newPage;
    fetchConsultations();
  }
};

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

onMounted(() => {
  fetchConsultations();
});
</script>
