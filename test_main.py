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

#datum von file auslesen ordner erstellen mit dem datum.

from pathlib import Path
import os
from datetime import datetime

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
            print(f"{temp_dir_path} is already existing skipping")
        else:
            os.mkdir(temp_dir_path)
            print(f"{temp_dir_path} has been created.")
        

if __name__ == "__main__":
    sd_card_reader_path : Path = Path("E:\\")
    target_path : Path = "D:\\test_taget_path"

    list_of_allowed_file_names = [".ORF"]

    found_files = list_files_walk(sd_card_reader_path,list_of_allowed_file_names)

    file_date_dict = {}
    for file_element in found_files:
        unix_timestamp = os.path.getctime(found_files[file_element])
        date_d_m_y = datetime.utcfromtimestamp(unix_timestamp).strftime('%d-%m-%Y')

        file_date_dict[file_element] = date_d_m_y


    folders_to_create_with_doubles = file_date_dict.values()
    folders_to_create = list(set(folders_to_create_with_doubles))
    print(folders_to_create)

    create_folders(target_path,folders_to_create)



    #print(next(scan_dir_object))  	    datetime.utcfromtimestamp(unix_timestamp).strftime('%d-%m-%Y')