# Research & Analysis: Hệ thống Quản lý Công việc STAX

Dựa trên việc phân tích các ứng dụng hàng đầu (Linear, Asana, Monday.com), chúng ta sẽ xây dựng module Task cho STAX theo các tiêu chuẩn sau:

## 1. Cảm hứng thiết kế (Inspiration)
- **Linear**: Tối giản, tập trung vào hiệu suất (Performance), bỏ qua các chi tiết thừa.
- **Monday.com**: Màu sắc trực quan, trạng thái công việc rõ ràng.
- **Notion**: Sự linh hoạt trong việc tổ chức thông tin.

## 2. Các nguyên tắc trải nghiệm (UX Principles)
- **Single Source of Truth**: Mọi công việc đều được quản lý tập trung nhưng có thể truy cập từ nhiều nơi (Profile nhân viên, Sơ đồ tổ chức).
- **Speed First**: Thao tác tạo và cập nhật trạng thái phải diễn ra trong tích tắc (< 1s).
- **Visual Feedback**: Khi hoàn thành công việc, người dùng phải nhận được sự "thỏa mãn" về mặt thị giác (Micro-interactions).

## 3. Cấu trúc chức năng (Functional Structure)
- **Smart Inbox**: Nơi chứa các task mới được giao hoặc cần xử lý gấp.
- **Views**: 
    - **List View**: Dành cho quản lý số lượng lớn.
    - **Board View**: Dành cho theo dõi luồng công việc (Todo, In Progress, Done).
- **Task Detail (Drawer)**: Xem chi tiết task mà không rời khỏi màn hình hiện tại.

## 4. Công nghệ sử dụng
- **Framer Motion**: Cho các hiệu ứng chuyển động cao cấp.
- **Lucide React**: Bộ icon hiện đại, mảnh dẻ.
- **Vanilla CSS + Tailwind**: Tạo các gradient và hiệu ứng Blur (Glassmorphism).
