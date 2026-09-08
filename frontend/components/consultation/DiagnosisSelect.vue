<template>
  <div class="relative">
    <label class="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
      ICD-10 Diagnosis Classification <span class="text-rose-500">*</span>
    </label>

    <!-- Selected Diagnosis Badge -->
    <div
      v-if="modelValue"
      class="p-4 rounded-2xl bg-teal-50/70 border border-teal-200/80 flex items-center justify-between shadow-2xs"
    >
      <div class="flex items-center gap-3.5">
        <span class="px-3 py-1.5 rounded-xl bg-teal-600 text-white font-mono font-bold text-xs shadow-xs">
          {{ modelValue.code }}
        </span>
        <div>
          <p class="text-sm font-bold text-slate-900">{{ modelValue.description }}</p>
          <p class="text-[11px] text-teal-700 font-semibold mt-0.5">Validated clinical code</p>
        </div>
      </div>
      <button
        type="button"
        @click="clearSelection"
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
          :value="query"
          @input="onInput(($event.target as HTMLInputElement).value)"
          type="text"
          placeholder="Type to search ICD-10 (e.g. Headache, Fever, A00.0)..."
          @focus="handleFocus"
          @keydown.enter.prevent="handleEnter"
          class="w-full pl-10 pr-10 py-3 text-sm rounded-xl border border-slate-200 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 outline-none transition bg-slate-50/50 focus:bg-white font-medium"
        />
        <div v-if="isLoading" class="absolute right-3.5 top-3.5 text-teal-600">
          <svg class="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </div>
      </div>

      <!-- Dropdown Options -->
      <div
        v-if="isOpen && results.length > 0"
        class="absolute z-20 mt-1.5 w-full max-h-64 overflow-y-auto bg-white rounded-2xl border border-slate-200 shadow-xl divide-y divide-slate-100"
      >
        <div
          v-for="item in results"
          :key="item.code"
          @mousedown="selectItem(item)"
          class="p-3.5 hover:bg-teal-50/50 cursor-pointer flex items-center justify-between transition-colors"
        >
          <div class="flex items-center gap-3">
            <span class="font-mono text-xs font-bold text-teal-700 bg-teal-50 px-2.5 py-1 rounded-lg border border-teal-200/80">
              {{ item.code }}
            </span>
            <span class="text-xs font-semibold text-slate-800">{{ item.description }}</span>
          </div>
          <span class="text-[11px] font-bold text-teal-600 opacity-0 hover:opacity-100 transition">Select &rarr;</span>
        </div>
      </div>
      <div
        v-else-if="isOpen && query.trim() && !isLoading"
        class="absolute z-20 mt-1.5 w-full p-4 bg-white rounded-2xl border border-slate-200 shadow-xl text-center text-xs text-slate-500 font-medium"
      >
        No matching ICD-10 codes found for "{{ query }}".
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { DiagnosisCode } from '~/types';

defineProps<{
  modelValue: DiagnosisCode | null;
}>();

const emit = defineEmits<{
  (e: 'update:modelValue', val: DiagnosisCode | null): void;
}>();

const api = useApi();

const query = ref('');
const results = ref<DiagnosisCode[]>([]);
const isOpen = ref(false);
const isLoading = ref(false);

let searchTimeout: ReturnType<typeof setTimeout> | null = null;
let abortController: AbortController | null = null;

const fetchDiagnoses = async (term: string) => {
  if (abortController) {
    abortController.abort();
  }
  const currentController = new AbortController();
  abortController = currentController;

  isLoading.value = true;
  try {
    const res = await api.get<DiagnosisCode[]>(
      '/api/diagnosis/',
      { search: term.trim() },
      { signal: currentController.signal }
    );
    results.value = res || [];
    isOpen.value = true;
  } catch (err: any) {
    if (err.name === 'AbortError' || err.message?.includes('aborted')) {
      return; // Ignore aborted requests
    }
    console.error('Diagnosis search error:', err);
    results.value = [];
  } finally {
    if (abortController === currentController) {
      isLoading.value = false;
    }
  }
};

onUnmounted(() => {
  if (searchTimeout) clearTimeout(searchTimeout);
  if (abortController) abortController.abort();
});

const onInput = (val: string) => {
  query.value = val;
  isOpen.value = true;
  
  if (searchTimeout) {
    clearTimeout(searchTimeout);
  }

  isLoading.value = true;
  searchTimeout = setTimeout(() => {
    fetchDiagnoses(val);
  }, 250);
};

const handleEnter = (e: Event) => {
  e.preventDefault();
  if (searchTimeout) {
    clearTimeout(searchTimeout);
  }
  fetchDiagnoses(query.value);
};

const handleFocus = () => {
  isOpen.value = true;
  if (results.value.length === 0) {
    fetchDiagnoses(query.value);
  }
};

const selectItem = (item: DiagnosisCode) => {
  emit('update:modelValue', item);
  isOpen.value = false;
  query.value = '';
};

const clearSelection = () => {
  emit('update:modelValue', null);
  isOpen.value = true;
};
</script>
