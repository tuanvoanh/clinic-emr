# ClinicCare Mini EMR - FastAPI Backend Architecture & Implementation Guide

Tài liệu này mô tả chi tiết kiến trúc, quy chuẩn nghiệp vụ, thiết kế cơ sở dữ liệu, chiến lược Indexing và danh sách API của hệ thống Backend **ClinicCare Mini EMR**.

---

## 1. Kiến trúc hệ thống (Layered Architecture & Repository Pattern)

Dự án áp dụng mô hình phân tầng chặt chẽ của một hệ thống FastAPI chuẩn Enterprise:

```text
backend/
├── app/
│   ├── main.py                 # Khởi tạo FastAPI app, cấu hình CORS, đăng ký exception handlers & routes
│   ├── core/
│   │   ├── config.py           # Quản lý cấu hình & biến môi trường (Pydantic BaseSettings)
│   │   ├── database.py         # SQLAlchemy engine & SessionLocal factory
│   │   └── exceptions.py       # ErrorCode Enum (Single Source of Truth), AppException, Global Exception Handlers
│   ├── models/                 # SQLAlchemy 2.0 Models (Mapped & mapped_column)
│   │   ├── base.py             # Declarative Base
│   │   ├── patient.py          # Patient model (Unique B-Tree Index trên phone)
│   │   ├── diagnosis.py        # ICD10Code model
│   │   └── consultation.py     # Consultation model (Index trên FKs & created_at)
│   ├── schemas/                # Pydantic V2 Schemas (Strict Validations)
│   │   ├── patient.py          # PatientBase, PatientCreate, PatientResponse
│   │   ├── diagnosis.py        # ICD10CodeResponse
│   │   └── consultation.py     # ConsultationCreate, ConsultationResponse, PaginatedConsultationResponse
│   ├── repositories/           # Tầng truy vấn Database (Repository Pattern, cách ly logic SQL)
│   │   ├── patient.py          # CRUD & Prefix search by phone
│   │   ├── diagnosis.py        # Search ICD-10 codes
│   │   └── consultation.py     # Create & Paginated query with filters
│   ├── api/
│   │   ├── dependencies.py     # get_db dependency
│   │   ├── api_router.py       # Tổng hợp router các module
│   │   └── endpoints/
│   │       ├── patient.py      # Endpoints quản lý & tìm kiếm bệnh nhân
│   │       ├── diagnosis.py    # Endpoint tra cứu mã ICD-10
│   │       └── consultation.py # Endpoints tiếp nhận & lịch sử khám bệnh
│   └── db/
│       └── seed_icd10.py       # Script nạp 100 mã ICD-10 chuẩn
├── alembic/                    # Database Migrations (Alembic)
├── requirements.txt            # Danh sách dependencies
├── .env.example                # Mẫu biến môi trường
└── .gitignore                  # Cấu hình bỏ qua file nhạy cảm và database local
```

---

## 2. Quy chuẩn nghiệp vụ & Dữ liệu (Business Rules & Standards)

### 2.1. Định danh bệnh nhân duy nhất (Unique Identity)
* Bệnh nhân được định danh duy nhất qua **Số điện thoại (`phone`)**.
* Khi tạo hồ sơ khám (`POST /api/consultation`):
  1. Hệ thống tìm kiếm theo `phone` trong database.
  2. **Nếu đã tồn tại:** Tự động tái sử dụng `patient.id` của bệnh nhân đó.
  3. **Nếu chưa có:** Tạo mới bản ghi `Patient` với `phone` tương ứng.

### 2.2. Chuẩn số điện thoại di động Singapore (Unified Format)
* **Định dạng:** Đúng **8 chữ số**, bắt đầu bằng **`8`** hoặc **`9`**.
* **Biểu thức chính quy (Regex):** `^[89]\d{7}$` (VD: `81234567`, `98765432`).
* **Không lưu mã vùng (`+65`):** Vì toàn bộ Singapore dùng chung một mã vùng nội địa. Việc lưu số 8 chữ số thuần túy giúp tối ưu hóa B-Tree Index và tránh sai lệch dữ liệu.

---

## 3. Thiết kế Cơ sở dữ liệu & Chiến lược Indexing

Hệ thống được thiết kế để tối ưu hóa hiệu năng truy vấn, tránh hoàn toàn **Full Table Scan**:

| Bảng | Cột | Kiểu dữ liệu | Loại Index | Mục đích tối ưu |
| :--- | :--- | :--- | :--- | :--- |
| **`patients`** | `id` | `Integer` | **Primary Key** | Khóa chính, phục vụ JOIN. |
| **`patients`** | `phone` | `String` | **UNIQUE B-Tree Index** | Tra cứu $O(1)$ / $O(\log N)$, ngăn chặn trùng lặp. |
| **`patients`** | `full_name` | `String` | **B-Tree Index** | Tìm kiếm theo tên. |
| **`patients`** | `dob` | `String` | **B-Tree Index** | Lọc theo ngày sinh. |
| **`consultations`** | `id` | `Integer` | **Primary Key** | Khóa chính hồ sơ khám. |
| **`consultations`** | `patient_id` | `Integer` | **Foreign Key Index** | Tăng tốc độ phép `JOIN patients`. |
| **`consultations`** | `diagnosis_code` | `String` | **Foreign Key Index** | Tăng tốc độ phép `JOIN icd10_codes`. |
| **`consultations`** | `created_at` | `DateTime (UTC)` | **B-Tree Index** | Tối ưu phép sắp xếp `ORDER BY created_at DESC` (tránh Filesort). |
| **`icd10_codes`** | `code` | `String` | **Primary Key** | Tra cứu mã bệnh ICD-10. |

---

## 4. Chuẩn hóa Xử lý Lỗi (Enterprise Error Handling)

Hệ thống sử dụng **`ErrorCode` Enum** làm **Single Source of Truth** duy nhất trong [exceptions.py](file:///Users/tuananh/Documents/clinic-emr/backend/app/core/exceptions.py), loại bỏ hoàn toàn việc phân mảnh cấu hình sang file JSON.

### 4.1. Cấu trúc `ErrorCode` Enum:
Mỗi mã lỗi trong Enum tự động gắn liền với: `(code, default_message, default_status_code)`:
```python
class ErrorCode(Enum):
    VALIDATION_ERROR = ("validation_error", "Invalid input data.", 400)
    HTTP_ERROR = ("http_error", "HTTP request error.", 400)
    INTERNAL_SERVER_ERROR = ("internal_server_error", "Internal server error. Please try again later.", 500)
    INVALID_ICD10_CODE = ("invalid_icd10_code", "Invalid ICD-10 code or it does not exist in the system.", 400)
    PATIENT_NOT_FOUND = ("patient_not_found", "Patient not found.", 404)
```

### 4.2. Cấu trúc Response lỗi chuẩn:
Mọi lỗi (Validation, Business, HTTP, Internal Error) đều trả về format thống nhất:
```json
{
  "status": "error",
  "status_code": 400,
  "error_code": "invalid_icd10_code",
  "message": "Invalid ICD-10 code or it does not exist in the system.",
  "errors": []
}
```

* **Lỗi Validation Pydantic:** Trả về mã HTTP `400` với chi tiết từng trường bị lỗi trong mảng `errors`.
* **Lỗi Nghiệp vụ:** `raise AppException(ErrorCode.INVALID_ICD10_CODE)` $\rightarrow$ Tự động có autocomplete, type safety, không lo gõ sai chính tả.
* **Lỗi Hệ thống (500):** Bắt qua `global_exception_handler`, ghi log chi tiết và ẩn stack trace nhạy cảm với client.

---

## 5. Chi tiết danh sách API Endpoints

### 5.1. Nhóm Bệnh nhân (`/api/patient`)

#### 1. `GET /api/patient/?phone={prefix}&limit={n}`
* **Chức năng:** Tìm kiếm gợi ý / autocomplete bệnh nhân khi nhập đầu số điện thoại.
* **Quy tắc:** Bắt buộc nhập **tối thiểu 6 chữ số** (`pattern=r"^[89]\d{5,7}$"`).
* **Cơ chế SQL:** `WHERE phone LIKE '812345%' LIMIT 20` $\rightarrow$ Tận dụng **Index Range Scan**.

#### 2. `GET /api/patient/{phone}`
* **Chức năng:** Lấy thông tin chi tiết của 1 bệnh nhân theo đúng số điện thoại.
* **Quy tắc:** Validate đúng 8 chữ số (`Path(..., pattern=r"^[89]\d{7}$")`) trước khi query DB.
* **Cơ chế SQL:** `WHERE phone = '81234567' LIMIT 1` $\rightarrow$ Tận dụng **Unique Index Lookup**. Trả về `404` (`patient_not_found`) nếu không tồn tại.

---

### 5.2. Nhóm Chẩn đoán ICD-10 (`/api/diagnosis`)

#### 1. `GET /api/diagnosis/?search={keyword}`
* **Chức năng:** Tìm kiếm mã hoặc tên bệnh ICD-10. Trả về toàn bộ danh sách mã nếu không truyền `search`.

---

### 5.3. Nhóm Hồ sơ Khám bệnh (`/api/consultation`)

#### 1. `POST /api/consultation/`
* **Chức năng:** Tiếp nhận và tạo mới hồ sơ khám bệnh.
* **Request Body (`ConsultationCreate`):**
  ```json
  {
    "patient_name": "Tan Ah Kow",
    "dob": "1990-01-01",
    "phone": "81234567",
    "diagnosis_code": "A00.0",
    "treatment_notes": "Prescribed medicine and rest for 3 days."
  }
  ```
* **Luồng xử lý:**
  1. Kiểm tra tồn tại mã `diagnosis_code` trong bảng `icd10_codes` $\rightarrow$ Báo lỗi `invalid_icd10_code` nếu sai.
  2. Tìm kiếm `Patient` theo `phone` $\rightarrow$ Tái sử dụng `patient.id` hoặc tạo mới `Patient`.
  3. Tạo bản ghi `Consultation` gắn với `patient.id` và tự động sinh `created_at` (UTC).

#### 2. `GET /api/consultation/?phone={exact_phone}&diagnosis_code={code}&page={p}&page_size={s}`
* **Chức năng:** Lấy lịch sử khám bệnh có phân trang, lọc chính xác và sắp xếp thời gian mới nhất lên đầu (`created_at DESC`).
* **Query Parameters:**
  * `phone`: Lọc chính xác theo số điện thoại bệnh nhân (`pattern=r"^[89]\d{7}$"`).
  * `diagnosis_code`: Lọc chính xác theo mã ICD-10 (VD: `A00.0`).
  * `page`: Số thứ tự trang (mặc định: `1`).
  * `page_size`: Số bản ghi mỗi trang (mặc định: `10`, tối đa `100`).
* **Response Body (`PaginatedConsultationResponse`):**
  ```json
  {
    "items": [
      {
        "id": 1,
        "patient_id": 1,
        "full_name": "Tan Ah Kow",
        "dob": "1990-01-01",
        "phone": "81234567",
        "diagnosis_code": "A00.0",
        "diagnosis_desc": "Cholera due to Vibrio cholerae 01, biovar cholerae",
        "treatment_notes": "Prescribed medicine and rest.",
        "created_at": "2026-09-07T03:48:54.123456Z"
      }
    ],
    "total": 1,
    "page": 1,
    "page_size": 10,
    "total_pages": 1
  }
  ```

---

## 6. Kế hoạch Kiểm thử & Vận hành (Verification & Run)

### Khởi chạy Backend:
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Swagger UI & OpenAPI Documentation:
* **Interactive Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
* **OpenAPI Schema:** [http://127.0.0.1:8000/api/openapi.json](http://127.0.0.1:8000/api/openapi.json)
