# API Documentation: Accounting Foundation (Phase 1)

Tài liệu này cung cấp chi tiết các API mới thuộc phân hệ Kế toán (Accounting) để đội ngũ Frontend tích hợp. Các API này tập trung vào quản lý Hệ thống tài khoản (COA) và Bút toán (Journal Entries).

---

## 1. Tổng quan
- **Base Path**: `/api/accounting`
- **Authentication**: Yêu cầu Bearer Token (JWT).
- **Multi-tenancy**: Hệ thống tự động lọc dữ liệu theo `organizationId` của người dùng đang đăng nhập.

---

## 2. Hệ thống tài khoản (Chart of Accounts - COA)

### 2.1 Lấy danh sách tài khoản
Lấy toàn bộ danh sách tài khoản của tổ chức, sắp xếp theo mã tài khoản.

- **Endpoint**: `GET /accounts`
- **Response**: `AccountResponseDto[]`

**Example Response**:
```json
[
  {
    "id": 1,
    "code": "111",
    "name": "Tiền mặt",
    "type": "ASSET",
    "parentId": null,
    "path": "/",
    "isSystem": true,
    "isActive": true
  },
  {
    "id": 2,
    "code": "1111",
    "name": "Tiền Việt Nam",
    "type": "ASSET",
    "parentId": 1,
    "path": "/1/",
    "isSystem": false,
    "isActive": true
  }
]
```

### 2.2 Khởi tạo bộ tài khoản mẫu
Dùng để tạo nhanh các tài khoản cơ bản (Tiền mặt, Doanh thu, Chi phí...) cho một tổ chức mới.

- **Endpoint**: `POST /accounts/initialize`
- **Response**: 
```json
{ "message": "Đã khởi tạo hệ thống tài khoản mặc định" }
```

### 2.3 Tạo tài khoản mới
Tạo một tài khoản con hoặc tài khoản cấp 1 mới.

- **Endpoint**: `POST /accounts`
- **Body**:
```json
{
  "parentId": 1, 
  "code": "1112",
  "name": "Ngoại tệ",
  "type": "ASSET"
}
```
- **Lưu ý**: `parentId` có thể null nếu là tài khoản cấp 1. `type` phải thuộc: `ASSET`, `LIABILITY`, `EQUITY`, `REVENUE`, `EXPENSE`.

---

## 3. Nhật ký chung & Bút toán (General Ledger)

### 3.1 Tạo bút toán thủ công (Manual Journal Entry)
Ghi nhận một nghiệp vụ tài chính vào sổ nhật ký.

- **Endpoint**: `POST /journal-entries`
- **Body**:
```json
{
  "description": "Mua văn phòng phẩm bằng tiền mặt",
  "transactionDate": "2026-05-08T10:00:00Z",
  "items": [
    {
      "accountId": 8, 
      "debit": 500000,
      "credit": 0,
      "description": "Chi phí văn phòng phẩm"
    },
    {
      "accountId": 1,
      "debit": 0,
      "credit": 500000,
      "description": "Chi tiền mặt"
    }
  ]
}
```
- **Validation**: Tổng Nợ (`debit`) phải bằng Tổng Có (`credit`). Nếu không bằng, API sẽ trả về lỗi 400.

### 3.2 Ghi sổ chính thức (Post)
Sau khi tạo ở trạng thái `DRAFT`, bút toán cần được "Post" để chính thức ghi vào sổ cái.

- **Endpoint**: `PATCH /journal-entries/:id/post`
- **Response**: Trả về thông tin bút toán với `status: "POSTED"`.
- **Lưu ý**: Một khi đã Post, bút toán sẽ không thể sửa hoặc xóa trực tiếp (phải dùng bút toán đảo để điều chỉnh).

---

## 4. Tự động hóa từ Finote (Dành cho FE nắm luồng)

Hệ thống đã tích hợp sẵn luồng tự động:
1. Khi Kế toán gạch nợ thành công cho một Phiếu Thu/Chi (`Finote`) sang trạng thái `PAID`.
2. Hệ thống tự động sinh một **Bút toán Nháp (Draft Journal Entry)**.
3. Kế toán chỉ cần vào danh sách Bút toán, kiểm tra lại và nhấn **Post** để hoàn tất.

---

## 5. Danh mục Enums cho Frontend

### AccountType
- `ASSET`: Tài sản (Đầu 1, 2)
- `LIABILITY`: Nợ phải trả (Đầu 3)
- `EQUITY`: Vốn chủ sở hữu (Đầu 4)
- `REVENUE`: Doanh thu (Đầu 5, 7)
- `EXPENSE`: Chi phí (Đầu 6, 8, 9)

### JournalEntryStatus
- `DRAFT`: Bản nháp (Có thể sửa/xóa)
- `POSTED`: Đã ghi sổ (Khóa dữ liệu)
- `CANCELLED`: Đã hủy
