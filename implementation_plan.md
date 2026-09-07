# FastAPI Backend Implementation Plan for ClinicCare Mini EMR

This plan outlines the architecture and implementation steps for building the backend of the ClinicCare Mini EMR using FastAPI, SQLite, SQLAlchemy, and Pydantic. 

Dự án sẽ được cấu trúc theo chuẩn của một **ứng dụng FastAPI quy mô lớn** (tuân theo Repository Pattern), phân chia rõ ràng các tầng (layers) như core, models, schemas, repositories, và api endpoints.

## Proposed Changes

### Cấu trúc thư mục (Scalable FastAPI Structure)

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Khởi tạo app FastAPI, cấu hình CORS, kết nối router
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Quản lý các biến môi trường (Settings)
│   │   └── database.py         # Khởi tạo SQLAlchemy engine, SessionLocal
│   ├── models/                 # Chứa các Model SQLAlchemy (Định nghĩa DB)
│   │   ├── __init__.py
│   │   ├── base.py             # Base model (Declarative Base)
│   │   ├── patient.py
│   │   ├── diagnosis.py        # ICD10Code model
│   │   └── consultation.py
│   ├── schemas/                # Chứa các Model Pydantic (Validate Input/Output)
│   │   ├── __init__.py
│   │   ├── patient.py
│   │   ├── diagnosis.py
│   │   └── consultation.py
│   ├── repositories/           # Chứa logic thao tác với Database (Repository Pattern)
│   │   ├── __init__.py
│   │   ├── patient.py
│   │   ├── diagnosis.py
│   │   └── consultation.py
│   ├── api/                    # Chứa các Route API
│   │   ├── __init__.py
│   │   ├── dependencies.py     # Các Dependency như get_db()
│   │   ├── api_router.py       # Gom các router lại với nhau
│   │   └── endpoints/
│   │       ├── __init__.py
│   │       ├── diagnosis.py    # GET /diagnosis
│   │       └── consultation.py # POST /consultation, GET /consultation
│   └── db/
│       ├── __init__.py
│       └── seed.py             # Tự động nạp (seed) 100 mã ICD-10
├── requirements.txt            # Danh sách thư viện (fastapi, uvicorn, sqlalchemy, pydantic...)
└── .env                        # Chứa các biến môi trường cấu hình
```

### 1. Database & Models (Tầng Dữ liệu)

- **`app/core/database.py`**: Thiết lập kết nối SQLite qua biến môi trường ở `app/core/config.py`.
- **`app/models/`**: 
  - `ICD10Code`: `code` (PK), `description`.
  - `Patient`: `id` (PK), `full_name`, `dob`, `phone`.
  - `Consultation`: `id` (PK), `patient_id` (FK), `diagnosis_code` (FK), `treatment_notes`, `created_at`.

### 2. Validation & Schemas (Tầng Xác thực)

- **`app/schemas/`**:
  - Tách riêng schema đầu vào và đầu ra. Ví dụ: `ConsultationCreate` (dùng cho POST) và `ConsultationResponse` (dùng cho GET). Đảm bảo validate chặt chẽ thông tin từ request.
  - Cung cấp mô tả (`Field(description="...")`) chi tiết để Swagger UI hiển thị rõ ràng.

### 3. Repositories (Tầng Xử lý Database - Repository Pattern)

- **`app/repositories/`**: 
  - Mọi thao tác Query DB sẽ không nằm chung ở API endpoint mà được chuyển xuống tầng này để dễ tái sử dụng và mock khi test.
  - Viết **comment (docstring) chuẩn xịn** cho từng hàm (VD: params, return type).
  - Các hàm như: `get_diagnoses_by_term()`, `get_patient_by_details()`, `create_patient()`, `create_consultation()`, `get_all_consultations()`.

### 4. API Endpoints (Tầng Giao tiếp)

- **Mục tiêu**: **Tự động generate Swagger UI xịn xò** thông qua metadata của FastAPI. Mọi hàm sẽ có docstring rõ ràng giải thích chức năng, parameter, và return models.
- **`app/api/endpoints/diagnosis.py`**:
  - `GET /diagnosis?search={term}`: Gọi hàm `repositories.diagnosis.get_diagnoses_by_term()`.
- **`app/api/endpoints/consultation.py`**:
  - `POST /consultation`: 
    1. Kiểm tra tồn tại qua `repositories.patient.get_patient_by_details()`, nếu không có thì `repositories.patient.create_patient()`.
    2. Tạo bệnh án qua `repositories.consultation.create_consultation()`.
  - `GET /consultation`: Gọi hàm lấy danh sách từ `repositories.consultation.get_all_consultations()`.

### 5. Setup & Initialization

- **`app/main.py`**: Khai báo FastAPI app, gắn `api_router`, khai báo title và mô tả cho Swagger UI, đồng thời gọi event khởi động để tự động kiểm tra và chạy `seed.py`.

## Verification Plan

### Automated Tests
- Dùng `pytest` (nếu cần thiết sau này) để test các tầng Repository và Endpoints.

### Manual Verification
- Chạy server bằng: `cd backend && uvicorn app.main:app --reload`.
- Vào Swagger UI tại `http://localhost:8000/docs`. Kiểm tra xem mô tả và comment có chuẩn chỉnh không.
- Kiểm thử các API `/diagnosis` và `/consultation`.
- Đảm bảo database file (`clinic.db`) tự động sinh ra và được mồi dữ liệu mã ICD-10 đúng yêu cầu.
