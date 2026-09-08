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

## 4. Harden default JWT configuration

**Priority:** High

`backend/app/core/config.py` contains predictable fallback credentials and a
development signing key. Require secure environment values outside demo mode,
shorten the token lifetime, and restrict or remove the public setup endpoint
after initial provisioning.

## 5. Complete consultation search behavior

**Priority:** Medium

Consultation filtering currently supports only exact phone and exact diagnosis
code. Clarify whether "search by patient" means phone or name, implement the
required patient-name/partial search if needed, and either implement or remove
the unused `search_term` repository parameter.

## 6. Validate real dates of birth

**Priority:** Medium

The consultation schema validates only the `YYYY-MM-DD` text pattern, while the
patient schema has no equivalent constraint. Use a Pydantic `date` field or a
validator to reject impossible and future dates, and add HTTP/schema tests for
values such as `2025-02-29` and `2026-99-99`.

## 7. Show reliable frontend request errors

**Priority:** Medium

`frontend/pages/index.vue` logs list failures but leaves stale records visible.
Add an explicit error and retry state, clear or clearly mark stale data, and do
not display the database as "Live Synced" when the latest request failed.

## 8. Prevent stale autocomplete responses

**Priority:** Medium

Diagnosis and patient autocomplete requests can complete out of order. Cancel
superseded requests with `AbortController` or ignore responses whose request ID
does not match the latest query in `DiagnosisSelect.vue`,
`ConsultationFilter.vue`, and `PatientDemographicsForm.vue`.

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
