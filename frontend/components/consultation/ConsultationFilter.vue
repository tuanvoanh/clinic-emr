<template>
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
      <!-- Search by Phone with Live Patient Suggestions -->
      <div class="sm:col-span-5 relative">
        <div class="flex items-center justify-between mb-1.5">
          <label class="block text-xs font-bold text-slate-600">
            Patient Mobile Number
          </label>
          <span class="text-[11px] text-slate-400 font-medium">8 digits, starts with 8 or 9</span>
        </div>
        <div class="relative">
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <span class="text-xs font-bold text-teal-700 bg-teal-50 px-1.5 py-0.5 rounded border border-teal-200/80 font-mono">
              +65
            </span>
          </div>
          <input
            :value="phone"
            @input="onPhoneInput(($event.target as HTMLInputElement).value)"
            type="text"
            maxlength="8"
            placeholder="Type e.g. 8 or 9 to search..."
            @focus="showPatientDropdown = true"
            @keyup.enter="handleSearch"
            class="w-full pl-14 pr-9 py-2.5 text-sm rounded-xl border focus:ring-2 outline-none transition bg-slate-50/50 focus:bg-white font-mono"
            :class="phoneError ? 'border-rose-300 focus:border-rose-500 focus:ring-rose-500/20 text-rose-800' : 'border-slate-200 focus:border-teal-500 focus:ring-teal-500/20 text-slate-800'"
          />
          <div v-if="isSearchingPatients" class="absolute right-3 top-3 text-teal-600">
            <svg class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          </div>
        </div>

        <!-- Patient Search Results Dropdown -->
        <div
          v-if="showPatientDropdown && patientSuggestions.length > 0"
          class="absolute z-30 mt-1.5 w-full bg-white rounded-2xl border border-slate-200 shadow-xl divide-y divide-slate-100 max-h-60 overflow-y-auto"
        >
          <div
            v-for="patient in patientSuggestions"
            :key="patient.id"
            @mousedown="onSelectPatient(patient)"
            class="p-3 hover:bg-teal-50/60 cursor-pointer flex items-center justify-between transition-colors group"
          >
            <div class="flex items-center gap-2.5">
              <div class="w-7 h-7 rounded-lg bg-teal-50 text-teal-700 font-bold text-xs flex items-center justify-center">
                {{ getInitials(patient.full_name) }}
              </div>
              <div>
                <p class="text-xs font-bold text-slate-800 group-hover:text-teal-700 transition">{{ patient.full_name }}</p>
                <p class="text-[11px] text-slate-400">DOB: {{ patient.dob }}</p>
              </div>
            </div>
            <span class="font-mono text-xs font-bold text-teal-700 bg-teal-50 px-2 py-0.5 rounded border border-teal-200">
              +65 {{ patient.phone }}
            </span>
          </div>
        </div>

        <!-- Error Text -->
        <p v-if="phoneError" class="text-xs font-semibold text-rose-600 mt-1.5 flex items-center gap-1">
          <svg class="w-3.5 h-3.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span>{{ phoneError }}</span>
        </p>
      </div>

      <!-- Filter by Diagnosis Code with Live Suggestions -->
      <div class="sm:col-span-5 relative">
        <div class="flex items-center justify-between mb-1.5 h-4">
          <label class="block text-xs font-bold text-slate-600">
            ICD-10 Disease Code
          </label>
        </div>
        <div class="relative">
          <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
            </svg>
          </div>
          <input
            :value="diagnosisCode"
            @input="onDiagnosisInput(($event.target as HTMLInputElement).value)"
            type="text"
            placeholder="Type code or disease (e.g. A00.0, Headache)..."
            @focus="showDiagnosisDropdown = true"
            @keyup.enter="handleSearch"
            class="w-full pl-10 pr-9 py-2.5 text-sm rounded-xl border border-slate-200 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 outline-none transition bg-slate-50/50 focus:bg-white"
          />
          <div v-if="isSearchingDiagnoses" class="absolute right-3 top-3 text-teal-600">
            <svg class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          </div>
        </div>

        <!-- ICD-10 Search Results Dropdown -->
        <div
          v-if="showDiagnosisDropdown && diagnosisSuggestions.length > 0"
          class="absolute z-30 mt-1.5 w-full bg-white rounded-2xl border border-slate-200 shadow-xl divide-y divide-slate-100 max-h-60 overflow-y-auto"
        >
          <div
            v-for="diag in diagnosisSuggestions"
            :key="diag.code"
            @mousedown="onSelectDiagnosis(diag)"
            class="p-3 hover:bg-teal-50/60 cursor-pointer flex items-center justify-between transition-colors group"
          >
            <div class="flex items-center gap-2.5">
              <span class="font-mono text-xs font-bold text-teal-700 bg-teal-50 px-2 py-0.5 rounded border border-teal-200/80">
                {{ diag.code }}
              </span>
              <span class="text-xs font-semibold text-slate-800 group-hover:text-teal-700 transition">
                {{ diag.description }}
              </span>
            </div>
            <span class="text-[11px] font-bold text-teal-600 opacity-0 group-hover:opacity-100 transition">Select &rarr;</span>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="sm:col-span-2 flex flex-col justify-end">
        <div class="mb-1.5 h-4 hidden sm:block"></div>
        <div class="flex items-center gap-2">
          <button
            @click="handleSearch"
            class="flex-1 h-[42px] px-4 bg-slate-900 hover:bg-slate-800 active:bg-black text-white text-sm font-bold rounded-xl transition shadow-xs cursor-pointer inline-flex items-center justify-center border border-slate-900"
          >
            Filter
          </button>
          <button
            @click="handleReset"
            class="h-[42px] px-3.5 border border-slate-200 hover:bg-slate-100 active:bg-slate-200 text-slate-600 text-sm font-semibold rounded-xl transition cursor-pointer inline-flex items-center justify-center bg-white"
            title="Reset filters"
          >
            Reset
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Patient, DiagnosisCode } from '~/types';

const props = defineProps<{
  phone: string;
  diagnosisCode: string;
}>();

const emit = defineEmits<{
  (e: 'update:phone', val: string): void;
  (e: 'update:diagnosisCode', val: string): void;
  (e: 'search'): void;
  (e: 'reset'): void;
}>();

const api = useApi();

const phoneError = ref('');
const patientSuggestions = ref<Patient[]>([]);
const isSearchingPatients = ref(false);
const showPatientDropdown = ref(false);

const diagnosisSuggestions = ref<DiagnosisCode[]>([]);
const isSearchingDiagnoses = ref(false);
const showDiagnosisDropdown = ref(false);

const hasActiveFilters = computed(() => !!props.phone.trim() || !!props.diagnosisCode.trim());

let patientSearchTimer: ReturnType<typeof setTimeout> | null = null;
let diagnosisSearchTimer: ReturnType<typeof setTimeout> | null = null;

const onPhoneInput = (val: string) => {
  emit('update:phone', val);
  phoneError.value = '';
  const trimmed = val.trim();

  if (patientSearchTimer) clearTimeout(patientSearchTimer);

  if (!trimmed || !/^[89]\d*$/.test(trimmed)) {
    patientSuggestions.value = [];
    isSearchingPatients.value = false;
    return;
  }

  isSearchingPatients.value = true;
  patientSearchTimer = setTimeout(async () => {
    try {
      const res = await api.get<Patient[]>('/api/patient/', {
        phone: trimmed,
        limit: 10,
      });
      patientSuggestions.value = res || [];
      showPatientDropdown.value = (res && res.length > 0);
    } catch (err) {
      console.error('Patient search error:', err);
      patientSuggestions.value = [];
    } finally {
      isSearchingPatients.value = false;
    }
  }, 250);
};

const onSelectPatient = (patient: Patient) => {
  emit('update:phone', patient.phone);
  showPatientDropdown.value = false;
  patientSuggestions.value = [];
  phoneError.value = '';
  emit('search');
};

const onDiagnosisInput = (val: string) => {
  emit('update:diagnosisCode', val);
  const trimmed = val.trim();

  if (diagnosisSearchTimer) clearTimeout(diagnosisSearchTimer);

  if (!trimmed) {
    diagnosisSuggestions.value = [];
    isSearchingDiagnoses.value = false;
    return;
  }

  isSearchingDiagnoses.value = true;
  diagnosisSearchTimer = setTimeout(async () => {
    try {
      const res = await api.get<DiagnosisCode[]>('/api/diagnosis/', {
        search: trimmed,
      });
      diagnosisSuggestions.value = res || [];
      showDiagnosisDropdown.value = (res && res.length > 0);
    } catch (err) {
      console.error('Diagnosis search error:', err);
      diagnosisSuggestions.value = [];
    } finally {
      isSearchingDiagnoses.value = false;
    }
  }, 250);
};

const onSelectDiagnosis = (diag: DiagnosisCode) => {
  emit('update:diagnosisCode', diag.code);
  showDiagnosisDropdown.value = false;
  diagnosisSuggestions.value = [];
  emit('search');
};

const validatePhone = (phone: string): boolean => {
  if (!phone) return true;
  return /^[89]\d{7}$/.test(phone);
};

const handleSearch = () => {
  phoneError.value = '';
  const trimmedPhone = props.phone.trim();

  if (trimmedPhone && !validatePhone(trimmedPhone)) {
    phoneError.value = 'Singapore mobile number must be exactly 8 digits starting with 8 or 9 (e.g. 81234567, 91234567).';
    return;
  }

  showPatientDropdown.value = false;
  showDiagnosisDropdown.value = false;
  emit('search');
};

const handleReset = () => {
  phoneError.value = '';
  patientSuggestions.value = [];
  diagnosisSuggestions.value = [];
  showPatientDropdown.value = false;
  showDiagnosisDropdown.value = false;
  emit('update:phone', '');
  emit('update:diagnosisCode', '');
  emit('reset');
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
</script>
