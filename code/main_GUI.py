import tkinter as tk
from tkinter import messagebox
import utility
from table_management import create_table, insert_media_table
from suggestion_algorithm import main_algorithm, suggestion_algorithm_single_use, selecting_media, list_of_media_classes
from account_handling import updating_account_data
from filters import filters, Filters
import webbrowser

bg_col: str = "grey"
fg_col: str = "white"
button_col: str = "dark grey"

global_likes_to_save = []


def link_callback(event):
    webbrowser.open_new(event.widget.cget("text"))


def pop_up_window(root, retail_link):
    pop_up = tk.Toplevel(root, bg=bg_col)
    pop_up.title = "Purchase item"
    pop_up.geometry("600x400")

    page_title = tk.Label(pop_up, text="VMedia: Retail assistant", font=("arial", 15, "bold"), fg=fg_col, bg=bg_col)
    page_title.place(relx=0.5, rely=0.05, anchor=tk.CENTER)
    utility.underline(page_title)

    link_label = tk.Label(pop_up, cursor="hand2", text=retail_link,
                          font=("arial", 15), fg="blue", bg=bg_col, wraplength=500)
    link_label.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.2)
    link_label.bind("<Button-1>", link_callback)


def select_media(root, table, likes_to_save, searched_item, filter_obj):
    cur_item = table.focus()
    row_data: dict = table.item(cur_item)
    item_values: list = row_data['values']
    selected_title = item_values[0]
    try:
        media_selected, likes_to_save = selecting_media(likes_to_save, selected_title)
    except TypeError:
        # Bug occurs when items are not found however it is unclear what causes items to not be found
        # As of now, only two items are known to cause this bug (both have been removed)
        messagebox.showinfo(message="ERROR: The item you requested was not found in"
                                    " our database. Sorry for the inconvenience")

    global global_likes_to_save
    global_likes_to_save = likes_to_save
    selected_data = media_selected.data

    pop_up_window(root, media_selected.retail_link)  # Display link to buy object

    updating_gui(table, selected_data, searched_item, filter_obj)


def clearing_table(table):
    for x in table.get_children():
        table.delete(x)


def updating_gui(table, media_data_to_set_scores, searched_item, filter_obj):
    clearing_table(table)
    main_algorithm(media_data_to_set_scores)
    search(table, searched_item, filter_obj)


def search(table, searched_item, filter_obj=None):

    clearing_table(table)
    filtered_data = [media for media in list_of_media_classes if searched_item.lower() in media.title.lower()]

    if filter_obj is not None:
        filter_list: list[str] = filter_obj.get_filters()
        if filter_list:
            for chosen_filter in filter_list:
                filtered_data = [media for media in filtered_data if chosen_filter in media.genres]

    insert_media_table(table, filtered_data)

#     search_button.place(relx=0.395, rely=0.15, relwidth=0.05, relheight=0.025)
#     show_all_button.place(relx=0.455, rely=0.15, relwidth=0.05, relheight=0.025)
#     exit_button.place(relx=0.8, rely=0.05, relwidth=0.1, relheight=0.05)


def suggestion_gui(root, account_data, account_found):
    utility.clear_root(root)
    title = tk.Label(root, text="VMedia: Suggestions", font=("arial", 28, "bold"), fg=fg_col, bg=bg_col)
    title.place(relx=0.5, rely=0.05, anchor=tk.CENTER)
    utility.underline(title)

    table = create_table(root)
    table.place(relx=0.1, rely=0.2, relwidth=0.40, relheight=0.75)
    scroll_bar_y = tk.Scrollbar(root, command=table.yview)
    scroll_bar_y.place(relx=0.5, rely=0.2, relheight=0.75)

    select_button = tk.Button(root, text="Select media", font=("arial", 10, "bold"),
                              bg=button_col, command=lambda:
                              select_media(root, table, likes_to_save,
                                           search_bar.get(), filter_obj))
    select_button.place(relx=0.5, rely=0.1, relwidth=0.04, relheight=0.025, anchor=tk.CENTER)

    search_bar = tk.Entry(root, relief=tk.GROOVE, bd=2, font=("arial", 13))
    search_bar.place(relx=0.1, rely=0.15, relwidth=0.68, relheight=0.025)

    search_button = tk.Button(root, text="Search", font=("arial", 10, "bold"), bg=button_col,
                              command=lambda: search(table, search_bar.get(), filter_obj))
    search_button.place(relx=0.8, rely=0.15, relwidth=0.04, relheight=0.025)

    show_all_button = tk.Button(root, text="Show All", font=("arial", 10, "bold"),
                                bg=button_col, command=lambda: search(table, ""))
    show_all_button.place(relx=0.85, rely=0.15, relwidth=0.04, relheight=0.025)

    exit_button = tk.Button(root, text="Exit", font=("arial", 10, "bold"),
                            bg=button_col, command=lambda: updating_account_data(account_found, likes_to_save))
    exit_button.place(relx=0.8, rely=0.05, relwidth=0.09, relheight=0.05)

    filters_label = tk.Label(root, text="Filters:", font=("arial", 25, "bold"), fg=fg_col, bg=bg_col)
    filters_label.place(relx=0.60, rely=0.25)
    utility.underline(filters_label)

    filter_obj = Filters()
    filters(root, filter_obj)

    if account_data == ['']:
        account_data = []

    # A second list is made so media already used to calculate score do not need to be checked again
    likes_to_save: list[int] = [int(x) for x in account_data]
    global global_likes_to_save
    global_likes_to_save = likes_to_save

    media_data_to_set_scores = suggestion_algorithm_single_use(likes_to_save)

    ordered_media_classes = main_algorithm(media_data_to_set_scores)
    insert_media_table(table, ordered_media_classes)
