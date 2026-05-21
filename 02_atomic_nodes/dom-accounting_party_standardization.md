---
id: dom-accounting_party_standardization
title: Chuẩn hóa Đối tượng Kế toán
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[dom-accounting-finote]]"
summary: "Chuẩn hóa cấu trúc Đối tượng (Party) trong Finote nhằm phân định Tenant và Partner, tối ưu hóa DB Schema và API response."
tags: [accounting, database-schema, domain-entity, api-contract]
---

## 1. Nghiệp vụ & Quy tắc thiết kế
- **Mục tiêu**: Phân tách rõ ràng giữa Chủ thể sở hữu đơn vị (`tenantId` - cô lập dữ liệu theo `[[arch-tenant-isolation]]`) và Đối tượng giao dịch (`party`).
- **Business Rule**: Cấm tạo/lưu phiếu kế toán (`Finote`) nếu thiếu thông tin tên đối tượng (`party.name`).

## 2. Thay đổi Kỹ thuật

### A. Database Schema (`finotes.schema.ts`)
- `tenantId`: Khóa ngoại/trường định danh cô lập dữ liệu đa thuê.
- `organizationId` / `employeeId`: Khóa ngoại liên kết tới thực thể đối tác tương ứng.
- `partyName`, `partyType` (`ORGANIZATION` | `EMPLOYEE`): Khử chuẩn hóa (denormalize) trực tiếp vào bảng `finotes` để tăng hiệu năng truy vấn, tránh JOIN.

### B. Domain & Application Layer
- **`finote.entity.ts`**: Tích hợp interface `FinoteParty` vào thực thể lõi.
- **`finote.service.ts`**: Tự động phân giải (resolve) `partyName` và `partyType` từ database khi tạo phiếu để đảm bảo tính toàn vẹn dữ liệu từ Backend.

### C. API Contract (`FinoteResponseDto`)
- Endpoint trả về cấu trúc DTO chuẩn hóa:
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

## 3. Tham chiếu chéo
- Thực thể nghiệp vụ gốc: `[[dom-accounting-finote]]`
- Cơ chế cô lập dữ liệu: `[[arch-tenant-isolation]]`