---
id: dom-crm-fix-lead-acquired-at
title: Sửa đổi hiển thị acquiredAt của Lead trong CRM
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on: []
summary: "Cập nhật API GET /crm/leads trả về acquiredAt thực tế từ DB thay vì fallback sang createdAt tại Backend, đồng bộ với LeadResponseDto và UI Kanban."
tags: [crm, lead, api-contract, dto, bug-fix]
---

### 1. Vấn đề kỹ thuật
- **Hiện tượng**: Thẻ Lead trên Kanban hiển thị trùng ngày tiếp nhận do API backend chưa trả về trường `acquiredAt` từ database, buộc Frontend phải fallback về `createdAt`.
- **Giải pháp**: Đồng bộ Domain Entity/Database Schema với DTO đầu ra của API để trả về đúng giá trị `acquiredAt`.

### 2. Thay đổi chi tiết
#### Backend (API & DTO)
- **Endpoints ảnh hưởng**: `GET /crm/leads` và `GET /crm/leads/:id`
- **Cập nhật `LeadResponseDto`**:
  - Thực hiện ánh xạ (mapping) chính xác trường `acquiredAt` từ database sang DTO đầu ra.
  - Kiểu dữ liệu: ISO Date String (`string | null`).

#### Frontend (UI & Contract)
- **Contract Zod** (`shared/contracts/crm.ts`): Đã định nghĩa sẵn `acquiredAt?: string`, giữ nguyên không đổi.
- **UI Component (`LeadKanbanBoard.tsx`)**: Giữ nguyên logic hiển thị `acquiredAt || createdAt`. Hệ thống sẽ tự động hiển thị ngày tiếp nhận thực tế ngay khi API trả về dữ liệu.

### 3. Kiểm thử & Rủi ro
- **Database**: Không thay đổi Schema hay Migrate DB.
- **API Test**: Xác nhận kết quả JSON trả về từ hai endpoints trên có chứa thuộc tính `acquiredAt` đúng định dạng ISO.