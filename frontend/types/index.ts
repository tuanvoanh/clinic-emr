export interface Consultation {
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

export interface PaginatedConsultationResponse {
  items: Consultation[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface Patient {
  id: number;
  full_name: string;
  dob: string;
  phone: string;
}

export interface DiagnosisCode {
  code: string;
  description: string;
}

export interface ConsultationFilter {
  phone: string;
  diagnosis_code: string;
}
