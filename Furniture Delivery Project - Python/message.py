import tkinter as tk
#from tkinter import messagebox
from database import Database

# Instanciate databse object
db = Database('store.db')

# Main Application/GUI class


class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        master.title('Family Furniture & Mattress')
        # Width height
        master.geometry("700x350")
        # Create widgets/grid
        self.create_widgets()
        # Init selected item var
        self.selected_item = 0
        # Populate initial list
        self.populate_list()

    def create_widgets(self):
        # Part
        self.furniture_text = tk.StringVar()
        self.furniture_label = tk.Label(
            self.master, text='Item name', font=('bold', 14), pady=20)
        self.furniture_label.grid(row=0, column=0, sticky=tk.W)
        self.furniture_entry = tk.Entry(self.master, textvariable=self.furniture_text)
        self.furniture_entry.grid(row=0, column=1)
        # Customer
        self.customer_text = tk.StringVar()
        self.customer_label = tk.Label(
            self.master, text='Customer', font=('bold', 14))
        self.customer_label.grid(row=0, column=2, sticky=tk.W)
        self.customer_entry = tk.Entry(
            self.master, textvariable=self.customer_text)
        self.customer_entry.grid(row=0, column=3)
        # employee
        self.employee_text = tk.StringVar()
        self.employee_label = tk.Label(
            self.master, text='Employee', font=('bold', 14))
        self.employee_label.grid(row=1, column=0, sticky=tk.W)
        self.employee_entry = tk.Entry(
            self.master, textvariable=self.employee_text)
        self.employee_entry.grid(row=1, column=1)
        # Price
        self.price_text = tk.StringVar()
        self.price_label = tk.Label(
            self.master, text='Price', font=('bold', 14))
        self.price_label.grid(row=1, column=2, sticky=tk.W)
        self.price_entry = tk.Entry(self.master, textvariable=self.price_text)
        self.price_entry.grid(row=1, column=3)

        # Parts list (listbox)
        self.furniture_list = tk.Listbox(self.master, height=8, width=50, border=0)
        self.furniture_list.grid(row=3, column=0, columnspan=3,
                             rowspan=6, pady=20, padx=20)
        # Create scrollbar
        self.scrollbar = tk.Scrollbar(self.master)
        self.scrollbar.grid(row=3, column=3)
        # Set scrollbar to parts
        self.furniture_list.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.furniture_list.yview)

        # Bind select
        self.furniture_list.bind('<<ListboxSelect>>', self.select_item)

        # Buttons
        self.add_btn = tk.Button(
            self.master, text="Add Furniture", width=12, command=self.add_item)
        self.add_btn.grid(row=2, column=0, pady=20)

        self.remove_btn = tk.Button(
            self.master, text="Remove Item", width=12, command=self.remove_item)
        self.remove_btn.grid(row=2, column=1)

        self.update_btn = tk.Button(
            self.master, text="Update Inventory", width=12, command=self.update_item)
        self.update_btn.grid(row=2, column=2)

        self.exit_btn = tk.Button(
            self.master, text="Clear Input", width=12, command=self.clear_text)
        self.exit_btn.grid(row=2, column=3)

    def populate_list(self):
        # Delete items before update. So when you keep pressing it doesnt keep getting (show example by calling this twice)
        self.furniture_list.delete(0, tk.END)
        # Loop through records
        for row in db.fetch():
            # Insert into list
            self.furniture_list.insert(tk.END, row)

    # Add new item
    def add_item(self):
        if self.furniture_text.get() == '' or self.customer_text.get() == '' or self.employee_text.get() == '' or self.price_text.get() == '':
            tk.messagebox.showerror(
                "Required Fields", "Please include all fields")
            return
        print(self.furniture_text.get())
        # Insert into DB
        db.insert(self.furniture_text.get(), self.customer_text.get(),
                  self.employee_text.get(), self.price_text.get())
        # Clear list
        self.furniture_list.delete(0, tk.END)
        # Insert into list
        self.furniture_list.insert(tk.END, (self.furniture_text.get(), self.customer_text.get(
        ), self.employee_text.get(), self.price_text.get()))
        self.clear_text()
        self.populate_list()

    # Runs when item is selected
    def select_item(self, event):
        # # Create global selected item to use in other functions
        # global self.selected_item
        try:
            # Get index
            index = self.furniture_list.curselection()[0]
            # Get selected item
            self.selected_item = self.furniture_list.get(index)
            # print(selected_item) # Print tuple

            # Add text to entries
            self.furniture_entry.delete(0, tk.END)
            self.furniture_entry.insert(tk.END, self.selected_item[1])
            self.customer_entry.delete(0, tk.END)
            self.customer_entry.insert(tk.END, self.selected_item[2])
            self.employee_entry.delete(0, tk.END)
            self.employee_entry.insert(tk.END, self.selected_item[3])
            self.price_entry.delete(0, tk.END)
            self.price_entry.insert(tk.END, self.selected_item[4])
        except IndexError:
            pass

    # Remove item
    def remove_item(self):
        db.remove(self.selected_item[0])
        self.clear_text()
        self.populate_list()

    # Update item
    def update_item(self):
        db.update(self.selected_item[0], self.furniture_text.get(
        ), self.customer_text.get(), self.employee_text.get(), self.price_text.get())
        self.populate_list()

    # Clear all text fields
    def clear_text(self):
        self.furniture_entry.delete(0, tk.END)
        self.customer_entry.delete(0, tk.END)
        self.employee_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)


root = tk.Tk()
app = Application(master=root)
app.mainloop()