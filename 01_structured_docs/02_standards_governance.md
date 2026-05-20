# 🏰 TIÊU CHUẨN & QUY TẮC QUẢN TRỊ (STANDARDS & GOVERNANCE)

Hệ thống STAX áp dụng các quy chuẩn quản trị và lập trình nghiêm ngặt dưới đây nhằm đảm bảo tính nhất quán tuyệt đối của mã nguồn qua nhiều thế hệ lập trình viên và AI Agents.

---

## 1. QUY ƯỚC ĐẶT TÊN (NAMING CONVENTIONS)

Quy ước đặt tên đồng bộ từ CSDL, Backend lên Frontend giúp AI và Dev tra cứu cực nhanh:

### 1.1) Đặt tên File & Folder
*   **Module folder:** Chữ thường, phân tách bằng dấu gạch ngang (kebab-case) (e.g., `org-structure`, `cash-book`).
*   **File name:** Định dạng `[name].[type].ts` (kebab-case) nhằm phản ánh rõ phân tầng kiến trúc:
    *   Entity: `session.entity.ts`
    *   Repository Port: `session.repository.ts`
    *   Use Case: `create-session.usecase.ts`
    *   Controller: `session.controller.ts`
    *   DTO: `create-session.dto.ts`
    *   DB Schema: `sessions.schema.ts`

### 1.2) Đặt tên biến, hàm và lớp
*   **Class/Interface/Type:** Định dạng PascalCase (e.g., `OrgStructureService`, `CreateEmployeeDto`).
*   **Biến & Hàm:** Định dạng camelCase (e.g., `organizationId`, `isExpired()`).
*   **Database Table:** Định dạng snake_case số nhiều (e.g., `organizations`, `employees`).
*   **Database Column:** Định dạng snake_case chữ thường (e.g., `organization_id`, `created_at`).

### 1.3) Tiêu chuẩn đặt tên ID đặc biệt
Để bảo toàn tính toàn vẹn định danh của nghiệp vụ, hậu tố `Id` bắt buộc phải được định nghĩa đúng ngữ cảnh:
*   `organizationId`: Ranh giới phân tách đa doanh nghiệp (Multi-tenancy).
*   `userId`: Định danh đăng nhập tài khoản hệ thống.
*   `employeeId`: Định danh nhân sự nội bộ (HRM Context).
*   `contactId`: Định danh đại diện khách hàng (CRM Context).
*   `actorId`: Mã định danh người thực hiện hành động (Audit Context).

---

## 2. RANH GIỚI NHẬP KHẨU (IMPORT BOUNDARIES)

Việc quản lý ranh giới import giữa các module là bắt buộc để ngăn ngừa việc cấu trúc hóa bị phá vỡ:

```
┌────────────────┐          ┌────────────────┐
│   Module CRM   │ ◄──X───► │   Module HRM   │
└───────┬────────┘          └───────┬────────┘
        │                           │
        ▼ (Public API only)         ▼ (Public API only)
    `index.ts`                  `index.ts`
```

### 🚨 Quy tắc ranh giới bất biến (Strict Import Boundary Rules)
1.  **Cấm import sâu (Deep Import Prohibition):** Tuyệt đối không được import trực tiếp vào sâu bên trong thư mục con của module khác.
    *   *Sai:* `import { Employee } from '../../hrm/domain/entities/employee.entity'`
    *   *Đúng:* `import { Employee } from '@modules/hrm'`
2.  **Cổng công khai (Public API):** Mỗi module bắt buộc phải có một tệp `index.ts` ở root làm cổng xuất khẩu duy nhất (Public API Gateway). Tất cả các lớp bên ngoài muốn sử dụng tài nguyên của module phải đi qua cổng này.
3.  **Khối `shared/` biệt lập:** Các thư mục nằm trong `shared/` (ví dụ `shared/contracts/`) chỉ chứa các kiểu dữ liệu, hằng số kỹ thuật và validator thô. Tuyệt đối **không** được đưa các logic nghiệp vụ (Business Logic) nặng vào đây.

---

## 3. HỢP ĐỒNG API DÙNG CHUNG (API CONTRACTS)

Mọi giao tiếp và kiểm soát dữ liệu giữa Backend (BE) và Frontend (FE) phải được định nghĩa qua một hợp đồng thống nhất:

*   **Contract-Driven Development:** Sử dụng thư viện validation như **Zod** để viết các schema dữ liệu dùng chung tại `shared/contracts/`.
*   **Single Source of Truth:** Cả BE và FE đều import từ `shared/contracts` để validate request/response, đảm bảo không lệch pha dữ liệu khi hệ thống cập nhật.
*   **Cấu trúc Phản hồi chuẩn (Standard Envelope):**
    ```typescript
    {
      success: boolean;
      data: T;
      error?: {
        code: string;
        message: string;
        details?: Record<string, any>;
      }
    }
    ```

---

## 4. QUY TRÌNH PHÁT TRIỂN & ARCHIVE (TEAM WORKFLOW)

Để đảm bảo lịch sử mã nguồn và tài liệu đồng hành đồng bộ, mọi đầu việc triển khai (Task) phải tuân thủ quy trình 4 bước lưu vết:

1.  **Bước 1 - Business Analysis (`00_analysis.md`):** Phân tích rõ bài toán nghiệp vụ, từ vựng Ubiquitous Language và các ca sử dụng (Use Cases).
2.  **Bước 2 - Architecture Design (`01_implementation_plan.md`):** Thiết kế cấu trúc database schema, API contracts và phân bổ lớp (Clean Arch).
3.  **Bước 3 - Tasks Checklist (`02_tasks.md`):** Phân rã công việc thành các checklist cụ thể trước khi lập trình.
4.  **Bước 4 - Walkthrough (`03_walkthrough.md`):** Ghi chép chi tiết kết quả chạy thử nghiệm thực tế (manual/automated test).

### 🕰️ Quy trình đóng băng lịch sử (History Archiving)
Sau khi tính năng hoàn tất và được merged thành công vào `main`:
*   Toàn bộ folder chứa 4 bước trên sẽ được di chuyển vào `docs/STAX/history/{YYYYMMDD}_{slug}/` làm tài liệu lưu trữ bất biến.
*   Không chỉnh sửa các tài liệu trong `history/`. Bất kỳ thay đổi nào tiếp theo phải tạo một context lịch sử mới.

---
*Tiêu chuẩn này cấu thành Hiến pháp lập trình tối cao của STAX.*
