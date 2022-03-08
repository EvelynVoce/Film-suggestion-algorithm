import tkinter as tk
import utility
import hashlib
import Password_validation
import csv
import os

bg_col: str = "grey"
fg_col: str = "white"
button_col: str = "dark grey"

script_dir = os.path.dirname(__file__)  # Script directory
script_dir, _ = script_dir.rsplit('\\', 1)  # Won't run correctly when running this file but will when running main
accounts_file_path = os.path.join(script_dir, 'user_data.csv')


def writing_account(signup_username, signup_password):
    if os.path.isfile(accounts_file_path):  # If the file exists, append new account to the file
        with open(accounts_file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([signup_username, signup_password])

    else:  # If the file doesn't exist, create the file
        with open(accounts_file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Username", "Password", "Viewed items"])
            writer.writerow([signup_username, signup_password])


def hashing(data_to_encrypt) -> str:
    SALT: str = "AbX2f8Z&1SVFHUB4UZPW"
    plus_salt: str = data_to_encrypt + SALT
    hashed_data: str = hashlib.sha256(plus_salt.encode()).hexdigest()
    return hashed_data


def create_account(signup_username: str, signup_password: str):
    checks_passed: bool = Password_validation.run_checks(signup_password)  # Password validation
    if checks_passed:
        hashed_password: str = hashing(signup_password)
        writing_account(signup_username, hashed_password)


def signup_screen(root, func):
    signup_title = tk.Label(root, text="VMedia: Signup", font=("arial", 28, "bold"), fg=fg_col, bg=bg_col)
    signup_title.place(relx=0.5, rely=0.05, anchor=tk.CENTER)
    utility.underline(signup_title)

    back_button = utility.create_back_button(root)
    back_button.config(command=lambda: utility.clear_root(root) or func())

    username_label = tk.Label(root, text="Username:", font=("arial", 15, "bold"), fg=fg_col, bg=bg_col)
    username_label.place(relx=0.05, rely=0.25)
    signup_username_entry = tk.Entry(root, relief=tk.GROOVE, bd=2, font=("arial", 13))
    signup_username_entry.place(relx=0.20, rely=0.25, relwidth=0.2, relheight=0.05)

    password_label = tk.Label(root, text="Password:", font=("arial", 15, "bold"), fg=fg_col, bg=bg_col)
    password_label.place(relx=0.05, rely=0.35)
    signup_password_entry = tk.Entry(root, relief=tk.GROOVE, bd=2, font=("arial", 13), show="*")
    signup_password_entry.place(relx=0.20, rely=0.35, relwidth=0.2, relheight=0.05)

    submit_details = tk.Button(root, text="signup", font=("arial", 10, "bold"),
                               bg=button_col, command=lambda:
                               create_account(signup_username_entry.get(), signup_password_entry.get()))
    submit_details.place(relx=0.20, rely=0.75, relwidth=0.2, relheight=0.05)
