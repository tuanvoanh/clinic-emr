<template>
  <div class="max-w-4xl mx-auto space-y-6">
    <!-- Breadcrumb & Back Link -->
    <div class="flex items-center gap-2 text-sm text-slate-500">
      <NuxtLink to="/" class="hover:text-teal-600 flex items-center gap-1.5 font-semibold transition-colors">
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        <span>Back to Consultations</span>
      </NuxtLink>
    </div>

    <!-- Header Banner -->
    <div class="bg-gradient-to-br from-teal-700 via-teal-600 to-emerald-500 rounded-3xl p-8 text-white shadow-lg shadow-teal-700/20 relative overflow-hidden">
      <!-- Background pattern decoration -->
      <div class="absolute -right-10 -bottom-10 w-64 h-64 bg-white/10 rounded-full blur-2xl pointer-events-none"></div>
      <div class="relative z-10 max-w-2xl">
        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold bg-white/20 text-white border border-white/30 mb-3">
          Clinical Encounter
        </span>
        <h1 class="text-2xl sm:text-3xl font-extrabold tracking-tight">Record Patient Consultation</h1>
        <p class="text-teal-100 text-sm mt-2 leading-relaxed">
          Record diagnosis, treatment recommendations, and patient records. If the patient exists by their unique phone number, their profile will be linked automatically.
        </p>
      </div>
    </div>

    <!-- Error Alert Message -->
    <div
      v-if="errorMessage"
      class="p-4 rounded-2xl bg-rose-50/90 border border-rose-200 flex items-start gap-3 text-rose-700 text-sm animate-shake"
    >
      <svg class="w-5 h-5 flex-shrink-0 text-rose-500 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <div class="flex-1 font-semibold">{{ errorMessage }}</div>
    </div>

    <!-- Form Container -->
    <form @submit.prevent="handleSubmit" class="space-y-6">
      <!-- Section 1: Patient Information -->
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
          <!-- Patient Name -->
          <div class="sm:col-span-2">
            <label for="patient_name" class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
              Full Legal Name <span class="text-rose-500">*</span>
            </label>
            <input
              id="patient_name"
              v-model="form.patient_name"
              type="text"
              required
              minlength="2"
              maxlength="150"
              placeholder="e.g. Jane Smith"
              class="w-full px-4 py-3 text-sm rounded-xl border border-slate-200 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 outline-none transition bg-slate-50/50 focus:bg-white font-medium text-slate-800"
            />
          </div>

          <!-- Date of Birth -->
          <div>
            <label for="dob" class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
              Date of Birth <span class="text-rose-500">*</span>
            </label>
            <input
              id="dob"
              v-model="form.dob"
              type="date"
              required
              :max="todayDate"
              class="w-full px-4 py-3 text-sm rounded-xl border border-slate-200 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 outline-none transition bg-slate-50/50 focus:bg-white font-medium text-slate-800"
            />
            <p class="text-[11px] text-slate-400 mt-1.5 font-medium">Standard format: YYYY-MM-DD</p>
          </div>

          <!-- Phone Number (Singapore) -->
          <div>
            <label for="phone" class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
              Singapore Mobile Number <span class="text-rose-500">*</span>
            </label>
            <div class="relative">
              <span class="absolute inset-y-0 left-0 pl-3.5 flex items-center text-xs font-bold text-teal-700 bg-teal-50/80 my-1 ml-1 px-2 rounded-lg border border-teal-100">
                +65
              </span>
              <input
                id="phone"
                v-model="form.phone"
                type="tel"
                required
                pattern="^[89]\d{7}$"
                maxlength="8"
                placeholder="81234567"
                class="w-full pl-16 pr-4 py-3 text-sm rounded-xl border border-slate-200 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 outline-none transition bg-slate-50/50 focus:bg-white font-mono font-medium text-slate-800"
              />
            </div>
            <p class="text-[11px] text-slate-400 mt-1.5 font-medium">Unique patient key: 8 digits starting with 8 or 9</p>
          </div>
        </div>
      </div>

      <!-- Section 2: Clinical Details -->
      <div class="bg-white rounded-3xl border border-slate-200/70 p-6 sm:p-8 shadow-xs space-y-6">
        <div class="flex items-center gap-3 pb-4 border-b border-slate-100">
          <div class="w-9 h-9 rounded-xl bg-teal-50 border border-teal-100 text-teal-700 flex items-center justify-center font-extrabold text-sm">
            02
          </div>
          <div>
            <h2 class="text-base font-bold text-slate-900">Diagnosis & Care Plan</h2>
            <p class="text-xs text-slate-400">ICD-10 clinical classification and physician notes</p>
          </div>
        </div>

        <!-- ICD-10 Search & Select -->
        <div class="relative">
          <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
            ICD-10 Diagnosis Classification <span class="text-rose-500">*</span>
          </label>

          <!-- Selected Diagnosis Badge -->
          <div
            v-if="selectedDiagnosis"
            class="p-4 rounded-2xl bg-teal-50/70 border border-teal-200/80 flex items-center justify-between shadow-2xs"
          >
            <div class="flex items-center gap-3.5">
              <span class="px-3 py-1.5 rounded-xl bg-teal-600 text-white font-mono font-bold text-xs shadow-xs">
                {{ selectedDiagnosis.code }}
              </span>
              <div>
                <p class="text-sm font-bold text-slate-900">{{ selectedDiagnosis.description }}</p>
                <p class="text-[11px] text-teal-700 font-semibold mt-0.5">Validated clinical code</p>
              </div>
            </div>
            <button
              type="button"
              @click="clearDiagnosis"
              class="text-xs font-bold text-slate-500 hover:text-rose-600 bg-white hover:bg-rose-50 px-3 py-1.5 rounded-xl border border-slate-200/80 transition cursor-pointer"
            >
              Change Code
            </button>
          </div>

          <!-- Search Input for ICD-10 -->
          <div v-else class="relative">
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
              <input
                v-model="diagnosisQuery"
                type="text"
                placeholder="Search by code or keyword (e.g. Headache, Fever, A00.0)..."
                @focus="isSearchingDiagnosis = true"
                class="w-full pl-10 pr-10 py-3 text-sm rounded-xl border border-slate-200 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 outline-none transition bg-slate-50/50 focus:bg-white font-medium"
              />
              <div v-if="isSearchLoading" class="absolute right-3.5 top-3.5 text-teal-600">
                <svg class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              </div>
            </div>

            <!-- Dropdown Options -->
            <div
              v-if="isSearchingDiagnosis && diagnosisResults.length > 0"
              class="absolute z-20 mt-1.5 w-full max-h-64 overflow-y-auto bg-white rounded-2xl border border-slate-200 shadow-xl divide-y divide-slate-100"
            >
              <div
                v-for="code in diagnosisResults"
                :key="code.code"
                @mousedown="selectDiagnosis(code)"
                class="p-3.5 hover:bg-teal-50/50 cursor-pointer flex items-center justify-between transition-colors"
              >
                <div class="flex items-center gap-3">
                  <span class="font-mono text-xs font-bold text-teal-700 bg-teal-50 px-2.5 py-1 rounded-lg border border-teal-200/80">
                    {{ code.code }}
                  </span>
                  <span class="text-xs font-semibold text-slate-800">{{ code.description }}</span>
                </div>
                <span class="text-[11px] font-bold text-teal-600 opacity-0 hover:opacity-100 transition">Select &rarr;</span>
              </div>
            </div>
            <div
              v-else-if="isSearchingDiagnosis && diagnosisQuery.trim() && !isSearchLoading"
              class="absolute z-20 mt-1.5 w-full p-4 bg-white rounded-2xl border border-slate-200 shadow-xl text-center text-xs text-slate-500 font-medium"
            >
              No matching ICD-10 codes found for "{{ diagnosisQuery }}".
            </div>
          </div>
        </div>

        <!-- Treatment Notes -->
        <div>
          <label for="treatment_notes" class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
            Clinical Notes & Prescription <span class="text-rose-500">*</span>
          </label>
          <textarea
            id="treatment_notes"
            v-model="form.treatment_notes"
            required
            minlength="5"
            rows="4"
            placeholder="Record symptoms, observations, medical prescriptions and instructions for patient care..."
            class="w-full px-4 py-3.5 text-sm rounded-xl border border-slate-200 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 outline-none transition bg-slate-50/50 focus:bg-white font-medium leading-relaxed text-slate-800"
          ></textarea>
          <p class="text-[11px] text-slate-400 mt-1.5 font-medium">Minimum 5 characters describing the clinical consultation.</p>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex items-center justify-end gap-3 pt-2">
        <NuxtLink
          to="/"
          class="px-5 py-3 rounded-xl border border-slate-200 text-slate-600 hover:bg-slate-100 text-sm font-bold transition cursor-pointer"
        >
          Cancel
        </NuxtLink>

        <button
          type="submit"
          :disabled="isSubmitting"
          class="px-8 py-3 rounded-xl bg-gradient-to-r from-teal-600 to-emerald-600 hover:from-teal-700 hover:to-emerald-700 text-white text-sm font-bold shadow-md shadow-teal-600/25 transition-all duration-150 flex items-center gap-2 disabled:opacity-60 cursor-pointer transform hover:-translate-y-0.5"
        >
          <svg
            v-if="isSubmitting"
            class="animate-spin h-4 w-4 text-white"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span>{{ isSubmitting ? 'Recording Encounter...' : 'Complete & Save Consultation' }}</span>
        </button>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
interface DiagnosisCode {
  code: string;
  description: string;
}

const api = useApi();
const router = useRouter();

const todayDate = computed(() => {
  return new Date().toISOString().split('T')[0];
});

const form = reactive({
  patient_name: '',
  dob: '',
  phone: '',
  diagnosis_code: '',
  treatment_notes: '',
});

const diagnosisQuery = ref('');
const diagnosisResults = ref<DiagnosisCode[]>([]);
const selectedDiagnosis = ref<DiagnosisCode | null>(null);
const isSearchingDiagnosis = ref(false);
const isSearchLoading = ref(false);

const isSubmitting = ref(false);
const errorMessage = ref('');

// Debounced ICD-10 Search
let searchTimeout: NodeJS.Timeout | null = null;
watch(diagnosisQuery, (newVal) => {
  if (searchTimeout) clearTimeout(searchTimeout);

  if (!newVal.trim()) {
    diagnosisResults.value = [];
    return;
  }

  isSearchLoading.value = true;
  searchTimeout = setTimeout(async () => {
    try {
      const res = await api.get<DiagnosisCode[]>('/api/diagnosis/', {
        search: newVal.trim(),
      });
      diagnosisResults.value = res || [];
    } catch (err) {
      console.error('Diagnosis search failed', err);
    } finally {
      isSearchLoading.value = false;
    }
  }, 300);
});

const selectDiagnosis = (code: DiagnosisCode) => {
  selectedDiagnosis.value = code;
  form.diagnosis_code = code.code;
  isSearchingDiagnosis.value = false;
  diagnosisQuery.value = '';
};

const clearDiagnosis = () => {
  selectedDiagnosis.value = null;
  form.diagnosis_code = '';
  isSearchingDiagnosis.value = true;
};

const handleSubmit = async () => {
  errorMessage.value = '';

  if (!form.diagnosis_code) {
    errorMessage.value = 'Please select a valid ICD-10 diagnosis code.';
    return;
  }

  isSubmitting.value = true;
  try {
    await api.post('/api/consultation/', {
      patient_name: form.patient_name.trim(),
      dob: form.dob,
      phone: form.phone.trim(),
      diagnosis_code: form.diagnosis_code,
      treatment_notes: form.treatment_notes.trim(),
    });

    // Navigate back to consultation list on success
    router.push('/');
  } catch (err: any) {
    if (err.data?.message) {
      errorMessage.value = err.data.message;
    } else if (err.data?.detail) {
      errorMessage.value = typeof err.data.detail === 'string'
        ? err.data.detail
        : 'Validation error. Please verify the input values.';
    } else {
      errorMessage.value = 'Failed to create consultation record. Please try again.';
    }
  } finally {
    isSubmitting.value = false;
  }
};
</script>
