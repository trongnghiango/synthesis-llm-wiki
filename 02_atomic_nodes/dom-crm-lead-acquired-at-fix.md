---
id: dom-crm-lead-acquired-at-fix
title: Sửa lỗi hiển thị ngày tiếp nhận Lead
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on: []
summary: "Đồng bộ LeadResponseDto để trả về thuộc tính acquiredAt thực tế từ Database cho các API Leads."
tags: [crm, lead, dto, api-contract, bug-fix]
---

## 1. Vấn đề & Mục tiêu
- **Vấn đề**: Thẻ Kanban CRM hiển thị sai ngày tiếp nhận thực tế do API không trả về `acquiredAt`, dẫn đến UI phải fallback về ngày tạo hệ thống (`createdAt`).
- **Mục tiêu**: Cập nhật API để trả về chính xác giá trị `acquiredAt` định dạng ISO String từ DB, giúp `LeadKanbanBoard.tsx` hiển thị đúng tiến trình.

## 2. Thay đổi Kỹ thuật
### Backend
- **Endpoints ảnh hưởng**: `GET /crm/leads` và `GET /crm/leads/:id`.
- **Data Transfer Object (DTO)**: Cập nhật `LeadResponseDto` để đồng bộ và ánh xạ chính xác trường `acquiredAt` từ Domain Entity / Database Schema sang JSON Payload.
- **Database**: Không thay đổi schema. Thực thể `Lead` trong DB đã có sẵn trường `acquiredAt` (Timestamp).

### Frontend & API Contract
- **API Contract**: `shared/contracts/crm.ts` (đã có sẵn định nghĩa `acquiredAt?: string`, giữ nguyên).
- **Frontend**: Component `LeadKanbanBoard.tsx` tự động nhận diện trường `acquiredAt` mới bổ sung từ API payload. Giữ nguyên cơ chế fallback `acquiredAt || createdAt` trên UI để tương thích ngược với dữ liệu cũ thiếu `acquiredAt`.

## 3. Cấu trúc Payload Kỳ vọng
```json
{
  "id": "lead_01j7y...",
  "name": "Khách hàng tiềm năng A",
  "acquiredAt": "2026-05-20T08:30:00.000Z",
  "createdAt": "2026-05-19T02:15:00.000Z"
}
```