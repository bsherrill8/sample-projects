#This file contains the class and functions for furniture objects as well as the furniture screen code
import UIcomponents as comp
import tkinter as tk

class Furniture:
  id = 0 
  def __init__(self, desc, price, stock):
    self.desc = desc
    self.price = price
    self.stock = stock

#creates a funiture object and saves it in the db
def create_new(db, fields):
  furn = Furniture(fields[1].get(), fields[2].get(), fields[3].get())
  db.insert(furn)

#removes a furniture object from the db based on id#
def delete(db, fields):
  furn = Furniture(fields[1].get(), fields[2].get(), fields[3].get())
  furn.id = fields[0].get()
  db.remove(furn)
  clear(fields)

#retrieves furniture information from db and places it in text fields
def look_up(db, fields):
  data = db.fetch("Furniture", fields[0].get(), fields[2].get())
  clear(fields)
  for i in range(len(fields)):
    fields[i].insert(0, data[0][i])

#erases all fields
def clear(fields):
  for field in fields:
    field.delete(0, tk.END)

#updates db information with info from text fields
def modify(db, fields):
  furn = Furniture(fields[1].get(), fields[2].get(), fields[3].get())
  furn.id = fields[0].get()
  db.update(furn)

#creates furniture screen and associated widgets
def furn_screen(db):
  window = comp.newWindow("Furniture Options")

  title = comp.newLabel(window, "Furniture", 16)
  title.grid(column = 2, row = 0,)

  #lists allow labels and text fields to be placed with loop and passed to functions together
  labels = ["Item #: ", "Description: ", "Price: ", "In Stock: "]
  fields = []
  
  for str in labels:
    label = comp.newLabel(window, str, 12)
    label.grid(column = 1, row = labels.index(str)+1)
    entry = tk.Entry(window, width = 40)
    fields.append(entry)
    entry.grid(column = 2, row = labels.index(str)+1, sticky="w", columnspan=3)

  #same for the list of buttons
  btn_names = ["Search", "Add", "Delete", "Update", "Clear", "Cancel"]
  buttons = []

  for str in btn_names:
    button = comp.newButton(window, str)
    button.grid(column = 0, row = btn_names.index(str)+1, sticky = "n")
    buttons.append(button)

  #assigns functions to each button
  buttons[0].configure(command = lambda: look_up(db, fields))  
  buttons[1].configure(command = lambda: create_new(db, fields))
  buttons[2].configure(command = lambda: delete(db, fields))
  buttons[3].configure(command = lambda: modify(db, fields))
  buttons[4].configure(command = lambda: clear(fields))
  buttons[5].configure(command = window.destroy)