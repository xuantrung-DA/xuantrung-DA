# Bảo trì GitHub profile

Profile dùng các SVG tự chứa được tạo bằng Python. Nội dung và animation nằm trong repo; không cần dịch vụ tạo ảnh, JavaScript, webfont hoặc workflow chạy định kỳ.

## Cấu trúc

- [`README.md`](../README.md): các liên kết, alt text và quy tắc chọn ảnh.
- [`scripts/generate_readme_visuals.py`](../scripts/generate_readme_visuals.py): nội dung, bố cục và animation; chỉ dùng Python standard library.
- [`assets/chrome-ruby/`](../assets/chrome-ruby/): 84 SVG được tạo từ script, gồm light/dark, desktop/mobile và bản tĩnh cho các phần có animation.

## Cập nhật

Yêu cầu **Python 3.12 trở lên**. Chạy từ thư mục repo:

```sh
python scripts/generate_readme_visuals.py
python scripts/generate_readme_visuals.py --check
git diff --check
```

Lệnh đầu tạo lại SVG; `--check` kiểm tra nội dung file mà không ghi thay đổi. Chỉnh script rồi tạo lại asset, không sửa SVG bằng tay. Khi thay đổi nội dung hiển thị, cập nhật cả alt text trong README. Giữ các file SVG đã tạo trong repo để GitHub hiển thị trực tiếp.

| Nội dung | Vị trí chỉnh trong script |
| --- | --- |
| Màu sắc và chất liệu bạc/ruby | `THEMES`, `material_defs()` |
| Hero và tên | `hero()`, `brain_art()`, `signature_title()`, `signature_bus()` |
| Bốn dự án, số liệu và điều kiện đo | `PROJECTS`, `project()` và các hàm minh họa |
| Kinh nghiệm | `experience()`, `delivery_stage()` |
| Bảy bài nghiên cứu và trạng thái | `PAPERS`, `research()`, `research_art()` |
| Năm nhóm toolkit | `STACK_GROUPS`, `toolkit()` |
| Email, availability, học vấn | `footer()`, `connection_iris()` |
| Animation | `CSS`, `signature_motion()`, `brain_art()`, `project_defs()`, `profile_defs()`, `research_art()` |

Link Portfolio, Résumé, LinkedIn, Email và các repository nằm trong README. Email còn xuất hiện trong `footer()` nên cần cập nhật cả hai khi đổi địa chỉ.

## Thiết kế Chrome / Ruby

Profile dùng bạc ánh kim, đỏ ruby và nền graphite; bản sáng dùng nền bạc nhạt. Tên và headline footer có ánh phản chiếu chạy qua nét chữ, giữ nguyên vị trí và nền chữ để luôn đọc được. Footer giữ biểu tượng iris xoay và có đường tín hiệu dưới email.

Research minh họa nguồn dữ liệu đi qua ba lớp ma trận, chuyển xuống đồ thị đối chiếu và bước xác nhận. Đồ thị là hình minh họa, không phải kết quả đo. Danh sách bảy bài và trạng thái đứng yên. Bố cục mobile dành thêm một hàng cho phần minh họa này.

Nhịp ánh quét trên tên và mô phỏng Research là 6,4 giây; headline footer là 8 giây. Bản tĩnh tắt chuyển động và giữ đủ nội dung. Các GIF, ảnh chụp và trang preview dùng để duyệt thiết kế nằm ngoài repo; README hiển thị trực tiếp SVG.

## Nội dung tham chiếu

Nội dung được đối chiếu với [portfolio](https://xuantrung-ai-portfolio.vercel.app/) ngày **10/09/2026**:

- Dự án chính: TraceVision, Subject Knowledge Hub, AQB-FAS và DATU / Offline RL. Giữ điều kiện benchmark đi cùng số liệu; animation chỉ minh họa cơ chế, không phải telemetry hay kết quả đo trực tiếp.
- Research: 7 bài, gồm 2 published, 2 accepted và 3 submitted. DATU là dự án nghiên cứu độc lập, không nằm trong danh sách bài báo. Khi có trạng thái mới, cập nhật `PAPERS`, số đếm trong `research()` và alt text.
- Toolkit: đúng 5 nhóm và 25 mục trong phần Capabilities của portfolio. Không hiển thị điểm hoặc phần trăm thành thạo.
- Résumé dẫn tới CV trên portfolio; repo không giữ thêm bản PDF riêng.

## Kiểm tra hiển thị

`<picture>` chọn ảnh theo theme, viewport và tùy chọn giảm chuyển động. Bố cục mobile áp dụng ở viewport tối đa 800 px. Nguồn reduced motion đứng trước nguồn động; SVG cũng có CSS dừng animation khi hệ thống yêu cầu giảm chuyển động.

Sau khi sửa, kiểm tra light/dark, mobile/desktop và reduced motion. Đặc biệt xem tên bài dài, alt text, các liên kết và kích thước ảnh. README hiện có 14 ảnh, 70 nguồn media và 12 liên kết; không có mục thu gọn.

Có thể render Markdown bằng GitHub Markdown API để kiểm tra HTML sau sanitization. CSS của công cụ preview có thể khác giao diện GitHub; kiểm tra trang profile thực sau khi xuất bản. Việc chạy generator không commit, push hay xuất bản nội dung.
