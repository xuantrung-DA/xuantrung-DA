HƯỚNG DẪN CẬP NHẬT CÁC SVG TRONG README
=========================================

1. TỔNG QUAN
------------

Các file SVG trong thư mục assets/ được sinh tự động từ dữ liệu JSON.
Không nên sửa trực tiếp nội dung các file SVG vì thay đổi sẽ bị ghi đè ở lần chạy tiếp theo.

Script chính:
  scripts/generate_readme_visuals.py

File dữ liệu:
  data/profile-visuals.json
  data/tech-stack.json

Yêu cầu:
  - Python 3.10 trở lên.
  - Không cần cài thêm thư viện ngoài.
  - Chạy lệnh tại thư mục gốc của repo xuantrung-DA.


2. CẬP NHẬT TOÀN BỘ SVG
-----------------------

Sau khi sửa dữ liệu JSON, chạy:

  py scripts/generate_readme_visuals.py

Lệnh này tạo hoặc cập nhật:

  assets/profile-signal.svg
  assets/tech-stack.svg
  assets/selected-work.svg
  assets/research.svg
  assets/credentials.svg
  assets/footer.svg

Kiểm tra các SVG đã đồng bộ với dữ liệu chưa:

  py scripts/generate_readme_visuals.py --check

Nếu mọi thứ hợp lệ, kết quả sẽ là:

  README visuals are up to date.


3. CẬP NHẬT TỪNG PHẦN
----------------------

3.1. Profile Signal

SVG đầu ra:
  assets/profile-signal.svg

Dữ liệu cần sửa:
  data/profile-visuals.json

Các trường liên quan:
  - signals: ba tagline chạy luân phiên.
  - facts: Education, GPA, Graduation và Status.

Lệnh chạy riêng:

  py scripts/generate_readme_visuals.py --only profile-signal

Lệnh kiểm tra riêng:

  py scripts/generate_readme_visuals.py --only profile-signal --check


3.2. Engineering Stack

SVG đầu ra:
  assets/tech-stack.svg

Dữ liệu cần sửa:
  data/tech-stack.json

Các trường liên quan:
  - eyebrow: nhãn nhỏ phía trên tiêu đề.
  - title: tiêu đề chính.
  - subtitle: mô tả ngắn.
  - sections: các nhóm kỹ năng.
  - sections[].phase: tên giai đoạn, ví dụ BUILD hoặc DELIVER.
  - sections[].title: tên nhóm kỹ năng.
  - sections[].accent: màu nhấn dạng mã HEX, ví dụ #D5A84F.
  - sections[].items: danh sách công nghệ hoặc kỹ năng.
  - principles: các nguyên tắc engineering ở cuối SVG.

Ví dụ thêm một công nghệ:

  "items": [
    "Python",
    "PyTorch",
    "Docker"
  ]

Lệnh chạy riêng:

  py scripts/generate_readme_visuals.py --only tech-stack

Lệnh kiểm tra riêng:

  py scripts/generate_readme_visuals.py --only tech-stack --check


3.3. Selected Systems

SVG đầu ra:
  assets/selected-work.svg

Dữ liệu cần sửa:
  data/profile-visuals.json

Trường liên quan:
  projects

Mỗi project gồm:
  - name: tên dự án.
  - domain: nhóm chuyên môn hiển thị bằng chữ in hoa.
  - description: kết quả hoặc điểm nổi bật của dự án.
  - stack: danh sách công nghệ chính.

Ví dụ:

  {
    "name": "Project Name",
    "domain": "COMPUTER VISION",
    "description": "Mô tả ngắn, ưu tiên kết quả đo được",
    "stack": ["PyTorch", "OpenCV", "FastAPI"]
  }

Lệnh chạy riêng:

  py scripts/generate_readme_visuals.py --only selected-work

Lệnh kiểm tra riêng:

  py scripts/generate_readme_visuals.py --only selected-work --check


3.4. Research & Recognition

SVG đầu ra:
  assets/research.svg

Dữ liệu cần sửa:
  data/profile-visuals.json

Trường liên quan:
  research

Mỗi mục gồm:
  - type: loại thành tích, ví dụ RECOGNITION hoặc SPRINGER LNAI.
  - year: năm hiển thị trên timeline.
  - title: tên giải thưởng hoặc bài báo.
  - detail: trường, hội nghị, volume và trạng thái xuất bản.

Lệnh chạy riêng:

  py scripts/generate_readme_visuals.py --only research

Lệnh kiểm tra riêng:

  py scripts/generate_readme_visuals.py --only research --check

Lưu ý:
  Layout hiện được thiết kế cho đúng 3 mục research/recognition.


3.5. Credentials

SVG đầu ra:
  assets/credentials.svg

Dữ liệu cần sửa:
  data/profile-visuals.json

Trường liên quan:
  certifications

Mỗi chứng chỉ gồm:
  - title: tên chứng chỉ.
  - issuer: đơn vị phát hành.
  - date: thời gian hoàn thành theo định dạng MM / YYYY.

Lệnh chạy riêng:

  py scripts/generate_readme_visuals.py --only credentials

Lệnh kiểm tra riêng:

  py scripts/generate_readme_visuals.py --only credentials --check

Lưu ý:
  Layout hiện được thiết kế cho đúng 4 chứng chỉ.


3.6. Footer

SVG đầu ra:
  assets/footer.svg

Dữ liệu cần sửa:
  data/profile-visuals.json

Trường liên quan:
  footer

Lệnh chạy riêng:

  py scripts/generate_readme_visuals.py --only footer

Lệnh kiểm tra riêng:

  py scripts/generate_readme_visuals.py --only footer --check


4. QUY TRÌNH KHUYẾN NGHỊ MỖI LẦN CẬP NHẬT
------------------------------------------

Bước 1:
  Sửa data/profile-visuals.json hoặc data/tech-stack.json.

Bước 2:
  Sinh lại SVG cần thay đổi hoặc toàn bộ SVG.

  py scripts/generate_readme_visuals.py

Bước 3:
  Chạy kiểm tra đồng bộ.

  py scripts/generate_readme_visuals.py --check

Bước 4:
  Mở README.md hoặc SVG vừa sinh để kiểm tra chữ, khoảng cách và animation.

Bước 5:
  Kiểm tra thay đổi Git.

  git status --short
  git diff --check

Bước 6:
  Commit và push khi đã duyệt giao diện.


5. LƯU Ý KHI SỬA JSON
---------------------

  - Giữ file ở encoding UTF-8.
  - Dùng dấu ngoặc kép cho key và text.
  - Không đặt dấu phẩy sau phần tử cuối cùng.
  - Không xóa các key bắt buộc.
  - Viết description ngắn và ưu tiên metric hoặc outcome.
  - Không thêm quá nhiều công nghệ chỉ để lấp đầy giao diện.
  - Màu accent phải có định dạng #RRGGBB.
  - Nếu script báo lỗi JSON, kiểm tra dấu phẩy, ngoặc vuông và ngoặc nhọn.


6. KHI MUỐN THAY ĐỔI BỐ CỤC HOẶC ANIMATION
------------------------------------------

Dữ liệu và nội dung:
  Sửa các file JSON trong data/.

Bố cục, màu sắc và animation:
  Sửa scripts/generate_readme_visuals.py, sau đó chạy lại:

  py scripts/generate_readme_visuals.py

Các màu dùng chung nằm trong biến COLORS ở đầu script.
Animation dùng CSS keyframes và SVG animate/animateMotion.

Luôn kiểm tra lại toàn bộ asset sau khi sửa generator:

  py scripts/generate_readme_visuals.py --check


7. XỬ LÝ LỖI NHANH
------------------

Lỗi "Out-of-date generated assets":
  Chạy py scripts/generate_readme_visuals.py để sinh lại SVG.

Lỗi JSONDecodeError:
  File JSON đang sai cú pháp; kiểm tra dấu phẩy và dấu ngoặc.

Chữ bị tràn:
  Rút ngắn title/description hoặc điều chỉnh wrap_text và pack_items trong script.

Animation không chạy khi xem ảnh preview tĩnh:
  Mở trực tiếp file SVG bằng trình duyệt hoặc xem README trên GitHub.

Animation không chạy do hệ điều hành:
  Kiểm tra cài đặt Reduce Motion. SVG chủ động giảm animation khi
  prefers-reduced-motion được bật.


TÓM TẮT LỆNH
------------

Cập nhật tất cả:
  py scripts/generate_readme_visuals.py

Kiểm tra tất cả:
  py scripts/generate_readme_visuals.py --check

Cập nhật riêng một phần:
  py scripts/generate_readme_visuals.py --only <tên-phần>

Các tên phần hợp lệ:
  profile-signal
  tech-stack
  selected-work
  research
  credentials
  footer
