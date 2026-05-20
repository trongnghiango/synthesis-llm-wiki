# Implementation Plan: Finote Detail API

## A. Database & Schema
- Không thay đổi Schema.
- Câu query sẽ sử dụng `leftJoin` với bảng `attachments` để lấy danh sách tệp đính kèm liên quan (`entity_type = 'finote'`).

## B. Domain Layer
- Sử dụng các thực thể hiện có: `Finote`, `Attachment`.
- Đảm bảo logic nghiệp vụ kiểm tra trạng thái (`canApprove()`, `canReject()`, v.v.) được đóng gói trong Entity nếu cần, hoặc xử lý tại Service dựa trên quy tắc STAX.

## C. Application Layer
- **FinoteService.getById(id: number, orgId: number, roles: string[]):**
    - Tìm kiếm Finote qua Repository.
    - **Security:** Nếu không tìm thấy hoặc `finote.sourceOrgId !== orgId`, ném `EntityNotFoundException` (để tránh lộ thông tin tồn tại của bản ghi thuộc Org khác).
    - **Action Logic:**
        - `approve`/`reject`: Chỉ xuất hiện nếu trạng thái là `PENDING` VÀ user có role `admin` hoặc `manager`.
        - `pay`: Chỉ xuất hiện nếu trạng thái là `APPROVED` VÀ user có quyền kế toán.
        - `edit`: Chỉ xuất hiện nếu trạng thái là `PENDING` hoặc `REJECTED`.

## D. API Contracts
- **Endpoint:** `GET /api/accounting/finotes/:id`
- **Controller:** `FinoteController.getFinoteDetail`
- **Response DTO:** `FinoteResponseDto` mở rộng:
    ```json
    {
      "id": 368,
      "code": "INC-2026-0003",
      "status": "PENDING",
      "attachments": [...],
      "_actions": ["approve", "reject", "edit"],
      "_metadata": {
          "canDelete": false
      }
    }
    ```

## E. Testing Strategy
- **Unit Test (Service):**
    - Test truy cập hợp lệ (cùng Org).
    - Test truy cập trái phép (khác Org) -> Phải ném lỗi.
    - Test logic sinh `_actions` cho các vai trò khác nhau (Manager vs Staff).
- **Integration Test (Repo):** Kiểm tra câu lệnh Join Attachments.

## F. Decision Log
- **Tại sao trả về Attachments trong Detail?** Để giảm Round-trip request. Trang Detail thường yêu cầu hiển thị đầy đủ thông tin ngay lập tức.
- **Tại sao tính _actions ở Backend?** Để đảm bảo tính chính xác của Business Rule và bảo mật (Server-Driven UI). Frontend chỉ việc render nút dựa trên mảng này.
