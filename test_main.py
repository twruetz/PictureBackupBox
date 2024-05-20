#alle files kopieren
#quell laufwerk auswählen
#doppelte erkennen und neu neue files kopieren
#ordner anlegen für jeden tag, anhand bilder meta daten
#ausgabe wieviele files kopiert wurden
#ausgabe wieviele files erkannt wurden, bestätigung ob kopiert werden soll, kopieren und überschreiben? kopieren nur neue?
#sync der daten nach cloud  (an mit mobilen daten, an mit wlan, aus)
#mobile daten verwenden, rest volumen mobile daten anzeigen
#wlan anzeigen und einloggen
#schnittstelle zum handy für eingabe von wlan daten (WIFI?)
#anzeige vom festplatten speicher

#einstellbarmachen welche dateien kopiert werden sollen.
#status leiste: akku stand, festplatten stand, wifi, uhrzeit / datum
#progressbar kopieren

#logging output des ganzen prozesses, 


#wenn foto nicht in ordner einsortiert werden kann, dann in dummy ordner packen
#Signal Anzeige ob alle Daten in die Clound synchronisiert worden sind.
#gerät soll per usb auslesbar sein, also usb host 

#--------------------------Done------------------------------
#datum von file auslesen ordner erstellen mit dem datum.
#zuerst sortieren welche files wohin sollen und dann am ende alle files am stück kopieren, für progress bar

#-------------------------Verworfen--------------------------
#wenn gerät unter 30% akku warnung, wenn gerät unter 10% stop, unter 5% kein anschalten -> Betrieb nur mit Netzstecker



from pathlib import Path
import os
from datetime import datetime
import shutil

def list_files_walk(start_path:Path,list_of_allowed_file_names):
    found_files_dict = {}

    for root, dirs, files in os.walk(start_path):
        for file in files:
            for file_subfix in list_of_allowed_file_names:
                if file.endswith(file_subfix):
                    found_files_dict[file]=os.path.join(root, file)

    return found_files_dict

def create_folders(target_dir:Path,list_of_dates):
    
    for dir_element in list_of_dates:
        temp_dir_path = Path(target_dir,dir_element)
        if os.path.isdir(temp_dir_path):
            print(f"{temp_dir_path} is already there skipping")
        else:
            os.mkdir(temp_dir_path)
            print(f"{temp_dir_path} has been created.")

def check_if_file_already_exists(file_name:str, date_folder:str, target_path:Path):
    file_path_target = Path(target_path,date_folder,file_name)

    if file_path_target.is_file():
        return True
    else:
        return False
    
def copy_batched_files(dict_with_batched_files:dict[Path,Path],device_name:str):
    number_of_files_to_copy : int = len(dict_with_batched_files)
    print(f"Found {number_of_files_to_copy} files in total to copy.")
    file_counter = 0

    for source_path, target_path in dict_with_batched_files.items():
        shutil.copyfile(source_path,target_path)
        file_counter += 1
        print(f"{file_counter}.) {device_name} copied {target_path}.")

    print(f"Copied a total number of {file_counter} files.")

if __name__ == "__main__":
    sd_card_reader_path : Path = Path("E:\\")
    target_path : Path = "D:\\test_target_path"

    list_of_allowed_file_names = [".ORF"]
    batched_files_to_copy = {}

    FLAG_ALWAYS_COPY_REPLACE = False
    FLAG_ALWAYS_COPY = False
    MY_DEVICE = "BackupBox"


    found_files = list_files_walk(sd_card_reader_path,list_of_allowed_file_names)
    

    file_date_dict = {}
    for file_element in found_files:
        unix_timestamp = os.path.getctime(found_files[file_element])
        date_d_m_y = datetime.utcfromtimestamp(unix_timestamp).strftime('%d-%m-%Y')

        file_date_dict[file_element] = date_d_m_y

    folders_to_create_with_doubles = file_date_dict.values()
    folders_to_create = list(set(folders_to_create_with_doubles))

    create_folders(target_path,folders_to_create)

    for file_name in file_date_dict.keys():
        file_date_folder_name = file_date_dict[file_name]

        if (not check_if_file_already_exists(file_name,file_date_folder_name,target_path)) or FLAG_ALWAYS_COPY_REPLACE:
            file_full_target_path = Path(target_path,file_date_folder_name,file_name) 
            batched_files_to_copy[found_files[file_name]] = file_full_target_path
            print(f"{file_full_target_path} added to the copy list.")

        elif FLAG_ALWAYS_COPY:
            file_full_target_path_renamed = Path(target_path,file_date_folder_name,"new_"+file_name)
            batched_files_to_copy[found_files[file_name]] = file_full_target_path_renamed
            print(f"{file_name} is already there. Renaming")

        else:
            print(f"{file_name} is already there. Skipping...")


    if len(batched_files_to_copy) == 0:
        print("There are no files to copy")
    else:
        copy_batched_files(batched_files_to_copy,MY_DEVICE)



    #print(next(scan_dir_object))  	    datetime.utcfromtimestamp(unix_timestamp).strftime('%d-%m-%Y')