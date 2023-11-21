import os, shutil, time
import tkinter as tk
from tqdm import tqdm
from tkinter import filedialog
from tkinter import messagebox

desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')

def date_word_format(date):
    y = date[:4]
    m = date[4:6]
    d = date[6:8]
    h = date[8:10]
    min = date[10:12]
    s = date[12:14]
    
    date_string_format = f"{y}년{m}월{d}일 {h}:{min}:{s}"
    
    return date_string_format

def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def file_select():
    while True:
        file_paths = filedialog.askopenfilenames(
            initialdir=desktop_path,
            title = "파일 선택",
        )

        if file_paths == '':
            if messagebox.askyesno("경고", "파일을 선택해주세요"):
                continue
            else:
                return None        
        
        file_path_msg = ""
        
        if len(file_paths) >= 30:
            file_path_msg = f"선택한 파일이 많아 표시할 수 없습니다. ({len(file_paths)}개)\n"
        else:
            for file_path_tuple in file_paths:
                file_path_msg += str(file_path_tuple) + "\n"
        
        if messagebox.askyesno("파일 확인", file_path_msg + "계속 하시겠습니까?"):
            return file_paths
        else :
            continue

def select_folder():
    while True:
        folder_path = filedialog.askdirectory(
            initialdir=desktop_path,
            title = "폴더 선택"
        )
        
        if folder_path == '':
            if messagebox.askyesno("경고", "폴더를 선택해주세요"):
                continue
            else:
                return None
        
        if messagebox.askyesno("폴더 확인", folder_path + "\n여기에 저장하시겠습니까?"):
            return folder_path
        else :
            continue

def check_duplicate_file(file_path, file_name):
    files_in_path = os.listdir(file_path)
    if file_name in files_in_path:
        return True
    return False

def delete_file(file_path):
    try:
        os.remove(file_path)
    except OSError as e:
        return

def delete_folder_contents(folder_path):
    total_files_count = len(os.listdir(folder_path))
    process_bar = tqdm(total=total_files_count, desc="Delete process")
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # if file
        if os.path.isfile(file_path):
            os.unlink(file_path)
        # if folder
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
        
        process_bar.update(1)
    process_bar.set_description("Delete Complete")
    process_bar.close()
        

            
def get_number_box(show_number):
    def on_confirm():
        value = entry.get()
        try:
            num = int(value)
            window.destroy()
            return_value(num)
        except ValueError:
            error_label.config(text="올바른 숫자를 입력하세요", fg="red")

    def on_cancel():
        window.destroy()
        return_value(None)

    def on_closing():
        window.destroy()
        return_value(None)

    def return_value(value):
        nonlocal return_val
        return_val = value

    return_val = None

    window = tk.Tk()
    window.title("숫자 입력")
    
    window.resizable(False, False)

    window.geometry("250x150")
    
    frame = tk.Frame(window)
    frame.pack(padx=20, pady=10)

    label = tk.Label(frame, text=f"[{show_number}]\n표시된 숫자를 입력하세요")
    label.pack()

    entry = tk.Entry(frame)
    entry.pack(pady=5)

    error_label = tk.Label(frame, text="", fg="red")
    error_label.pack()

    button_frame = tk.Frame(window)
    button_frame.pack(padx=20, pady=(0, 10))

    confirm_button = tk.Button(button_frame, text="확인", command=on_confirm)
    confirm_button.pack(side=tk.LEFT, padx=5)

    cancel_button = tk.Button(button_frame, text="취소", command=on_cancel)
    cancel_button.pack(side=tk.LEFT, padx=5)

    window.protocol("WM_DELETE_WINDOW", on_closing)
    window.mainloop()

    return return_val

def cancel_input(pause_skip=False, print_desc="Task Canceld"):
    print(print_desc, end="\n\n")
    
    if pause_skip: return
    
    os.system("pause")