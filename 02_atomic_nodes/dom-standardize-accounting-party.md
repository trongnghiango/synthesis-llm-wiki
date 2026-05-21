---
id: dom-standardize-accounting-party
title: Chuẩn hóa Đối tượng Kế toán (Accounting Party)
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[dom-accounting-finote]]"
  - "[[arch-als-tenant-isolation]]"
summary: Chuẩn hóa thông tin Đối tượng Kế toán (Party) trực tiếp trong finotes phục vụ cách ly Tenant và hiển thị tối ưu không cần JOIN.
tags: [accounting, database-schema, domain-entity, tenant-isolation]
---

## 1. Cấu trúc Database Schema (`finotes.schema.ts`)
Bổ sung các trường lưu trữ phẳng trực tiếp vào bảng `finotes` nhằm tối ưu truy vấn:
- `tenantId` (UUID): Đảm bảo cách ly dữ liệu đơn vị sở hữu.
- `organizationId` (UUID, nullable): Liên kết đối tác tổ chức.
- `employeeId` (UUID, nullable): Liên kết nhân viên nội bộ.
- `partyName` (varchar): Tên đối tượng hiển thị trực tiếp.
- `partyType` (varchar): Phân loại đối tượng (`ORGANIZATION` | `EMPLOYEE`).

## 2. Ràng buộc Domain & Application Layer
- **Domain (`finote.entity.ts`)**: Tích hợp interface `FinoteParty`. Áp dụng Business Rule chặn tạo phiếu kế toán nếu thuộc tính `party.name` bị bỏ trống.
- **Service (`finote.service.ts`)**: Tự động truy vấn và ánh xạ `partyName`, `partyType` từ database khi tạo phiếu để đảm bảo tính nhất quán dữ liệu.
- **DTO (`finote-response.dto.ts`)**: Chuẩn hóa định dạng xuất dữ liệu:
  ```typescript
  party: { id: string | null; name: string; type: 'ORGANIZATION' | 'EMPLOYEE' }
  ```

## 3. API Contract (`GET /accounting/finotes`)
Cấu trúc JSON phản hồi chuẩn hóa thông tin đối tượng:
```json
{
  "id": 123,
  "code": "INC-2026-0001",
  "party": {
    "id": 101,
    "name": "Công ty TNHH STAX",
    "type": "ORGANIZATION"
  }
}
```
*Hướng dẫn Frontend:* Sử dụng trường `party.type` để mapping Icon tương ứng (ví dụ: `Building` cho tổ chức, `User` cho nhân viên) và `party.name` làm nhãn hiển thị trực tiếp trên UI.