<h2 align="center">
    <a href="https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin">
    🎓 Faculty of Information Technology (DaiNam University)
    </a>
</h2>
<h2 align="center">
    PLATFORM ERP
</h2>
<div align="center">
    <p align="center">
        <img src="docs/logo/aiotlab_logo.png" alt="AIoTLab Logo" width="170"/>
        <img src="docs/logo/fitdnu_logo.png" alt="AIoTLab Logo" width="180"/>
        <img src="docs/logo/dnu_logo.png" alt="DaiNam University Logo" width="200"/>
    </p>

[![AIoTLab](https://img.shields.io/badge/AIoTLab-green?style=for-the-badge)](https://www.facebook.com/DNUAIoTLab)
[![Faculty of Information Technology](https://img.shields.io/badge/Faculty%20of%20Information%20Technology-blue?style=for-the-badge)](https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin)
[![DaiNam University](https://img.shields.io/badge/DaiNam%20University-orange?style=for-the-badge)](https://dainam.edu.vn)

</div>

## 🔧 1. Các công nghệ được sử dụng
<div align="center">

### Hệ điều hành
[![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)](https://ubuntu.com/)
### Công nghệ chính
[![Odoo](https://img.shields.io/badge/Odoo-714B67?style=for-the-badge&logo=odoo&logoColor=white)](https://www.odoo.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![XML](https://img.shields.io/badge/XML-FF6600?style=for-the-badge&logo=codeforces&logoColor=white)](https://www.w3.org/XML/)
### Cơ sở dữ liệu
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
</div>

## ⚙️ 2. Cài đặt

### 2.1. Cài đặt công cụ, môi trường và các thư viện cần thiết

#### 2.1.1. Tải project.
```
https://github.com/QuangTungMasterD/BTL_HN-QTPMDN.git
```
#### 2.1.2. Cài đặt các thư viện cần thiết
Người sử dụng thực thi các lệnh sau đề cài đặt các thư viện cần thiết

```
sudo apt-get install libxml2-dev libxslt-dev libldap2-dev libsasl2-dev libssl-dev python3.10-distutils python3.10-dev build-essential libssl-dev libffi-dev zlib1g-dev python3.10-venv libpq-dev
```
#### 2.1.3. Khởi tạo môi trường ảo.
- Khởi tạo môi trường ảo
```
python3.10 -m venv ./venv
```
- Thay đổi trình thông dịch sang môi trường ảo
```
source venv/bin/activate
```
- Chạy requirements.txt để cài đặt tiếp các thư viện được yêu cầu
```
pip3 install -r requirements.txt
```
### 2.2. Setup database

Khởi tạo database trên docker bằng việc thực thi file dockercompose.yml.
```
sudo docker-compose up -d
```
### 2.3. Setup tham số chạy cho hệ thống
Tạo tệp **odoo.conf** có nội dung như sau:
```
[options]
addons_path = addons
db_host = localhost
db_password = odoo
db_user = odoo
db_port = 5431
xmlrpc_port = 8069
```
Có thể kế thừa từ file **odoo.conf.template**
### 2.4. Chạy hệ thống và cài đặt các ứng dụng cần thiết
Lệnh chạy
```
python3 odoo-bin.py -c odoo.conf -u all
```
Người sử dụng truy cập theo đường dẫn _http://localhost:8069/_ để đăng nhập vào hệ thống.

# 📖 4. Tham khảo
- #### [Module công việc](https://github.com/HDatz/TTDN-15-03-N6/tree/main/addons/quan_ly_cong_viec)
- #### [Module khách hàng](https://github.com/ThienDao103/TTDN-15-03-N5/tree/main/addons/quan_ly_khach_hang)

# 📅 5. Google Calendar – Đồng bộ lịch hai chiều
## 5.1. Tạo dự án và lấy thông tin xác thực trên Google Cloud Console.
- Truy cập [Google Cloud Console](https://console.cloud.google.com) và tạo một dự án.
- Bật Google Calendar API cho dự án.
- Trong mục APIs & Services > Credentials, tạo OAuth client ID với loại Web application.
- Cấu hình origin redirect URIs đúng với địa chỉ Odoo của bạn

    https://odoo.example.com
    (nếu chạy local: http://localhost:8069)
- Cấu hình Authorized redirect URIs đúng với địa chỉ Odoo của bạn

    https://odoo.example.com/google_account/authentication
    (nếu chạy local: http://localhost:8069/google_account/authentication)
- Sau khi tạo, lưu lại **Client ID** và **Client Secret**.
## 5.2. Nhập thông tin vào Odoo.
- Vào Cài đặt > Cài đặt chung > Google Calendar.
- Tích chọn Google Calendar, dán Client ID và Client Secret vào các trường tương ứng.
- Nhấn Lưu.

## 5.3. Kết nối tài khoản Google cá nhân (từng nhân viên tự thực hiện).
- Đăng nhập Odoo với tài khoản của bạn.
- Vào Lịch > nhấn nút Kết nối với Google (đồng bộ với google của bạn).
- Odoo chuyển hướng tới tài khoản google > Cấp quyền.

#### **Lưu ý: Chỉ những nhân viên đã kết nối tài khoản Google mới nhận được sự kiện đồng bộ.**
<br/>
<br/>

# ***Tiếp theo đến phần tích hợp Google Celander, email SMTP và AI Gemini***
## *🚨Lưu ý: do tương lai có thể các công nghệ thay có thể thay đổi bước thực hiện, tên, api, ... Nếu có lỗi hay hướng dẫn không đúng quy trình người dùng có thể tự tìm hướng dẫn*

# 📅 6. Cấu hình Email (SMTP)
Để Odoo gửi email thông báo (nhắc deadline công việc/dự án, xác nhận lịch hẹn…), bạn cần cấu hình một máy chủ gửi email đi
## 6.1. Tạo mật khẩu ứng dụng cho tài khoản Gmail.
- Truy cập trang https://myaccount.google.com/apppasswords.
- Nhập tên ứng dụng > nhấn tạo.
- Một mật khẩu 16 ký tự hiện ra, ***copy lại***(ví dụ: xxxx xxxx xxxx xxxx).
## 6.2. Cấu hình trong Odoo
- Vào Cài đặt > Kỹ thuật > Email > Máy chủ gửi email đi.
- Nhấn Tạo và điền:
    - Mô tả: Gmail SMTP
    - Máy chủ SMTP: smtp.gmail.com
    - Cổng: 587 (hoặc 465 nếu dùng SSL)
    - Bảo mật kết nối: STARTTLS (nếu cổng 587) hoặc SSL/TLS (nếu cổng 465)
    - Tên đăng nhập: địa chỉ Gmail của bạn (ví dụ yourmail@gmail.com)
    - Mật khẩu: dán mật khẩu ứng dụng vừa tạo
- **Đánh dấu Mặc định**.
- **Nhấn Kiểm tra kết nối** để xác nhận thành công, sau đó lưu.
## 6.3. Kiểm tra gửi email
- Vào Kỹ thuật > Email > Mẫu email, mở một mẫu bất kỳ.
- Nhấn Gửi thử, chọn một bản ghi có người nhận hợp lệ.
- Nếu email đến hộp thư, cấu hình đã hoạt động.
# 📅 7. Add AI gemini
Tính năng này cho phép nhân viên nhấn nút "Gợi ý AI" trên form công việc hoặc dự án để tự động sinh mô tả chi tiết.
## 7.1. Lấy API key Gemini
- Truy cập [Google AI Studio](https://aistudio.google.com), đăng nhập bằng tài khoản Google.
- Nhấn import > import project bạn vừa tạo để kết nối Google Celander.
- Nhấn Create API key > ***Copy key***.
## 7.2. Cấu hình API key trong Odoo
- Vào Kỹ thuật > Tham số hệ thống.
- Nhấn Tạo, điền:
    - **Key**: *gemini_api_key*
    - **value**: *dán API key vừa copy*
- Lưu lại.
## 7.3. Kiểm tra
- Tạo một công việc hoặc dự án mới, nhập tên.
- Nhấn nút Gợi ý AI (trên form công việc hoặc dự án).
- Sau vài giây, trường mô tả sẽ được điền nội dung do Gemini sinh ra.

# 8. Liên hệ
#### [Facebook](https://www.facebook.com/tran.quang.tung.716688)
#### tranquangtung26062005@gmail.com
