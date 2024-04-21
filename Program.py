from datetime import datetime
import shutil
import os
import json

def list_input(title):
    return input(f"Заполните поле {title} для текущей записи: ")

def notes_import():
    dict1 = (check_file())
    if (dict1 == None or dict1 == []):
        dict1 = dict({'notes': []})
        save_to_json(dict1)
    list1 = {'title': None, 'id_numb': None, 'date': None, 'body': None}
    list1['title'] = list_input('заголовок')
    list1['body'] = list_input('тело заметки')
    list1['id_numb'] = get_id(dict1)
    list1['date'] = get_date()
    dict1['notes'].append(list1)
    save_to_json(dict1)
    print("\nЗапись добавлена, ", end = "")
    show_inf(2)

def check_file():
    try:
        dict1 = import_json()
        if len(dict1.get("notes")) == 0: 
                return []
        else:
            return dict1
    except FileNotFoundError:
        return None
    
def import_json():
    with open('note_list.json', 'r', encoding='utf-8') as f:
        text = json.load(f)
    return text

def save_to_json(python_dict):
    with open('note_list.json', 'w', encoding="utf-8") as file:
        json.dump(python_dict, file, sort_keys=True, indent=2, ensure_ascii=False)

def get_id(dict1):
    if (len(dict1['notes']) == 0): return 1001
    else: return dict1['notes'][-1]['id_numb'] + 1

def get_date():
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

def show_inf(option):
    message1 = "Переход в главное меню"
    message2 = "для продолжения нажмите Enter\n"
    if option == 1: input(f"{message1}, {message2}")
    elif option == 2: input(f"{message2}")

def download_notes():
    path =os.getcwd()
    shutil.copyfile(path + "\\sample.json", path +"\\note_list.json")
    print("Список загружен(заменена всех записей), ", end = "")
    show_inf(2)

def check_input(buttons):
    button = "q"
    while button not in buttons:
        button = input(f"Для выбора введите {buttons[0]}-{buttons[-1]} : ")
        print("")
        if button not in buttons:
            print("Неверное значение. ", end ="")
    return button

def check_file_plus():
    dict1 = check_file()
    count = 0
    if dict1 == []:
        print('Список пуст, ничего не найдено', end ='')
        print("\n")
        show_inf(1)
        return []
    elif dict1 == None:
        print('Заметки отсутствуют, занесите новые данные или загрузите готовый список', end='')
        print("\n")
        show_inf(1)
        return None
    else: return dict1

def display_notes():
    count = 0
    dict1 = check_file_plus()
    if dict1 != None and dict1 != []:
        for i in dict1['notes']:
            count+=1
            print(f"{count}. #{i['id_numb']} {i['date']} {i['title']}: {i['body']}")
        print("")
        show_inf(1)

def input_date():
    filter_menu = "Введите дату в формате dd-mm-YYYY HH:MM"
    print(filter_menu)    
    try:
        return datetime.strptime(input(), "%d-%m-%Y %H:%M")
    except ValueError:
        print('Неверный формат даты, ', end='')
        return None

def show_filter():
    print('Отобразить записи, начиная с введенной временной отсечки:')
    dict1 = check_file_plus()
    if dict1 != None and dict1 != []:
        date1 = None
        while date1 == None:
            date1 = input_date()
        for i in dict1['notes']:
            count = 0
            if date1 < datetime.strptime(i['date'][:-3], "%d-%m-%Y %H:%M"):
                count+=1
                print(f"{count}. #{i['id_numb']} {i['date']} {i['title']}: {i['body']}")
            if count == 0: print('По данному запросу не найденно записей')
        print("")
        show_inf(1)
    
def delete_note():
    count = 0
    dict1 = check_file_plus()
    if dict1 != None and dict1 != []:
        for i in dict1['notes']:
            count+=1
            print(f"{count}. #{i['id_numb']} {i['date']} {i['title']}: {i['body']}")
        choose_list = [str(x) for x in range(1, len(dict1['notes']) + 2)]
        print(f"\nВыберите номер записи для удаления ({choose_list[0]}-{choose_list[-2]}). Для отмены операции нажмите {choose_list[-1]}")
        index = int(check_input(choose_list))
        if index == int(choose_list[-1]):
            print('Отмена удаления записи:')
            show_inf(1)
        else:
            show_record = dict1['notes'].pop(index -1)
            save_to_json(dict1)
            print("")
            print(f"{index}. #{show_record['id_numb']} {show_record['date']} {show_record['title']}: {show_record['body']}")
            print('Запись успешно удалена.')
            show_inf(1)
    
def change_note():
    count = 0
    dict1 = check_file_plus()
    if dict1 != None and dict1 != []:
        for i in dict1['notes']:
            count+=1
            print(f"{count}. #{i['id_numb']} {i['date']} {i['title']}: {i['body']}")
        choose_list = [str(x) for x in range(1, len(dict1['notes']) + 2)]
        print(f"\nВыберите номер записи для изменения ({choose_list[0]}-{choose_list[-2]}). Для отмены операции нажмите {choose_list[-1]}")
        index = int(check_input(choose_list))
        if index == int(choose_list[-1]):
            print('Отмена операции:')
            show_inf(1)
        else:
            list1 = {'title': None, 'id_numb': None, 'date': None, 'body': None}
            print('Введите новые данные для изменённой записи')
            list1['title'] = list_input('заголовок')
            list1['body'] = list_input('тело заметки')
            list1['id_numb'] = get_id(dict1)
            list1['date'] = get_date()
            dict1['notes'].insert(index - 1, list1)
            show_record = dict1['notes'].pop(index)
            save_to_json(dict1)
            print("")
            print(f"{index}. #{show_record['id_numb']} {show_record['date']} {show_record['title']}: {show_record['body']}")
            print('Запись успешно изменена.')
            show_inf(1)
            
def main():
    button = "0"
    button_list = ["1", "2", "3", "4", "5", "6", "7"]
    menu = "Выберите один из вариантов:\n1 - Создать новую заметку\n2 - Загрузить готовый список заметок\n\
3 - Отфильтровать заметки по дате\n4 - Просмотреть все заметки\n5 - Удалить заметку из списка\n\
6 - Редактировать заметку из списка\n7 - Завершить работу\n"
    while button != "7":
        print(f"\n{menu}")
        button = check_input(button_list)
        if button == "1": notes_import()
        elif button == "2": download_notes()
        elif button == "3": show_filter()
        elif button == "4": display_notes()
        elif button == "5": delete_note()
        elif button == "6": change_note()
    print("Конец работы")    
if __name__ == '__main__':
    main()