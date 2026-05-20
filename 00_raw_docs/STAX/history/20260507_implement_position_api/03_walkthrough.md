# Walkthrough - Implement Position API

Tôi đã hoàn thành việc triển khai API lấy danh sách vị trí theo Phòng ban (`GET /api/org-structure/positions?orgUnitId=...`).

## Các thay đổi chính:

1.  **Domain & Repository**:
    *   Bổ sung phương thức `findPositionsByOrgUnitId` vào `IOrgStructureRepository`.
    *   Thực thi query trong `DrizzleOrgStructureRepository` để lấy dữ liệu từ bảng `positions`.

2.  **Application Service**:
    *   Thêm phương thức `getPositionsByOrgUnit` vào `OrgStructureService` để kết nối Controller và Repository.

3.  **Infrastructure & API**:
    *   Tạo `PositionResponseDto` để chuẩn hóa dữ liệu trả về (bao gồm các trường: id, code, name, orgUnitId, jobTitleId, gradeId, headcountLimit, isActive).
    *   Mở endpoint `GET /org-structure/positions` trong `OrgStructureController`.
    *   Áp dụng Permission Guard `org:read` để đảm bảo an toàn.

## Kết quả:
Frontend hiện có thể gọi API: `GET /api/org-structure/positions?orgUnitId=527` để lấy danh sách các vị trí định biên của phòng ban có ID 527.
