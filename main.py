from datetime import date
from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import sqlite3
import csv
from tkinter import filedialog as fd
from tkcalendar import Calendar, DateEntry

RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
BLACK = "#000000"
BLUE = "#0995FF"
BACKGROUND = "#ECECEC"
FONT_NAME = "Courier"


# ---------------------------- Functions ------------------------------- #

def import_file():
    try:
        name = fd.askopenfilename()

        file = open(name, mode='r')
        csvReader = csv.reader(file)

        fields = next(csvReader)
        for row in csvReader:
            conn.execute(
                f"INSERT INTO VACCINES (FName,LName,Sex,ID,YOB,TOV,DT,PhoneNO)  VALUES ('{row[0]}', '{row[1]}', '{row[2]}', '{row[3]}', {row[4]}, '{row[5]}', '{row[6]}', '{row[7]}');");
            conn.commit()
    except Exception as error:
        print(error)
        messagebox.showerror(title='Error', message="error happened")
    else:
        messagebox.showerror(title='Done', message="Importing done successfully")


def export_db():
    try:
        name = fd.askdirectory()

        file = open(name + "/VaccinationDB.csv", mode="w")
        csvWriter = csv.writer(file)

        csvWriter.writerow(['FName', 'LName', 'Sex', 'ID', 'YOB', 'TOV', 'DT', 'PhoneNO'])  # writing the fields

        Vaccination = conn.execute(
            f"SELECT FName,LName,Sex,ID,YOB,TOV,DT,PhoneNO from VACCINES")

        for row in Vaccination:
            csvWriter.writerow(list(row))

    except Exception as error:
        print(error)
        messagebox.showerror(title='Error', message="error happened")
    else:
        messagebox.showerror(title='Done', message="Exporting done successfully")


def check_id():
    if len(check_id_field.get()) == 10:
        Vaccination = conn.execute(
            f"SELECT FName,LName,Sex,ID,YOB,TOV,DT,PhoneNO from VACCINES where ID == {check_id_field.get()}")

        counter = 0
        for row in Vaccination:
            counter += 1

        # Create a photoimage object of the image in the path
        if counter == 0:
            image1 = Image.open("states/unvaccinated.png")
        elif counter >= 2:
            image1 = Image.open("states/Fully_Vaccinated.png")
        elif counter == 1:
            image1 = Image.open("states/Vaccinated.png")
        test = ImageTk.PhotoImage(image1)

        label1 = ttk.Label(tab2, image=test)
        label1.image = test

        label1.grid(column=1, row=0)
        # Position image
    else:
        messagebox.showerror(title='Error', message="The ID should be 10 digits")


# radio button function
def check_num_doses():
    Vaccination = conn.execute(
        f"SELECT FName,LName,Sex,ID,YOB,TOV,DT,PhoneNO from VACCINES where ID == {id_field.get()}")
    doses_counter = 0
    for _ in Vaccination:
        doses_counter += 1

    return doses_counter


# add user to the DB
def add_v_user():
    if len(first_name_field.get()) == 0 or len(last_name_field.get()) == 0 or len(str(gender.get())) == 0 or len(
            str(gender.get())) == 0 or chosen_year.get() == 0 or \
            str(chosen_Vaccine.get()) == 'Choose here' or str(chosen_Vaccine.get()) == 'Vaccine Type':
        messagebox.showerror(title='Error', message="Please don't leave any field empty!")
    elif len(str(id_field.get())) < 10 or len(str(phone_number_field.get())) < 10:
        messagebox.showerror(title='Error', message="The ID and phone should be 10 digits")
    elif 0 > int(hour.get()) or int(hour.get()) > 12:
        messagebox.showerror(title='Error', message="The hour must be grater then 0 and less then 12")
    elif 0 > int(mins.get()) or int(mins.get()) > 59:
        messagebox.showerror(title='Error', message="The mints must be grater then 0 and less then 59")
    elif check_num_doses() >= 2:
        messagebox.showerror(title='Error',
                             message=f"the user with the {id_field.get()} is Fully Vaccinated you can't add more.")
    else:
        print('correct')
        fix_date()

        try:
            conn.execute(
                f"INSERT INTO VACCINES (FName,LName,Sex,ID,YOB,TOV,DT,PhoneNO)  VALUES ('{first_name_field.get()}', '{last_name_field.get()}', '{str(gender.get())}', '{str(id_field.get())}', {chosen_year.get()}, '{chosen_Vaccine.get()}', '{str(chosen_date)} {str(hour.get())}:{str(mins.get())} {chosen_time.get()}', '{str(phone_number_field.get())}');");

            conn.commit()

            messagebox.showerror(title='Done', message="Add vaccine successfully")
            first_name_field.delete(0, END)
            last_name_field.delete(0, END)
            id_field.delete(0, END)
            phone_number_field.delete(0, END)
        except Exception as error:
            print(error)
            messagebox.showerror(title='Error', message="Error happened!")


def fix_date():
    global chosen_date
    try:
        chosen_date = str(chosen_date.selection_get()).split('-')
        chosen_date = f"{chosen_date[2]}/{chosen_date[1]}/{chosen_date[0]}"
        print(chosen_date)
    except Exception as error:
        print(error)


def calendar():
    global chosen_date

    top = tk.Toplevel(window)

    chosen_date = Calendar(top,
                           font="Arial 14", selectmode='day',
                           cursor="hand1", year=date.today().year, month=date.today().month, day=date.today().day)
    chosen_date.pack(fill="both", expand=True)
    ok_button = Button(top, text="ok", command=fix_date).pack()


# ok_button.grid(column=1, row=4)


# ---------------------------- DB SETUP ------------------------------- #

conn = sqlite3.connect('centralDB.db')
print("Opened database successfully")

try:

    conn.execute('''CREATE TABLE VACCINES
                (FName TEXT NOT NULL,
                LName TEXT NOT NULL,
                Sex TEXT NOT NULL,
                ID TEXT NOT NULL,
                YOB INT NOT NULL,
                TOV TEXT NOT NULL,
                DT TEXT NOT NULL,
                PhoneNO TEXT NOT NULL);''')

except Exception as error:
    print(error)

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title('Covid-19 Vaccination')

# ---------------------------- tabs ---------------------------- #

style = ttk.Style()
textStyle = "BW.TLabel"
style.configure(textStyle, foreground="black", background="white", padding=5, font=('Courier', 15), )

tabControl = ttk.Notebook(window)

tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)

tabControl.add(tab1, text='Check-in')
tabControl.add(tab2, text='Immunity Check')
tabControl.add(tab3, text='Import & Export')

tk.Grid.rowconfigure(window, 2, weight=5)
tk.Grid.columnconfigure(window, 2, weight=5)
tabControl.grid(column=0, row=0, sticky=tk.E + tk.W + tk.N + tk.S)

#
# -------------------------------------------------- Tab 1 -------------------------------------------------- #
#

# -------------- first name row -------------- #
first_name = ttk.Label(tab1, text='First name:', style=textStyle)
first_name.grid(column=0, row=1)

first_name_field = ttk.Entry(tab1)
first_name_field.focus()
first_name_field.grid(column=1, row=1, columnspan=2)

# -------------- last name row -------------- #
last_name = ttk.Label(tab1, text='Last name:', style=textStyle)
last_name.grid(column=0, row=2)

last_name_field = ttk.Entry(tab1)
last_name_field.focus()
last_name_field.grid(column=1, row=2, columnspan=2)

# -------------- radio Buttons -------------- #

gender_label = ttk.Label(tab1, text='Sex:', style=textStyle)
gender_label.grid(column=0, row=3)
# variable to store the gender
gender = StringVar(window, "")

# male radio button
male_radioButton = ttk.Radiobutton(tab1, text="Male", variable=gender, value='Male')
male_radioButton.grid(column=1, row=3, columnspan=1)

# female radio button
female_radioButton = ttk.Radiobutton(tab1, text="Female", variable=gender, value='Female')
female_radioButton.grid(column=2, row=3, columnspan=1)

# -------------- ID row -------------- #
id_label = ttk.Label(tab1, text='id:', style=textStyle)
id_label.grid(column=0, row=4)

id_field = ttk.Entry(tab1)
id_field.focus()
id_field.grid(column=1, row=4, columnspan=2)

# -------------- drop down menu --------------
# list of years
years = []

# building the years
starting_year = 1900
for index in range(104):
    years.append(starting_year + index)

years.reverse()
years.insert(0, '0000')
# chosen year
chosen_year = IntVar()
chosen_year.set(0000)
# drop down label
barth_year_label = ttk.Label(tab1, text='Year of barth:', style=textStyle)
barth_year_label.grid(column=0, row=5)

# years drop down menu
barth_year_drop = ttk.OptionMenu(tab1, chosen_year, *years)
barth_year_drop.grid(column=1, row=5, columnspan=2)

# -------------- Type of Vaccine --------------
Vaccine_type = ['Vaccine Type', 'Pfizer', 'AstraZeneca', 'Moderna', 'J&J']

chosen_Vaccine = StringVar()
chosen_Vaccine.set("Choose here")

Vaccine_type_label = ttk.Label(tab1, text='Type of Vaccine:', style=textStyle)
Vaccine_type_label.grid(column=0, row=6)

Vaccine_type_drop = ttk.OptionMenu(tab1, chosen_Vaccine, *Vaccine_type)
Vaccine_type_drop.grid(column=1, row=6, columnspan=2)

# -------------- calendar -------------- #

# date picker
chosen_date = f'{date.today().day}/{date.today().month}/{date.today().year}'
calendar_label = ttk.Label(tab1, text='Date & Time: ', style=textStyle)
calendar_label.grid(column=0, row=8)

calendar_button = ttk.Button(tab1, text='Calendar', command=calendar)
calendar_button.grid(column=1, row=8)

# time picker
times = ['PM', 'PM', 'AM']

chosen_time = StringVar()
chosen_time.set("PM")

time_drop = ttk.OptionMenu(tab1, chosen_time, *times)
time_drop.grid(column=4, row=8)

hour = tk.Spinbox(tab1, from_=00, to=12, width=5)
hour.grid(column=2, row=8)
mins = tk.Spinbox(tab1, from_=0, to=59, width=5)
mins.grid(column=3, row=8)

# -------------- Phone number -------------- #

phone_number = ttk.Label(tab1, text='Phone Number:', style=textStyle)
phone_number.grid(column=0, row=9)

phone_number_field = ttk.Entry(tab1)
phone_number_field.focus()
phone_number_field.grid(column=1, row=9, columnspan=2)

# -------------- Submit Button -------------- #

submit_button = ttk.Button(tab1, text='Submit', command=add_v_user)
submit_button.grid(column=1, row=10, columnspan=2)

#
# -------------------------------------------------- Tab 1 -------------------------------------------------- #
#


check_id_label = ttk.Label(tab2, text='ID: ', style=textStyle)
check_id_label.grid(column=0, row=1, padx=35, pady=55)

check_id_field = ttk.Entry(tab2)
check_id_field.grid(column=1, row=1, columnspan=2)

submit_button = ttk.Button(tab2, text='Check', command=check_id)
submit_button.grid(column=0, row=2, ipadx=70, columnspan=4)

# -------------------------------------------------- Tab 3 -------------------------------------------------- #

# directory_label = ttk.Label(tab3, text="Directory: ", style=textStyle)
# directory_label.grid(column=0, row=0, padx=35, pady=55)
#
# directory_field = ttk.Entry(tab3)
# directory_field.grid(column=1, row=0)

import_button = ttk.Button(tab3, text="Import", command=import_file)
import_button.grid(column=1, row=0, padx=100, pady=100)

export_button = ttk.Button(tab3, text="Export", command=export_db)
export_button.grid(column=2, row=0, padx=35, pady=100)

# -------------- End of the UI and to keep the screen work --------------#
window.mainloop()
