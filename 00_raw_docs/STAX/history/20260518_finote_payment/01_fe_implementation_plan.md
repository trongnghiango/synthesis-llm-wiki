# Kế hoạch Kiến trúc Chi tiết Frontend: Finote Payment

**A. Contract Sync**
- Đồng bộ `accounting.ts` từ Backend về `frontend/shared/contracts/`. Dùng `RecordFinotePaymentSchema` để làm validation form.

**B. API Client**
- Tạo mutation `useRecordFinotePayment` trong file API hook của accounting.
- Gọi Endpoint: `POST /api/accounting/finotes/:id/payments`.
- On success: `queryClient.invalidateQueries({ queryKey: ["finotes"] })` và detail.

**C. Component Tree**
- Component: `RecordPaymentDialog.tsx` (Chứa form, nhận `finoteId` và `missingAmount`).
- Trang `FinoteListPage.tsx`: Thêm action button vào DataGrid (chỉ hiện khi `_actions.recordPayment.allowed === true`).
- Trang `FinoteDetailPage.tsx`: Render bảng Payment History. Thêm nút trigger Dialog.

**D. State Management**
- `react-hook-form` xử lý nội bộ Form.
- Không dùng Zustand cho form này.
- `RecordPaymentDialog` dùng state boolean local `isOpen` hoặc nhận state open từ component cha.
