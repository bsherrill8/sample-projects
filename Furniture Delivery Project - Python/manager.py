#file contains the class and function for the store as well as code for the Manager screen
import UIcomponents as comp
import tkinter as tk
import csv

class Store:
    
    def __init__(self, daily_inc, weekly_inc, del_ppm):
        self.weekly_inc = weekly_inc
        self.daily_inc = daily_inc
        self.del_ppm = del_ppm

#increases daily income
def add_income(store, price):
    store.daily_inc += price

#adds daily income to weekly income and resets daily
def end_day(store, fields):
    store.weekly_inc += store.daily_inc
    store.daily_inc = 0
    refresh_fields(store, fields)

#resets both daily and weekly income
def end_week(store, fields):
    store.weekly_inc = 0
    store.daily_inc = 0
    refresh_fields(store, fields)

#updates the delivery fee per mile
def update_del(store, price):
    store.del_ppm = price

#saves store information into a simple CSV file to be loaded next time file is opened
def save_info(fields):
    data = (fields[0].get(), fields[1].get(), fields[2].get())    
    with open("store.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)

#updates the text fields with current info
def refresh_fields(store, fields):
    for field in fields:
        field.delete(0, tk.END)

    fields[0].insert(0, "%.2f" % store.daily_inc)
    fields[1].insert(0, "%.2f" % store.weekly_inc)
    fields[2].insert(0, store.del_ppm)

#creates window for manager screen and associated widgets
def mgr_screen(store):
    window = comp.newWindow("Manager Options")
  
    title = comp.newLabel(window, "Manager Options", 16)
    title.grid(column = 2, row = 0,)

    #lists allow labels and fields to be set up in loop and passed into functions together
    labels = ["Daily Income: ", "Weekly Income: ", "Delvery Fee: "]
    fields = []
  
    for text in labels:
        label = comp.newLabel(window, text, 12)
        label.grid(column = 1, row = labels.index(text)+1)
        entry = tk.Entry(window, width = 10)
        fields.append(entry)
        entry.grid(column = 2, row = labels.index(text)+1, sticky="w", columnspan=3)
    
    #updates text fields when window is first opened
    refresh_fields(store, fields)

    #list of buttons to be created and placed by for loop
    btn_names = ["End Day", "End Week", "Update", "Save", "Cancel"]
    buttons = []

    for text in btn_names:
        button = comp.newButton(window, text)
        button.grid(column = 0, row = btn_names.index(text)+1, sticky = "n")
        buttons.append(button)

    #assigns functions to each button
    buttons[0].config(command=lambda: end_day(store, fields))
    buttons[1].config(command=lambda: end_week(store, fields))
    buttons[2].config(command=lambda: update_del(store, float(fields[2].get())))
    buttons[3].config(command=lambda: save_info(fields))
    buttons[4].config(command=window.destroy)
