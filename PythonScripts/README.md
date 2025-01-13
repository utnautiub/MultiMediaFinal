# PythonScripts - Hướng dẫn sử dụng

## 1. **Môi trường yêu cầu**
- Python >= 3.7
- Các thư viện: OpenCV, NumPy

---

## 2. **Hướng dẫn thiết lập**

### a. **Tạo môi trường ảo (venv)**
1. Mở terminal hoặc command prompt tại thư mục **PythonScripts**.
2. Tạo môi trường ảo:
   ```bash
   python -m venv venv
   ```
3. Kích hoạt môi trường ảo:
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **Linux/MacOS**:
     ```bash
     source venv/bin/activate
     ```
   - **Other**:
     ```bash
     source venv/Scripts/activate
     ```

### b. **Cài đặt các thư viện**
1. Sau khi kích hoạt môi trường ảo, cài đặt các thư viện cần thiết:
   ```bash
   pip install -r requirements.txt
   ```

### c. **Kiểm tra môi trường**
1. Kiểm tra các thư viện đã được cài đặt:
   ```bash
   pip list
   ```
2. Đảm bảo các thư viện **opencv-python** và **numpy** đã có trong danh sách.

---

## 3. **Cách sử dụng**

### a. **Đặt ảnh đầu vào**
- Đặt ảnh cần xử lý vào thư mục `input/`.

### b. **Chạy chương trình**
1. Kích hoạt môi trường ảo:
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **Linux/MacOS**:
     ```bash
     source venv/bin/activate
     ```
2. Chạy script Python:
   ```bash
   python main.py
   ```

### c. **Kết quả**
- Ảnh đầu ra sẽ được lưu trong thư mục `output/`.
- Mặc định, file đầu vào là `example.jpg` và file kết quả là `result.jpg`.

---

## 4. **Gọi từ WinForm (C#)**

Nếu bạn muốn gọi script này từ WinForm C#:
1. Đảm bảo môi trường ảo đã được kích hoạt.
2. Gọi file `main.py` từ C# với đường dẫn đầy đủ đến Python trong môi trường ảo:
   - Đường dẫn Python: `venv\Scripts\python.exe`.
   - Lệnh gọi từ C#:
     ```csharp
     string pythonPath = @"venv\Scripts\python.exe";
     string scriptPath = @"main.py";
     string arguments = $"{scriptPath} input_image output_image";
     ```

---

## 5. **Lưu ý**
- Luôn kích hoạt môi trường ảo trước khi chạy chương trình.
- Nếu thêm thư viện mới, hãy cập nhật file `requirements.txt`:
  ```bash
  pip freeze > requirements.txt
  ```

---

## 6. **Khắc phục sự cố**
- **Lỗi không tìm thấy Python hoặc thư viện:**
  - Đảm bảo môi trường ảo đã được kích hoạt.
- **Lỗi không đọc được ảnh đầu vào:**
  - Kiểm tra xem file ảnh có nằm trong thư mục `input/` hay không.
  - Đảm bảo file ảnh có định dạng hợp lệ (jpg, png, v.v.).

