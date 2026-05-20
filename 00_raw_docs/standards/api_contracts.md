---
title: "Tiêu chuẩn Hợp đồng API"
description: "Quy chuẩn thiết kế API Contracts & Integration giữa Frontend và Backend"
tags: [standards, api, contracts, integration]
last_updated: "2026-05-21"
---

# Tiêu chuẩn Hợp đồng API (API Contracts & Integration)

Tài liệu này là cầu nối giao tiếp giữa Frontend (FE) và Backend (BE). Mục tiêu là biến `shared/contracts` thành "Nguồn sự thật duy nhất" (Single Source of Truth) để tránh việc phải đọc code mới hiểu API.

## 1. Triết lý Contract-First
- **Không đoán mò**: Cả FE và BE đều làm việc dựa trên các Schema được định nghĩa trong `shared/contracts`.
- **Zod là tài liệu**: Các Zod schema trong thư mục `shared/` chính là tài liệu mô tả chính xác nhất dữ liệu đầu vào/đầu ra.

## 2. Tiêu chuẩn Giao tiếp (Communication Standards)

### A. Định dạng Phản hồi (Standard Response)
Mọi API nên tuân thủ cấu trúc:
- **Thành công (2xx)**: Trả về dữ liệu trực tiếp hoặc bọc trong object (nếu có phân trang).
- **Lỗi (4xx, 5xx)**:
  ```json
  {
    "message": "Thông báo lỗi thân thiện",
    "code": "ERROR_CODE_DUNG_CHO_LOGIC_FE",
    "errors": [] // Chi tiết lỗi (nếu có validation)
  }
  ```

### B. Sử dụng HTTP Methods
- `GET`: Lấy dữ liệu (Không thay đổi trạng thái).
- `POST`: Tạo mới.
- `PUT/PATCH`: Cập nhật.
- `DELETE`: Xóa.

## 3. Quy trình Đề xuất API mới (API Proposal Workflow)

Khi Frontend thiếu API hoặc cần thay đổi cấu trúc dữ liệu, hãy thực hiện các bước sau thay vì viết code tạm:

1. **Khởi tạo Proposal**: Tạo một section mới trong mục **[Danh sách Đề xuất API](#4-danh-sach-de-xuat-api-proposals)** hoặc trong tệp `01_implementation_plan.md` của task tương ứng.
2. **Định nghĩa Hợp đồng**:
   - `Endpoint`: (Ví dụ: `POST /api/crm/leads/bulk-assign`)
   - `Purpose`: (Lý do cần API này)
   - `Request Body`: (Schema dự kiến)
   - `Response Body`: (Dữ liệu FE mong muốn nhận được)
3. **Review**: Gửi link tài liệu cho Backend team để thống nhất trước khi code.

## 4. Danh sách Đề xuất API (Proposals)
*(Phần này dùng để lưu trữ các yêu cầu API đang chờ thảo luận)*

- **[Chưa có đề xuất nào hiện hành]**

---
*Ghi chú: Sau khi BE đồng ý, hãy đưa schema chính thức vào `shared/contracts`.*
