from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    password_text.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [random.choice(letters) for i in range(random.randint(8, 10))]
    password_symbols = [random.choice(symbols) for i in range(random.randint(2, 4))]
    password_numbers = [random.choice(numbers) for i in range(random.randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    password = "".join(password_list)
    password_text.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def clear():
    website_text.delete(0, END)
    email_user_text.delete(0, END)
    password_text.delete(0, END)


def save():
    website_value = website_text.get()
    email_user_value = email_user_text.get()
    password_value = password_text.get()
    new_data = {
        website_value: {
            "email": email_user_value,
            "password": password_value,
        }
    }

    if not website_value or not email_user_value or not password_value:
        messagebox.showinfo(title="Needs Review!", message="Check again! You have an empty field.")
    else:
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            with open("data.json", "w") as file:
                json.dump(new_data, file, indent=4)
        else:
            data.update(new_data)
            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)
        finally:
            clear()


# ---------------------------- FIND PASSWORD ------------------------------- #

def find_password():
    website_name = website_text.get()
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="No Passwords Found", message="Save passwords to the manager before searching.")
    else:
        if website_name in data:
            email = data[website_name]["email"]
            password = data[website_name]["password"]
            messagebox.showinfo(title=f"{website_name}", message=f"Credential found!\n\nEmail/Username:\n{email}"
                                                                 f"\n\nPassword:\n{password}")
        else:
            messagebox.showinfo(title="Not Found", message="No credential was found for that website.")

# ---------------------------- UI SETUP ------------------------------- #

# window setup
window = Tk()
window.title("Password Manager")
window.config(padx=40, pady=40)

# canvas image setup
canvas = Canvas(width=200, height=200)
lock_image = PhotoImage(file='logo.gif')
canvas.create_image(100, 100, image=lock_image)
# canvas.pack()

# label setup
website_l = Label(text="Website:")
email_user_l = Label(text="Email/Username:")
password_l = Label(text="Password:")

# textbox setup
website_text = Entry(width=35)
email_user_text = Entry(width=35)
password_text = Entry(width=21)

# button setup
generate_password_b = Button(text='Generate Password', width=14, command=generate_password)
add_b = Button(text='Add', width=36, command=save)
search_b = Button(text='Search', width=14, command=find_password)

# object positioning
canvas.grid(column=1, row=0)
website_l.grid(column=0, row=1)
email_user_l.grid(column=0, row=2)
password_l.grid(column=0, row=3)
website_text.grid(column=1, row=1, sticky='EW')
email_user_text.grid(column=1, row=2, columnspan=2, sticky='EW')
password_text.grid(column=1, row=3, sticky='EW')
generate_password_b.grid(column=2, row=3, sticky='EW')
search_b.grid(column=2, row=1, sticky='EW')
add_b.grid(column=1, row=4, columnspan=2, sticky='EW')

website_text.focus()

window.mainloop()
