<template>
  <div class="space-y-6">
    <!-- Quick Stats & Actions Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
      <div class="flex items-center gap-3">
        <h1 class="text-xl sm:text-2xl font-extrabold text-slate-900 tracking-tight">Patient Consultations</h1>
        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold bg-teal-50 text-teal-700 border border-teal-200/60">
          {{ totalItems }} Total Records
        </span>
      </div>

      <NuxtLink
        to="/consultations/new"
        class="inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-2xl bg-gradient-to-r from-teal-600 to-emerald-600 hover:from-teal-700 hover:to-emerald-700 text-white font-bold text-sm shadow-md shadow-teal-500/25 hover:shadow-lg hover:shadow-teal-500/30 transition-all duration-150 transform hover:-translate-y-0.5"
      >
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M12 4v16m8-8H4" />
        </svg>
        <span>+ Record New Consultation</span>
      </NuxtLink>
    </div>

    <!-- Stats Component -->
    <ConsultationStats
      :total="totalItems"
      :page="page"
      :total-pages="totalPages"
      :sync-status="syncStatus"
    />

    <!-- Filter Component -->
    <ConsultationFilter
      v-model:phone="filters.phone"
      v-model:diagnosis-code="filters.diagnosis_code"
      @search="handleSearch"
      @reset="handleReset"
    />

    <!-- Table Component -->
    <ConsultationTable
      :items="consultations"
      :is-loading="isLoading"
      :has-active-filters="hasActiveFilters"
      :page="page"
      :page-size="pageSize"
      :total="totalItems"
      :total-pages="totalPages"
      :error-message="errorMessage"
      @page-change="changePage"
      @retry="fetchConsultations"
    />
  </div>
</template>

<script setup lang="ts">
import type { Consultation, PaginatedConsultationResponse, ConsultationFilter as IConsultationFilter } from '~/types';
import ConsultationStats from '~/components/consultation/ConsultationStats.vue';
import ConsultationFilter from '~/components/consultation/ConsultationFilter.vue';
import ConsultationTable from '~/components/consultation/ConsultationTable.vue';

const api = useApi();

const consultations = ref<Consultation[]>([]);
const totalItems = ref(0);
const totalPages = ref(0);
const page = ref(1);
const pageSize = ref(10);
const isLoading = ref(false);
const errorMessage = ref<string | null>(null);

const syncStatus = computed<'synced' | 'syncing' | 'error'>(() => {
  if (errorMessage.value) return 'error';
  if (isLoading.value) return 'syncing';
  return 'synced';
});

const filters = reactive<IConsultationFilter>({
  phone: '',
  diagnosis_code: '',
});

const hasActiveFilters = computed(() => !!filters.phone.trim() || !!filters.diagnosis_code.trim());

const fetchConsultations = async () => {
  isLoading.value = true;
  errorMessage.value = null;
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

    const res = await api.get<PaginatedConsultationResponse>('/api/consultation/', query);
    consultations.value = res.items || [];
    totalItems.value = res.total;
    totalPages.value = res.total_pages;
  } catch (err: any) {
    console.error('Failed to load consultations', err);
    // Clear stale records so stale data is not mistaken for active query results
    consultations.value = [];
    totalItems.value = 0;
    totalPages.value = 0;
    errorMessage.value =
      err?.data?.message ||
      err?.message ||
      'Unable to connect to the clinical database. Please check your network connection or try again.';
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

onMounted(() => {
  fetchConsultations();
});
</script>
