```yaml
---
id: dom-position-crud
title: Triển khai CRUD Position (Cơ cấu tổ chức)
layer: 3-atomic
parent: "[[04_domain_knowledge]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
summary: "Đặc tả nghiệp vụ và kỹ thuật triển khai CRUD thực thể Position (Vị trí) tích hợp Drizzle ORM."
tags: [org-structure, position, crud, drizzle-orm, api-design]
---

## 1. Nghiệp Vụ & Constraints
- **Tạo mới (`POST`):** Kiểm tra trùng lặp `code`. Xác thực sự tồn tại ngoại quan của `orgUnitId`, `jobTitleId`, và `gradeId`.
- **Cập nhật (`PATCH`):** Hỗ trợ cập nhật từng phần (partial update) thông tin vị trí.
- **Xóa (`DELETE`):** Cơ chế bảo vệ nghiêm ngặt. Chặn xóa (trả về lỗi nghiệp vụ) nếu vị trí đang được gán cho nhân sự (`isPositionInUse` trả về `true`).

## 2. API Contracts
- `POST /api/org-structure/positions`: Tạo mới Vị trí. Payload: `PositionRequestDto`.
- `PATCH /api/org-structure/positions/:id`: Cập nhật thông tin. Payload: `Partial<PositionRequestDto>`.
- `DELETE /api/org-structure/positions/:id`: Xóa vị trí (nếu không có nhân sự đảm nhiệm).

## 3. Kiến Trúc Triển Khai
- **Repository Layer:** 
  - Giao diện `IOrgStructureRepository` được bổ sung: `updatePosition`, `deletePosition`, `isPositionInUse`, `findGradeById`, `findJobTitleById`.
  - Thực thi cụ thể tại `DrizzleOrgStructureRepository` sử dụng Drizzle ORM.
- **Application Layer:** 
  - Tách biệt dữ liệu với `PositionDto` nhằm đảm bảo tính Agnostic (độc lập với Database Schema).
  - Điều phối logic nghiệp vụ trong `OrgStructureService`.
- **Testing:** Unit test bao phủ các kịch bản trùng mã code và chặn xóa khi vị trí đang hoạt động (8/8 test cases Passed).
```