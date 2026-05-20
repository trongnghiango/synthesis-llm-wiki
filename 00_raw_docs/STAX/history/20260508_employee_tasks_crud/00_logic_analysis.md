# Phân tích Logic: Quản lý Công việc Nhân viên (Employee Tasks)

## 1. Cảm hứng thiết kế (Design Inspiration)

Để đạt được sự "hiện đại" và "đơn giản" như yêu cầu, chúng ta sẽ chắt lọc những tinh hoa từ các ứng dụng hàng đầu:

- **Linear Style (Minimalism & Focus)**: 
    - Tập trung vào trạng thái (Status) và Độ ưu tiên (Priority).
    - Không làm quá nhiều trường dữ liệu phức tạp. Chỉ tập trung vào việc: "Ai làm?", "Việc gì?", "Khi nào xong?".
- **Notion Style (Properties)**:
    - Sử dụng các nhãn màu sắc để phân biệt độ ưu tiên (Low, Medium, High, Urgent).
- **Trải nghiệm người dùng (UX)**:
    - API phải hỗ trợ cập nhật nhanh trạng thái (Toggle Done).
    - Hỗ trợ sắp xếp theo ngày hạn (Due Date) hoặc Độ ưu tiên.

## 2. Mô hình hóa dữ liệu (Data Modeling)

### Entity: EmployeeTask
- `id`: Định danh.
- `organizationId`: Multi-tenancy isolation.
- `employeeId`: Nhân viên được giao việc (Target).
- `creatorId`: Người giao việc (Sếp hoặc đồng nghiệp).
- `title`: Tiêu đề công việc (Ngắn gọn).
- `description`: Mô tả chi tiết (Markdown support).
- `status`: [BACKLOG, TODO, IN_PROGRESS, DONE, CANCELED].
- `priority`: [NONE, LOW, MEDIUM, HIGH, URGENT].
- `dueDate`: Hạn chót.
- `completedAt`: Thời điểm thực tế hoàn thành.

## 3. API Design

Theo yêu cầu của Frontend, chúng ta sử dụng kiến trúc Nested Resource:

- `GET /api/hrm/employees/:employeeId/tasks` - Lấy danh sách task của 1 nhân viên.
- `POST /api/hrm/employees/:employeeId/tasks` - Giao việc mới cho nhân viên.
- `PATCH /api/hrm/employees/:employeeId/tasks/:taskId` - Cập nhật task (trạng thái, nội dung).
- `DELETE /api/hrm/employees/:employeeId/tasks/:taskId` - Xóa task.

## 4. Bảo mật (Security)
- **Multi-tenancy**: Chặn tuyệt đối việc xem/giao task cho nhân viên công ty khác.
- **Permission**:
    - `task:read`: Xem công việc.
    - `task:create`: Giao việc.
    - `task:update`: Cập nhật trạng thái (Chỉ người giao hoặc người nhận).
    - `task:delete`: Xóa (Chỉ người giao hoặc Admin).

## 5. Kỹ thuật xuất sắc (Technical Excellence)
- **Tối ưu hóa Truy vấn**: 
    - Thêm Index B-Tree cho `organizationId`, `employeeId` và `status`.
    - Đảm bảo tốc độ O(log N) cho các thao tác lọc và phân trang.
- **Tính nhất quán dữ liệu**:
    - Sử dụng `class-transformer` để chuẩn hóa dữ liệu đầu vào (Date object) ngay từ Controller.
    - Logic đóng/mở task được đóng gói trong Domain Entity để đảm bảo tính toàn vẹn của `completedAt`.
