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
      <!-- Section 1: Patient Demographics Component -->
      <PatientDemographicsForm
        v-model:phone="form.phone"
        v-model:dob="form.dob"
        v-model:patient-name="form.patient_name"
      />

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

        <!-- ICD-10 Search & Select Component -->
        <DiagnosisSelect v-model="selectedDiagnosis" />

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
import type { DiagnosisCode } from '~/types';
import PatientDemographicsForm from '~/components/consultation/PatientDemographicsForm.vue';
import DiagnosisSelect from '~/components/consultation/DiagnosisSelect.vue';

const api = useApi();
const router = useRouter();

const form = reactive({
  patient_name: '',
  dob: '',
  phone: '',
  treatment_notes: '',
});

const selectedDiagnosis = ref<DiagnosisCode | null>(null);
const isSubmitting = ref(false);
const errorMessage = ref('');

const handleSubmit = async () => {
  errorMessage.value = '';

  if (!selectedDiagnosis.value?.code) {
    errorMessage.value = 'Please select a valid ICD-10 diagnosis code.';
    return;
  }

  isSubmitting.value = true;
  try {
    await api.post('/api/consultation/', {
      patient_name: form.patient_name.trim(),
      dob: form.dob,
      phone: form.phone.trim(),
      diagnosis_code: selectedDiagnosis.value.code,
      treatment_notes: form.treatment_notes.trim(),
    });

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
