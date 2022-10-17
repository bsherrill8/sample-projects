#this file contains the class and functions for the customer objects as well as the code for the customer screen

import UIcomponents as comp
import tkinter as tk


class Customer:
  id = 0 
  def __init__(self, name, phone, addr, dist):
    self.name = name
    self.phone = phone
    self.addr = addr
    self.dist = dist

#creates a new customer class from input information and then calls the function to insert it into the database
def create_new(db, fields):
  cust = Customer(fields[1].get(), fields[2].get(), fields[3].get(), fields[4].get())
  db.insert(cust)

#removes the customer from the database based on customer id #
def delete(db, fields):
  cust = Customer(fields[1].get(), fields[2].get(), fields[3].get(), fields[4].get())
  cust.id = fields[0].get()
  db.remove(cust)
  clear(fields)

#calls function to get customer information from db and then inserts that info into text fields
def look_up(db, fields):
  data = db.fetch("Customers", fields[0].get(), fields[2].get())
  clear(fields)
  for i in range(len(fields)):
    fields[i].insert(0, data[0][i])    

#erases all text from the fields  
def clear(fields):
  for field in fields:
    field.delete(0, tk.END)

#updates customer db information with info from text fields
def modify(db, fields):
  cust = Customer(fields[1].get(), fields[2].get(), fields[3].get(), fields[4].get())
  cust.id = fields[0].get()
  db.update(cust)

#opens customer screen and associated widgets
def cust_screen(db):
    
  window = comp.newWindow("Customer Options")
  title = comp.newLabel(window, "Customer", 16)
  title.grid(column = 2, row = 0,)

  #lists of labels and text fields so they can be placed using for loop and passed into functions togather
  labels = ["Customer #: ", "Name: ", "Phone: ", "Address: ", "Distance: "]
  fields = []
  
  #loop creates and places each label/text field in the window
  for text in labels:
    label = comp.newLabel(window, text, 12)
    label.grid(column = 1, row = labels.index(text)+1)
    entry = tk.Entry(window, width = 40)
    fields.append(entry)
    entry.grid(column = 2, row = labels.index(text)+1, sticky="w", columnspan=3)

  #lists again allow buttons to be created and placed using for loop
  btn_names = ["Search", "Add", "Delete", "Update", "Clear", "Cancel"]
  buttons = []

  for text in btn_names:
    button = comp.newButton(window, text)
    button.grid(column = 0, row = btn_names.index(text)+1, sticky = "n")
    buttons.append(button)
  
  #assigns functions to each button
  buttons[0].configure(command = lambda: look_up(db, fields))  
  buttons[1].configure(command = lambda: create_new(db, fields))
  buttons[2].configure(command = lambda: delete(db, fields))
  buttons[3].configure(command = lambda: modify(db, fields))
  buttons[4].configure(command = lambda: clear(fields))
  buttons[5].configure(command = window.destroy)