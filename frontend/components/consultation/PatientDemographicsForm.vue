<template>
  <div class="bg-white rounded-3xl border border-slate-200/70 p-6 sm:p-8 shadow-xs space-y-6">
    <div class="flex items-center gap-3 pb-4 border-b border-slate-100">
      <div class="w-9 h-9 rounded-xl bg-teal-50 border border-teal-100 text-teal-700 flex items-center justify-center font-extrabold text-sm">
        01
      </div>
      <div>
        <h2 class="text-base font-bold text-slate-900">Patient Demographics</h2>
        <p class="text-xs text-slate-400">Identification and contact information</p>
      </div>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
      <!-- 1. Phone Number (Singapore) with Live Patient Search -->
      <div class="relative">
        <div class="flex items-center justify-between mb-2">
          <label for="phone" class="block text-xs font-bold text-slate-700 uppercase tracking-wider">
            Singapore Mobile Number <span class="text-rose-500">*</span>
          </label>
          <span v-if="autoFilledPatient" class="text-[11px] font-bold text-teal-700 bg-teal-50 px-2 py-0.5 rounded-full border border-teal-200">
            Existing Patient Matched
          </span>
        </div>
        <div class="relative">
          <span class="absolute inset-y-0 left-0 pl-3.5 flex items-center text-xs font-bold text-teal-700 bg-teal-50/80 my-1 ml-1 px-2 rounded-lg border border-teal-100">
            +65
          </span>
          <input
            id="phone"
            :value="phone"
            @input="onPhoneInput(($event.target as HTMLInputElement).value)"
            type="tel"
            required
            pattern="^[89]\d{7}$"
            maxlength="8"
            placeholder="81234567"
            @focus="showPatientDropdown = true"
            class="w-full pl-16 pr-10 py-3 text-sm rounded-xl border border-slate-200 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 outline-none transition bg-slate-50/50 focus:bg-white font-mono font-medium text-slate-800"
          />
          <div v-if="isSearchingPatients" class="absolute right-3.5 top-3.5 text-teal-600">
            <svg class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          </div>
        </div>
        <p class="text-[11px] text-slate-400 mt-1.5 font-medium">Unique patient key: 8 digits starting with 8 or 9</p>

        <!-- Patient Suggestions Dropdown -->
        <div
          v-if="showPatientDropdown && patientSuggestions.length > 0"
          class="absolute z-30 mt-1.5 w-full bg-white rounded-2xl border border-slate-200 shadow-xl divide-y divide-slate-100 max-h-60 overflow-y-auto"
        >
          <div
            v-for="patient in patientSuggestions"
            :key="patient.id"
            @mousedown="selectPatient(patient)"
            class="p-3 hover:bg-teal-50/60 cursor-pointer flex items-center justify-between transition-colors group"
          >
            <div class="flex items-center gap-2.5">
              <div class="w-8 h-8 rounded-lg bg-teal-50 text-teal-700 font-bold text-xs flex items-center justify-center">
                {{ getInitials(patient.full_name) }}
              </div>
              <div>
                <p class="text-xs font-bold text-slate-800 group-hover:text-teal-700 transition">{{ patient.full_name }}</p>
                <p class="text-[11px] text-slate-400">DOB: {{ patient.dob }}</p>
              </div>
            </div>
            <div class="text-right">
              <span class="font-mono text-xs font-bold text-teal-700 bg-teal-50 px-2 py-0.5 rounded border border-teal-200 block">
                +65 {{ patient.phone }}
              </span>
              <span class="text-[10px] text-slate-400 mt-0.5 block">Click to auto-fill</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 2. Date of Birth -->
      <div>
        <label for="dob" class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
          Date of Birth <span class="text-rose-500">*</span>
        </label>
        <input
          id="dob"
          :value="dob"
          @input="$emit('update:dob', ($event.target as HTMLInputElement).value)"
          type="date"
          required
          :max="todayDate"
          class="w-full px-4 py-3 text-sm rounded-xl border border-slate-200 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 outline-none transition bg-slate-50/50 focus:bg-white font-medium text-slate-800"
        />
        <p class="text-[11px] text-slate-400 mt-1.5 font-medium">Standard format: YYYY-MM-DD</p>
      </div>

      <!-- 3. Patient Name -->
      <div class="sm:col-span-2">
        <label for="patient_name" class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
          Full Legal Name <span class="text-rose-500">*</span>
        </label>
        <input
          id="patient_name"
          :value="patientName"
          @input="$emit('update:patientName', ($event.target as HTMLInputElement).value)"
          type="text"
          required
          minlength="2"
          maxlength="150"
          placeholder="e.g. Jane Smith"
          class="w-full px-4 py-3 text-sm rounded-xl border border-slate-200 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 outline-none transition bg-slate-50/50 focus:bg-white font-medium text-slate-800"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Patient } from '~/types';

const props = defineProps<{
  phone: string;
  dob: string;
  patientName: string;
}>();

const emit = defineEmits<{
  (e: 'update:phone', val: string): void;
  (e: 'update:dob', val: string): void;
  (e: 'update:patientName', val: string): void;
}>();

const api = useApi();

const todayDate = computed(() => {
  return new Date().toISOString().split('T')[0];
});

const patientSuggestions = ref<Patient[]>([]);
const isSearchingPatients = ref(false);
const showPatientDropdown = ref(false);
const autoFilledPatient = ref(false);

let patientSearchTimer: ReturnType<typeof setTimeout> | null = null;

const onPhoneInput = (val: string) => {
  emit('update:phone', val);
  const trimmed = val.trim();

  if (autoFilledPatient.value) {
    autoFilledPatient.value = false;
  }

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
        limit: 8,
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

const selectPatient = (patient: Patient) => {
  emit('update:phone', patient.phone);
  emit('update:patientName', patient.full_name);
  emit('update:dob', patient.dob);
  autoFilledPatient.value = true;
  showPatientDropdown.value = false;
  patientSuggestions.value = [];
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
