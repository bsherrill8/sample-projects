import tkinter as tk
import UIcomponents as comp
import database, customer, furniture, order, manager, csv

#opens the csv file and reads in the saved store information to build the store object
with open("store.csv","r") as file:
    data = csv.reader(file)
    for line in data:
        store_info = line
    store = manager.Store(float(store_info[0]), float(store_info[1]), float(store_info[2]))

#connects program to the database
db = database.Database("furniture.db")

#opens main menu window
menu = tk.Tk()
menu.title("Furniture Delivery Inc")
menu.configure(bg="lightsteelblue")
width = 700
height = 500
menu.geometry("%dx%d" % (width, height))

#builds the layout grid for aligning widgets
for column in range(5):
    menu.columnconfigure(column, weight = 1)
for row in range(6):
    menu.rowconfigure(row, weight = 1)

title = comp.newLabel(menu, "Main Menu", 16)
title.grid(column = 2, row = 0)

#creates and places Customer button
btn_customer = tk.Button(
    width = 10,
    text = "Customers",
    command = lambda: customer.cust_screen(db)
)
btn_customer.grid(column = 2, row = 1)

#creates and places Furniture button
btn_furniture = tk.Button(
    width = 10,
    text="Furniture",
    command = lambda: furniture.furn_screen(db)
)
btn_furniture.grid(column = 2, row = 2)

#creates and places Orders button
btn_order = tk.Button(
    width = 10,
    text="Orders",
    command = lambda: order.ord_screen(db, store)
)
btn_order.grid(column = 2, row = 3)

#creates and places Manager button
btn_store = tk.Button(
    width = 10,
    text="Manager",
    command = lambda: manager.mgr_screen(store)
)
btn_store.grid(column = 2, row = 4)

tk.mainloop()