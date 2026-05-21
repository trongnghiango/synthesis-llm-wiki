---
id: dom-fix_lead_acquired_at_display
title: Sửa lỗi hiển thị ngày tiếp nhận Lead (acquiredAt) trên Kanban
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[dom-crm-leads]]"
summary: "Đồng bộ LeadResponseDto để trả về đúng trường dữ liệu acquiredAt từ database, khắc phục lỗi hiển thị trùng ngày tạo trên UI Kanban."
tags: [crm, lead, acquired-at, dto, api]
---

## 1. Bối cảnh & Vấn đề
- API `GET /crm/leads` và `GET /crm/leads/:id` chưa trả về đúng trường `acquiredAt` của Lead Entity.
- UI Kanban (`LeadKanbanBoard.tsx`) phải fallback về `createdAt`, gây hiện tượng hiển thị trùng lắp ngày khởi tạo hệ thống thay vì ngày tiếp nhận thực tế.

## 2. Giải pháp Kỹ thuật
- **DTO Update**: Cập nhật `LeadResponseDto` để đồng bộ và map thuộc tính `acquiredAt` (ISO string) từ Domain Entity sang API Response.
- **API Contract**: Không đổi. File contract `shared/contracts/crm.ts` đã định nghĩa sẵn `acquiredAt?: string`.
- **Database**: Không thay đổi Schema. Dữ liệu thực tế lấy trực tiếp từ cột `acquired_at` của bảng `leads`.
- **Data Flow**: `DB (leads.acquired_at)` -> `Domain Entity (Lead)` -> `LeadResponseDto` -> `Frontend (LeadKanbanBoard.tsx)`.

## 3. Tác động & Tương thích
- **Database/Migration**: Không có.
- **Tương thích ngược (Backward Compatibility)**: Hoàn toàn tương thích do Frontend đã có sẵn logic xử lý `acquiredAt || createdAt`.