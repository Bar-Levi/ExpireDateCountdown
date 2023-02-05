from tkinter import *
from collections import defaultdict
from datetime import datetime

LANGUAGE = "Hebrew"

if LANGUAGE == "Hebrew":
    justifying_side = 'right'
elif LANGUAGE == "English":
    justifying_side = 'left'

WIN = Tk()
WIN.resizable(False, False)
SCREEN_WIDTH = WIN.winfo_screenwidth()
SCREEN_HEIGHT = WIN.winfo_screenheight()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BACKGROUND_COLOR = "lightblue"
BUTTONS_COLOR = 'blue'
invalid_date = False
RETURN_ICON = PhotoImage(file="Assets/backward.png")
Expiration_Bounds = [3, 8]


def def_value():
    return []


def CheckValidation(day=0, month=0, year=0):

    def isLeap():
        if year % 4 == 0:
            if year % 100 == 0:
                if year % 400 == 0:
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False

    try:
        day, month, year = int(day), int(month), int(year)
    except:
        return False
    days_count = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    if not (year > 1):
        return False
    if not (1 <= month <= 12):
        return False
    if (isLeap() and month == 2 and day <= 29) or (not isLeap() and month == 2 and day <= 28):  # Handle February
        return True
    if not (0 < day <= days_count[month]):
        return False
    if DaysLeftUntilExpiration('{0}.{1}.{2}'.format(day, month, year)) < 0:
        return False
    if year - datetime.today().year > 1000:
        return False
    return True

NAMES_DATES = {}
DATES_NAMES = {}

def DaysLeftUntilExpiration(date):
    date = datetime.strptime(date, "%d.%m.%Y")
    today = datetime.today()
    today = "{0}.{1}.{2}".format(today.day, today.month, today.year)
    today = datetime.strptime(today, "%d.%m.%Y")
    return (date - today).days


def CenterWindow(window):
    center_x = int(SCREEN_WIDTH / 2 - WINDOW_WIDTH / 2)
    center_y = int(SCREEN_HEIGHT / 2 - WINDOW_HEIGHT / 2)

    return f'800x600+{center_x}+{center_y}'  # Placing the window at the middle of the screen.


def AddProduct():
    for feature in WIN.winfo_children():
        feature.pack_forget()
    WIN.title("הוספת פריטים")
    return_button = Button(WIN, image=RETURN_ICON, command=Home)
    return_button.pack(anchor="w")
    command_label = Label(WIN, text=":סוג הפריט", font=(None, 20), fg="blue", bg="white")
    command_label.pack()
    name_textbox = Entry(WIN, width=50, justify='center')
    name_textbox.pack()
    command_label = Label(WIN, text=":תוקף", font=(None, 20), fg="blue", bg="white")
    command_label.pack()
    date_textbox = Entry(WIN, width=50, justify='center')
    date_textbox.pack()
    Label(WIN).pack()
    search_list = Listbox(WIN, width=50, height=22, justify=justifying_side)
    search_list.pack()
    WIN.update()


    def AutoFillName(e):
        name_textbox.delete(0, END)
        try:
            name_textbox.insert(0, search_list.get(e.widget.curselection()[0]))
        except:
            print("Tuple index out of range.")

    def UpdateName(e):
        current_name = name_textbox.get()
        if current_name == "":
            UpdateSearchList()
        else:
            UpdateSearchList(current_name)

    def UpdateSearchList(n=""):
        search_list.delete(0, END)
        for name in NAMES_DATES:
            if n in name:
                search_list.insert(END, name)

    UpdateSearchList()
    search_list.bind("<<ListboxSelect>>", AutoFillName)
    name_textbox.bind("<KeyRelease>", UpdateName)

    def SaveProduct():
        global NAMES_DATES, invalid_date
        optional_chars = [',', '/', ' ']
        product_name = name_textbox.get().strip()
        for c in optional_chars:
            product_date = date_textbox.get().replace(c, ".")
        product_date = product_date.split(".")
        for i in range(len(product_date), 3):
            product_date.append(" ")
        if not CheckValidation(product_date[0], product_date[1], product_date[2]):
            invalid_date = True
            AddProduct()
        else:
            product_date = ".".join((product_date[0], product_date[1], product_date[2]))
            try:
                NAMES_DATES[product_name].append(str(product_date))
            except:
                NAMES_DATES[product_name] = []
            try:
                DATES_NAMES[product_date].append(str(product_name))
            except:
                DATES_NAMES[product_date] = []
                NAMES_DATES[product_name].append(str(product_date))
                DATES_NAMES[product_date].append(str(product_name))

            invalid_date = False
            UpdateChanges()
            AddProduct()

    save_button = Button(WIN, text="הוספת מוצר", font=(None, 20),fg=BUTTONS_COLOR, bg="light gray", command=SaveProduct)
    save_button.pack()
    if invalid_date:
        Label(WIN, text=".תאריך שגוי, אנא נסה שנית", fg='red').pack()
        Label(WIN).pack(side='bottom')
    WIN.mainloop()


def ShowDates():
    global WIN
    for feature in WIN.winfo_children():
        feature.pack_forget()
    return_button = Button(WIN, image=RETURN_ICON, command=Home)
    return_button.pack(anchor="w")
    WIN.title("סטטוס פריטים")
    command_label = Label(WIN, text=":חפש פריט", font=(None, 20), fg="blue")
    command_label.pack()
    name_textbox = Entry(WIN, width=50, justify=justifying_side)
    name_textbox.pack()
    Label(WIN).pack()
    search_list = Listbox(WIN, width=50, height=26, justify=justifying_side, selectmode=BROWSE)
    search_list.pack()
    WIN.update()

    def DeleteProduct():
        try:
            product = name_textbox.get().split('-')
            product_name = product[0].strip()
            product_date = product[1][1:-1].split(' ')[0]
            DATES_NAMES[product_date].remove(product_name)
            NAMES_DATES[product_name].remove(product_date)
            UpdateChanges()
            name_textbox.delete(0, END)
            UpdateSearchList()
        except:
            pass

    def AutoFillName(e):
        name_textbox.delete(0, END)
        try:
            name_textbox.insert(0, search_list.get(e.widget.curselection()[0]))
        except:
            print("Tuple index out of range.")

    def UpdateName(e):
        current_name = name_textbox.get()
        if current_name == "":
            UpdateSearchList()
        else:
            UpdateSearchList(current_name)

    def UpdateSearchList(n=""):
        inserted_items = defaultdict(def_value)
        search_list.delete(0, END)
        sorted_dates = sorted(list(DATES_NAMES.keys()), key=lambda x: DaysLeftUntilExpiration(x))
        for date in sorted_dates:
            difference = DaysLeftUntilExpiration(date)
            for product in DATES_NAMES[date]:
                if n.lower() in product.lower() and inserted_items[product] != 1:
                    search_list.insert(END, product + " - " + str(date) + " ({0})".format(difference))
                    inserted_items[product] = 1
                    if difference < Expiration_Bounds[0]:
                        search_list.itemconfig(search_list.size() - 1, bg='red', foreground='white')
                    elif difference < Expiration_Bounds[1]:
                        search_list.itemconfig(search_list.size() - 1, bg='yellow', foreground='black')
                    else:
                        search_list.itemconfig(search_list.size() - 1, bg='green', foreground='white')

    UpdateSearchList()
    search_list.bind("<<ListboxSelect>>", AutoFillName)
    name_textbox.bind("<KeyRelease>", UpdateName)
    delete_button = Button(WIN, text="הסר פריט", font=(None, 20), command=DeleteProduct, fg=BUTTONS_COLOR)
    delete_button.pack()
    WIN.update()
    WIN.mainloop()


def UpdateChanges():
    SaveData()
    LoadData()


def SaveData():
    file = open("products_dates.txt", 'w')
    file.write(str(NAMES_DATES)+'\n'+str(DATES_NAMES))
    file.close()


def LoadData():
    global DATES_NAMES, NAMES_DATES
    try:
        file = open("products_dates.txt", 'r')
        data = file.read().split('\n')
        if data == [""]:
            pass
        else:
            NAMES_DATES = eval(data[0])
            DATES_NAMES = eval(data[1])
    except Exception as e:
        print(e)




def Home():
    global WIN
    LoadData()
    for feature in WIN.winfo_children():
        feature.pack_forget()
    WIN.title("מסך הבית")
    WIN.geometry(CenterWindow(WIN))
    Label(WIN, text="My Supermarket",font=("Helvetica", 40), fg='black').pack(fill='x', side='top', expand=True)
    search_button = Button(WIN, text="הוספת מוצר", font=(None, 25), fg=BUTTONS_COLOR, width=int(WINDOW_WIDTH*0.75), command=AddProduct)
    search_button.pack(side='bottom', fill='both', expand=True)
    show_closest_button = Button(WIN, text="הצג את התאריכים", fg=BUTTONS_COLOR, font=(None, 25), width=int(WINDOW_WIDTH*0.75), command=ShowDates)
    show_closest_button.pack(side='bottom', fill='both', expand=True)
    WIN.mainloop()


if __name__ == "__main__":
    Home()
