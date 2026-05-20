# Bước 3: Checklist Thực thi — Frontend Service Catalog

## 🏗️ Nền tảng & Data
- [ ] 1. Định nghĩa Zod Schema và TypeScript Types cho `Service`.
- [ ] 2. Viết API hooks (`useServices`, `useCreateService`, `useUpdateService`) sử dụng TanStack Query.

## 🧱 Component Core
- [ ] 3. Xây dựng `ServicePicker` sử dụng Popover + Command (Shadcn/UI).
- [ ] 4. Đảm bảo `ServicePicker` có tính năng search và auto-complete mượt mà.

## 🖥️ Trang Quản lý (Admin)
- [ ] 5. Tạo trang `/admin/crm/services` hiển thị danh mục dịch vụ.
- [ ] 6. Tích hợp Dialog tạo/sửa dịch vụ cho Admin.

## 🔗 Tích hợp Form (Quan trọng)
- [ ] 7. **QuoteForm:** Thay thế input Description bằng `ServicePicker`. Tích hợp logic auto-fill Price.
- [ ] 8. **ContractDraft:** Hiển thị danh sách items (Service Catalog) thay vì chỉ một field `Value` tổng.
- [ ] 9. **FinoteForm:** Bổ sung field chọn dịch vụ liên quan để tracking chi phí.

## 🧪 Kiểm tra & Đánh giá UX
- [ ] 10. Kiểm tra luồng tạo Quote từ Lead: Chọn dịch vụ -> Giá tự nhảy -> Tính tổng tiền.
- [ ] 11. Kiểm tra tính responsive của bảng quản lý dịch vụ.
- [ ] 12. Tối ưu micro-interactions (Loading states, Error toasts).

---
Bạn đã sẵn sàng để tôi bắt đầu viết CODE chưa?
