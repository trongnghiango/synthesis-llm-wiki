# Phân tích Nghiệp vụ Lập chứng từ và Bút toán Thủ công (Manual Entries)

## A. Mục đích & Bối cảnh

Trong hệ thống kế toán doanh nghiệp STAX, dòng tiền và nghiệp vụ kế toán được hạch toán qua 2 con đường:
1.  **Tự động (Automated):** Đồng bộ trực tiếp từ các sự kiện nghiệp vụ (như thu/chi từ các Phiếu thu, Phiếu chi - Finotes).
2.  **Thủ công (Manual):** Dành cho kế toán viên trực tiếp nhập tay các nghiệp vụ đặc thù như trích khấu hao tài sản, phân bổ chi phí trả trước, tính lương nhân viên hoặc điều chỉnh sai sót cuối kỳ.

**Vấn đề phát hiện:**
*   Các nút bấm `"Lập phiếu thu"` và `"Lập phiếu chi"` trên giao diện danh sách Phiếu thu/chi là các nút tĩnh, không hoạt động.
*   Nút bấm `"Thêm Bút toán mới"` trên giao diện Nhật ký chung cũng là nút tĩnh, không liên kết với Form định khoản đã viết sẵn.

**Giải pháp:**
Tích hợp và kích hoạt toàn bộ các luồng lập chứng từ thủ công và hạch toán thủ công trên Frontend để đảm bảo 100% chức năng kế toán hoạt động thông suốt.

---

## B. Yêu cầu Phi chức năng (NFR Check)

1.  **Tenant Isolation (Cô lập Dữ liệu):** 
    *   Mọi phiếu thu/chi và bút toán thủ công khi gửi lên Backend bắt buộc phải được tự động gán theo `organizationId` của User đang đăng nhập. Điều này được đảm bảo nhờ JWT Guard ở Backend và `CurrentUser()` decorator.
2.  **Định khoản Cân đối (Accounting Double-Entry balance):**
    *   Mọi bút toán thủ công phải đảm bảo tổng tiền ghi **Nợ (Debit) = Có (Credit)** trước khi bấm lưu. Luật này được kiểm soát chặt chẽ ở cả Frontend (Zod validation & UI indicator) và Backend (Domain Invariant `.validateBalance()`).

---

## C. Phạm vi tác động (Scope of Impact)

*   **Frontend Components & Pages:**
    *   Tạo mới: `CreateFinoteDialog` (`components/create-finote-dialog.tsx`).
    *   Sửa đổi: `FinotesPage` (`finotes.tsx`).
    *   Sửa đổi: `JournalEntriesPage` (`journal-entries.tsx`).
*   **Backend Contracts:**
    *   Sử dụng schema có sẵn: `createFinoteSchema` và `createJournalEntrySchema` từ shared contract `@shared/contracts/accounting`.
