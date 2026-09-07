# Clinic EMR Frontend (Nuxt 3 SPA)

Production-ready, client-side rendered Nuxt 3 frontend application for Clinic EMR.

## 🌟 Key Features

1. **Past Consultations List & Search** (`/`)
   - Paginated medical record history.
   - Filter by Singapore phone number (`8xxxxxxx` / `9xxxxxxx`).
   - Filter by ICD-10 diagnosis code.
   - Doctor & patient details presentation with clean typography.

2. **New Consultation Form** (`/consultations/new`)
   - Patient auto-registration & reuse by unique phone number.
   - Real-time debounced search for ICD-10 diagnosis codes.
   - Structured validation for name, date of birth, phone, and treatment notes.

3. **Doctor Authentication** (`/login`)
   - JWT authentication integrated with `/api/auth/login/access-token`.
   - Global client-side route guard (`middleware/auth.global.ts`).
   - Token persistence in secure cookies.

4. **Production Architecture**
   - **Zero Hardcoded URLs**: Configured via `runtimeConfig` and `NUXT_PUBLIC_API_BASE_URL` in `.env`.
   - **Client-Side Only**: `ssr: false` in `nuxt.config.ts`.
   - **Tailwind CSS**: Modern, responsive clinical design system.

---

## 🚀 Quickstart

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Configure Environment
Ensure `.env` points to your backend FastAPI server:
```env
NUXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
```

### 3. Run Development Server
```bash
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

### 4. Production Build
```bash
npm run build
npm run preview
```
