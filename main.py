from cryptography.fernet import Fernet
from tqdm import tqdm
from src import *

import json, sys, datetime, random

program_key = b'8UNLxwvJynEi8At3V2BQJ23VglmRubdwVtqLR-L941M='
file_storage_path = './file_storage/'
abs_file_storage_path = os.path.abspath(file_storage_path)

program_ver = '2.1b'
program_name = 'FileGuardian'
program_title = program_name + " " + program_ver

def enc_files():
    file_paths = file_select()
    # file_paths = ('C:/Users/gi679/OneDrive/바탕 화면/test.txt','C:/Users/gi679/OneDrive/바탕 화면/test.txt',)

    if file_paths == None:
        print("There are no files selected.")
        return 1

    # 폴더 관리
    create_folder_if_not_exists(file_storage_path)

    # 전체 진행률 bar
    overall_progress_num = len(file_paths)
    overall_progress_bar = tqdm(total=overall_progress_num, desc="enc progress")
    for file in file_paths:
        # generate key
        enc_key = Fernet.generate_key()
            
        # encrypt file
        with open(file, 'rb') as file_contents_temp:
            file_contents = file_contents_temp.read()
        
        enc_file_contents = Fernet(enc_key).encrypt(file_contents)
        
        # file info save
        ## generate id. duplicate check
        duplicate_count = 0
        while True:
            file_id_path = str(Fernet.generate_key())
            if check_duplicate_file(file_storage_path, file_id_path+".json"): 
                if duplicate_count >= 10: return 1
                duplicate_count += 1
                continue
            else:
                break
                
        file_id = file_id_path
        file_name = os.path.basename(file)
        file_key = str(Fernet(program_key).encrypt(enc_key))
        enc_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        
        file_info = {
            "file_id": file_id,
            "file_name": file_name,
            "file_key": file_key,
            "enc_time": enc_time,
        }
        
        with open(file_storage_path+file_id+".json", 'w') as outfile:
            json.dump(file_info, outfile, indent=2)
            
        # file save
        with open(file_storage_path+file_id+".enc", 'wb') as file_contents_temp:
            file_contents_temp.write(enc_file_contents)
            
        overall_progress_bar.update(1)
    overall_progress_bar.set_description("enc Complete")
    overall_progress_bar.close()
    
    messagebox.Message(title=program_title, message="선택한 모든 파일이 성공적으로 암호화되었습니다.").show()
    
    
    
def dec_file():
    file_list = os.listdir(abs_file_storage_path)
    json_file_list = [file for file in file_list if file.endswith('.json')]
    
    file_num = 0
    
    print("{:>4s}  {:^40s}  {:^20s}".format("#", "file name", "file save time"))
    for file in json_file_list:
        with open(file_storage_path+file, "r") as json_file_contents:
            origin_file_name = json.load(json_file_contents)["file_name"]
        with open(file_storage_path+file, "r") as json_file_contents:
            origin_file_save_time = json.load(json_file_contents)["enc_time"]
            origin_file_save_time = date_word_format(origin_file_save_time)
        
        print("%4d. %-40s %20s" % (file_num+1, origin_file_name, origin_file_save_time))
        file_num += 1
    
    try:
        file_sel_num = int(input(">> "))-1
    except KeyboardInterrupt:
        print("Cancel input")
        return 0
    except:
        print("Invalid input value")
        return 1
    
    ############# dec ##############
    # file save path select
    dec_file_save_path = select_folder()
    
    if dec_file_save_path == None:
        print("There are no folder selected.")
        return 1
    
    # file info loading
    file_num = 0
    for file in json_file_list:
        if file_num == file_sel_num:
            with open(file_storage_path+file, "r") as json_file_contents:
                sel_file_id = json.load(json_file_contents)["file_id"]
            break
        file_num += 1
        
    # Retrieve selected file information
    with open(file_storage_path+sel_file_id+".json", "r") as file_temp:
        sel_json_data = json.load(file_temp)
    with open(file_storage_path+sel_file_id+".enc", "rb") as file_temp:
        sel_file_data = file_temp.read()
    
    sel_file_name = sel_json_data['file_name']
    
    # Decrypting
    try:
        sel_file_key = Fernet(program_key).decrypt(eval(sel_json_data['file_key']))
        dec_file_contents = Fernet(sel_file_key).decrypt(sel_file_data)
    except Exception as e:
        print("\nErorr Invalid file Key")
        return 1
        
    # file save
    if check_duplicate_file(dec_file_save_path, sel_file_name):
        if messagebox.askyesno(program_title, "해당 경로에 이미 같은 이름의 파일이 있습니다.\n덮어씌우겠습니까?") == False:
            messagebox.Message(title=program_title, message="복호화가 취소되었습니다.").show()
            return 1
        
    with open(dec_file_save_path+"/"+sel_file_name, "wb") as file_temp:
        file_temp.write(dec_file_contents)
        
    
    messagebox.Message(title=program_title, message="선택한 파일을 성공적으로 복호화하여 저장하였습니다.").show()

def save_file_show():
    try:
        file_list = os.listdir(abs_file_storage_path)
        json_file_list = [file for file in file_list if file.endswith('.json')]
        
        file_num = 0
        
        print("{:>4s}  {:^40s}  {:^20s}".format("#", "file name", "file save time"))
        
        for file in json_file_list:
            with open(file_storage_path+file, "r") as json_file_contents:
                origin_file_name = json.load(json_file_contents)["file_name"]
            with open(file_storage_path+file, "r") as json_file_contents:
                origin_file_save_time = json.load(json_file_contents)["enc_time"]
                origin_file_save_time = date_word_format(origin_file_save_time)
            
            print("%4d. %-40s %20s" % (file_num+1, origin_file_name, origin_file_save_time))
            file_num += 1
        
    except KeyboardInterrupt:
        print("Cancel Save file show")
        
    print("\n")
    os.system("pause")
    
def program_exit():
    if messagebox.askyesno(program_title, "프로그램을 종료하시겠습니까?") == False:
        return 0
    exit(0)



def del_save_file():
    file_list = os.listdir(abs_file_storage_path)
    json_file_list = [file for file in file_list if file.endswith('.json')]
    
    file_num = 0
    
    print("{:>4s}  {:^40s}  {:^20s}".format("#", "file name", "file save time"))
    for file in json_file_list:
        with open(file_storage_path+file, "r") as json_file_contents:
            origin_file_name = json.load(json_file_contents)["file_name"]
        with open(file_storage_path+file, "r") as json_file_contents:
            origin_file_save_time = json.load(json_file_contents)["enc_time"]
            origin_file_save_time = date_word_format(origin_file_save_time)
        
        print("%4d. %-40s %20s" % (file_num+1, origin_file_name, origin_file_save_time))
        file_num += 1
    
    try:
        file_sel_num = int(input(">> "))-1
    except KeyboardInterrupt:
        print("Cancel input")
        return 0
    except:
        print("Invalid input value")
        return 1
    
    # file id load
    file_num = 0
    for file in json_file_list:
        if file_num == file_sel_num:
            with open(file_storage_path+file, "r") as json_file_contents:
                sel_file_id = json.load(json_file_contents)["file_id"]
            with open(file_storage_path+file, "r") as json_file_contents:
                sel_file_name = json.load(json_file_contents)["file_name"]
            with open(file_storage_path+file, "r") as json_file_contents:
                sel_enc_time = json.load(json_file_contents)["enc_time"]
            break
        file_num += 1
    
    # file delete
    if messagebox.askyesno(program_title, f"선택한 파일 정보\n파일 이름: {sel_file_name}\n저장 시각: {date_word_format(sel_enc_time)}\n\n선택한 파일이 삭제됩니다.\n삭제된 파일은 복구할 수 없습니다.\n계속하시겠습니까?") == False:
        messagebox.Message(title=program_title, message="삭제가 취소되었습니다.").show()
        return 0
    
    exit_code = random.randint(1000, 9999)
    return_exit_code = get_number_box(exit_code)
    
    if return_exit_code != exit_code:
        messagebox.Message(title=program_title, message="숫자가 올바르지 않습니다.\n삭제가 취소되었습니다.").show()
        return
    
    delete_file(file_storage_path+sel_file_id+".json")
    delete_file(file_storage_path+sel_file_id+".enc")

    messagebox.Message(title=program_title, message="선택한 파일이 삭제되었습니다.").show()

def del_save_all_file():
    if messagebox.askyesno(program_title, "저장된 모든 파일들이 삭제됩니다.\n삭제된 파일들은 복구할 수 없습니다.\n계속하시겠습니까?") == False:
        messagebox.Message(title=program_title, message="전체 삭제가 취소되었습니다.").show()
        return 0
    
    exit_code = random.randint(1000, 9999)
    return_exit_code = get_number_box(exit_code)
    
    # 삭제 취소
    if return_exit_code == None:
        messagebox.Message(title=program_title, message="전체 삭제가 취소되었습니다.").show()
        return

    # 숫자 틀림
    if return_exit_code != exit_code:
        messagebox.Message(title=program_title, message="숫자가 올바르지 않습니다.\n전체 삭제가 취소되었습니다.").show()
        return
    
    delete_folder_contents(file_storage_path)
    
    messagebox.Message(title=program_title, message="모든 파일이 삭제되었습니다.").show()

## 본
while True:
    os.system("cls")
    print(program_title)
    print('''
        1. enc file
        2. dec file
        3. save file show
        4. exit
        5. delete file
        6. delete all files
          ''')
    try:
        sel_num = int(input(">> "))
    except KeyboardInterrupt:
        print("Cancel input")
        continue
    except:
        print("Invalid input value")
        continue

    if sel_num == 1:
        enc_files()
        
    elif sel_num == 2:
        dec_file()
    
    elif sel_num == 3:
        save_file_show()
    
    elif sel_num == 4:
        program_exit()
    
    elif sel_num == 5:
        del_save_file()
    
    elif sel_num == 6:
        del_save_all_file()
    