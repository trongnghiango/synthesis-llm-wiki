# 🚀 HƯỚNG DẪN DÀNH CHO LẬP TRÌNH VIÊN (DEVELOPER GUIDE)

Chào mừng bạn gia nhập đội ngũ phát triển STAX. Tài liệu này giúp bạn bắt nhịp nhanh nhất với workflow của dự án.

## 1. THIẾT LẬP MÔI TRƯỜNG

*   **Runtime:** Node.js v18+ (Khuyến nghị v20).
*   **Package Manager:** `pnpm`.
*   **Database:** PostgreSQL 15+ (Local hoặc Docker).
*   **Environment:** Sao chép `.env.example` thành `.env` và cấu hình các thông số kết nối.

---

## 2. WORKFLOW PHÁT TRIỂN MODULE MỚI

Để tạo một module mới tuân thủ Clean Architecture, hãy sử dụng script tự động:

```bash
python3 generate_module.py [tên-module]
```

Script này sẽ tạo sẵn cấu trúc thư mục: `domain`, `application`, `infrastructure`, `presentation` cùng với các file boilerplate chuẩn mực.

---

## 3. KIỂM THỬ (TESTING)

Chúng ta coi trọng Integration Test để đảm bảo SQL chạy đúng.

*   **Chạy toàn bộ test:** `npm run test`
*   **Test Repository:** Sử dụng `test-db.helper.ts` để khởi tạo PGLite. 
*   **Lưu ý:** Nếu gặp lỗi liên quan đến WASM hoặc Import, hãy đảm bảo chạy với flag `--experimental-vm-modules`.

---

## 4. QUẢN TRỊ DATABASE (DRIZZLE KIT)

*   **Generate Migration:** `npx drizzle-kit generate`
*   **Apply Migration:** `npx drizzle-kit migrate` (Yêu cầu TTY).
*   **Quick Fix:** Nếu bạn đang ở trong môi trường hạn chế (như Web Agent), hãy sử dụng:
    ```bash
    npx ts-node src/database/quick-fix.ts
    ```
    *Script này cho phép áp dụng SQL trực tiếp mà không cần tương tác dòng lệnh.*

---

## 5. CÔNG CỤ HỖ TRỢ (CLI TOOLS)

*   **Seeding:** `npx ts-node src/modules/test/seeders/database.seeder.ts`
*   **Migration Legacy:** Sử dụng các script trong `src/modules/test/` để di cư dữ liệu từ file Excel/CSV cũ của STAX vào hệ thống mới.
*   **Check Constraints:** `npx ts-node src/database/check-constraints.ts` để kiểm tra các ràng buộc DB đang có.

---

## 6. QUY TRÌNH PULL REQUEST (PR)

1.  Đảm bảo code đã qua `npx tsc --noEmit` (Không lỗi Type).
2.  Đảm bảo đã chạy `npm run lint`.
3.  Mô tả rõ ràng các thay đổi về Schema (nếu có) trong PR.

---
*Cập nhật ngày 08/05/2026 bởi Antigravity AI.*
