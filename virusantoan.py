import os
import sys
import platform
import string
from cryptography.fernet import Fernet

# --- CẤU HÌNH ---
KEY = b"JFDPxL5meIaGtBghmIhpKy4v1jcIywx3a3PgpuOq668="
FERNET = Fernet(KEY)

# --- CÁC HÀM XỬ LÝ FILE ---
def find_target_folder():
    system = platform.system()
    if os.path.exists('test_folder'):
        return os.path.abspath('test_folder')
    
    if system == "Windows":
        drives = [f'{d}:\\' for d in string.ascii_uppercase if os.path.exists(f'{d}:\\')]
        for drive in drives:
            if drive == 'C:\\': continue
            for root, dirs, _ in os.walk(drive):
                if 'test_folder' in dirs: return os.path.join(root, 'test_folder')
    else:
        home = os.path.expanduser("~")
        for root, dirs, _ in os.walk(home):
            if 'test_folder' in dirs: return os.path.join(root, 'test_folder')
    return None

def encrypt_files(folder_path):
    try:
        files = [f for f in os.listdir(folder_path) if not f.endswith(".encrypted")]
        if not files: print("-> Không có file để mã hóa.")
        for filename in files:
            path = os.path.join(folder_path, filename)
            if os.path.isfile(path):
                with open(path, "rb") as f: data = f.read()
                with open(path + ".encrypted", "wb") as f: f.write(FERNET.encrypt(data))
                os.remove(path)
        print("-> Đã mã hóa xong.")
    except Exception as e:
        print(f"[-] Lỗi khi mã hóa: {e}")

def decrypt_files(folder_path):
    try:
        files = [f for f in os.listdir(folder_path) if f.endswith(".encrypted")]
        if not files:
            print("-> Không có file nào cần giải mã.")
            return
        for filename in files:
            path = os.path.join(folder_path, filename)
            with open(path, "rb") as f: data = f.read()
            with open(path.replace(".encrypted", ""), "wb") as f: f.write(FERNET.decrypt(data))
            os.remove(path)
        print("-> Đã khôi phục xong dữ liệu.")
    except Exception as e:
        print(f"[-] Lỗi khi giải mã: {e}")

# --- HÀM ĐIỀU KHIỂN ---
def main():
    # 1. Hiển thị điều khoản xác nhận trách nhiệm
    print("--- CẢNH BÁO: ĐIỀU KHOẢN SỬ DỤNG ---")
    print("Đây là phần mềm thử nghiệm mã hóa dữ liệu.")
    print("Bằng cách nhấn 'y', bạn cam kết:")
    print("1. Hiểu rõ chương trình này sẽ tác động lên file.")
    print("2. Hoàn toàn chịu mọi trách nhiệm cá nhân về dữ liệu của bạn.")
    print("3. Không sử dụng chương trình vào các mục đích gây hại.")
    
    confirm = input("Bạn có đồng ý với các điều khoản trên không? (y/n): ").lower()
    if confirm != 'y':
        print("-> Bạn đã từ chối điều khoản. Chương trình sẽ tắt ngay lập tức.")
        return # Tắt chương trình

    # 2. Tìm kiếm thư mục
    folder = find_target_folder()
    if not folder:
        print("[-] Không tìm thấy thư mục 'test_folder'.")
        return

    print(f"[*] Tìm thấy thư mục tại: {folder}")
    
    # 3. Menu điều khiển
    while True:
        print("\n--- MENU CHÍNH ---")
        print("1. Mã hoá dữ liệu")
        print("2. Giải mã dữ liệu")
        print("3. Thoát (Tự động giải mã ngay lập tức)")
        
        choice = input("Chọn: ")
        
        if choice == '1':
            encrypt_files(folder)
        elif choice == '2':
            decrypt_files(folder)
        elif choice == '3':
            print("-> Đang thực hiện giải mã trước khi thoát...")
            decrypt_files(folder)
            print("-> Đã thoát chương trình.")
            sys.exit()
        else:
            print("Lựa chọn không hợp lệ.")

if __name__ == "__main__":
    main()
