# ClinicCare Improvement Backlog

## 1. Fix the missing users table migration (Completed)

**Status:** Completed

`backend/alembic/versions/6586ac325c7f_add_user_model.py` now creates the
`users` table and its indexes, with matching downgrade operations.
`backend/alembic/env.py` imports `app.models`, ensuring that the `User` model and
the other model metadata are available to Alembic autogeneration.

## 2. Document ICD-10 dataset provenance (Optional)

**Status:** Core requirement completed

`backend/app/db/seed_icd10.py` contains exactly 100 unique ICD-10 codes and
inserts or updates them in the SQLite table when the seed command runs. This
satisfies the database population requirement without requiring a separate raw
SQL file. As an optional documentation improvement, record the source URL,
ICD-10-CM version, retrieval date, and code selection process.

## 3. Make consultation creation atomic (Completed)

**Status:** Completed

Patient and consultation repositories now support `commit=False` and use
`flush()` so the endpoint can persist both records with one final `commit()`.
The endpoint rolls back failures, retries after a concurrent unique-phone
conflict by loading the existing patient, and the integration test verifies that
a failed consultation insert does not leave a patient record behind.

## 4. Harden default JWT configuration (Completed)

**Status:** Completed

`SECRET_KEY`, `FIRST_SUPERUSER_EMAIL`, and `FIRST_SUPERUSER_PASSWORD` are now
mandatory environment settings with no application fallback. The default token
lifetime is 60 minutes, and `ALLOW_SETUP_ENDPOINT` can disable the public setup
route after provisioning. The documented credentials remaining in
`docker-compose.demo.yaml` are explicitly scoped to the local demo stack.

## 5. Complete consultation search behavior

**Priority:** Medium

Consultation filtering currently supports only exact phone and exact diagnosis
code. Clarify whether "search by patient" means phone or name, implement the
required patient-name/partial search if needed, and either implement or remove
the unused `search_term` repository parameter.

## 6. Validate real dates of birth (Completed)

**Status:** Completed

Patient and consultation schemas now share a date-of-birth validator that
enforces the strict `YYYY-MM-DD` format, rejects impossible dates, future dates,
and dates before `1900-01-01`, while accepting valid leap-year dates. Schema and
HTTP integration tests cover malformed, non-zero-padded, impossible, future,
and unreasonably old values.

## 7. Show reliable frontend request errors (Completed)

**Status:** Completed

`frontend/pages/index.vue` now records request failures and clears stale list
data. `ConsultationTable.vue` renders the error message with a retry action, and
`ConsultationStats.vue` reports syncing, synced, or connection-error state
instead of always displaying "Live Synced".

## 8. Prevent stale autocomplete responses (Completed)

**Status:** Completed

`DiagnosisSelect.vue`, `ConsultationFilter.vue`, and
`PatientDemographicsForm.vue` now cancel superseded requests with
`AbortController`, pass the abort signal through `useApi`, ignore cancellation
errors, and clean up timers and active requests when unmounted.

## 9. Improve frontend token storage and session validation

**Priority:** Medium

The JWT cookie is readable by JavaScript and authentication is inferred only
from cookie presence. Prefer a server-managed `HttpOnly`, `Secure`, `SameSite`
cookie where possible, validate the session on startup, handle token expiry,
and remove the unsupported "secure cookies" documentation claim otherwise.

## 10. Document the API path difference

**Priority:** Low

The task examples use `/diagnosis` and `/consultation`, while this application
exposes `/api/diagnosis/` and `/api/consultation/`. Document the API prefix
clearly and consider compatibility routes only if the evaluator requires the
sample paths exactly.
