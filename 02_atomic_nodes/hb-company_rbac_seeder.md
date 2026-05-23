---
id: hb-company_rbac_seeder
title: Đồng bộ Cơ cấu Doanh nghiệp & RBAC Seeder
layer: 3-atomic
parent: "[[03_technical_handbooks]]"
depends_on:
  - "[[hb-drizzle-base-repo]]"
summary: "Đồng bộ hóa nhân sự, định biên vị trí và kế thừa quyền RBAC qua CLI seeder với cơ chế Smart Upsert."
tags: [seeder, rbac, employee-sync, metadata-jsonb, nestjs]
---

# Cơ chế Đồng bộ Doanh nghiệp & RBAC Seeder

## 1. Tối ưu hóa Khởi động & Parsing CSV
- **Boot Bypass:** Cấu hình `RUN_SEEDS=false` tại thời điểm khởi động NestJS để tối ưu tài nguyên, chuyển toàn bộ quyền seed sang CLI `seed:company`.
- **Index-based Mapping:** Sử dụng chỉ số mảng cố định (`row[index]`) thay vì tên cột để tránh sai lệch cấu trúc khi import dữ liệu hành chính phức tạp.

## 2. Kế thừa Quyền RBAC & Định biên
- **RBAC Inheritance:** Tự động hóa ánh xạ kế thừa quyền: `SUPER_ADMIN -> ADMIN`, `STAFF -> SPECIALIST / ASSISTANT`.
- **Ma trận Định biên (Positions):** Tự động hóa cấu trúc phòng ban (cập nhật cây `path`), liên kết động với chức danh (`job_titles`), cấp bậc (`grades`), địa điểm (`locations`), và giới hạn headcount.

## 3. Logic Smart Upsert (Non-destructive)
- **Định danh:** Dựa trên `employeeCode`.
- **Trùng khớp:** Giữ nguyên `userId`, `username`, và `email` hiện tại để bảo toàn phiên làm việc và bảo mật.
- **Tạo mới:** Tự động sinh `username` không trùng lặp thông qua cơ chế kiểm tra xung đột DB tuần tự (`username`, `username2`, ...).
- **JSONB Metadata Schema:**
  ```typescript
  interface EmployeeMetadata {
    bank: { bankName: string; accountNumber: string };
    idCard: { number: string; issueDate: string; issuePlace: string };
    insurance: { hospital: string; bookNumber: string };
    maritalStatus: string;
    emergencyContact: { fullName?: string; phoneNumber?: string; relationship?: string };
    permanentAddress: string;
    temporaryAddress?: string;
  }
  ```

## 4. Trạng thái Kiểm thử
- Tương thích 100% với hệ thống kiểm thử hiện tại: 46 test suites (234 test cases) passed thành công.