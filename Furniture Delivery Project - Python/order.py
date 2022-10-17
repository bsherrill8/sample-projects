#this file contains class and functions for the Orders as well as code for the Order screen
import UIcomponents as comp
import tkinter as tk
import furniture, customer

class Order:
  id = 0
  furn = furniture.Furniture("", "", "")
  furn_set = {}
  subtotal = 0

  def __init__(self, customer, store):
    self.customer = customer
    self.del_fee = float(customer.dist) * store.del_ppm

#function looks up a customer and adds it to the order in progress
def cust_search(db, id, labels, order, store):
  data = db.fetch("Customers", id, "")
  order.customer = customer.Customer(data[0][1], data[0][2], data[0][3], data[0][4])
  order.customer.id = data[0][0]
  order.del_fee = order.customer.dist * store.del_ppm

#labels display active customer information
  labels[0].config(text=order.customer.name)
  labels[1].config(text=order.customer.phone)
  labels[2].config(text=order.customer.addr)

#looks up furniture information and makes it the active furniture item for the order
def furn_search(db, id, labels, order):
  #checks to see if this furniture is already part of the order and makes it active if so
  newitem = True
  for item in order.furn_set:
    if id == item.id:
      newitem = False
      order.furn = item
  
  #if it isn't then it creates a new furniture object using db info
  if newitem:
    data = db.fetch("Furniture", id, "")
    order.furn = furniture.Furniture(data[0][1], data[0][2], data[0][3])
    order.furn.id = data[0][0]
  
#labels display active furniture info
  labels[3].config(text=order.furn.desc)
  labels[4].config(text=order.furn.price)
  if str(order.furn.stock) == "0":
    labels[5].config(text="Out of Stock")
  else:
    labels[5].config(text="In Stock: " + str(order.furn.stock))

#searches for and loads saved order information from db
def ord_search(db, id, fields, labels, txtbox, order, store):
  clear(labels, fields, txtbox, order)
  data = db.fetch("Orders", id, "") #loads order info from db
  cust_search(db, data[0][2], labels, order, store) #loads customer info from order
  for row in data:
    furn_search(db, row[1], labels, order) #loads each item from the order and adds it
    add_item(order, txtbox)

#adds active furniture information to pending order
def add_item(order, txtbox):
  #first checks to see if that furniture is already part of the order
  if order.furn in order.furn_set:
    order.furn_set[order.furn] += 1 #increases the quantity if so
  else:
     order.furn_set[order.furn] = 1 #if not, adds it to the dict and sets qty to 1

  #adds furn price to order total and displays order
  order.subtotal +=order.furn.price
  display(order, txtbox)

#similar to above function, but removes active furn item from order
def rem_item(order,txtbox):
  if order.furn in order.furn_set:
    order.subtotal -= order.furn.price

    if order.furn_set[order.furn] == 1:
      del order.furn_set[order.furn]
    else:
      order.furn_set[order.furn] -= 1
  
  display(order, txtbox)

#displays current order in text box along with total price
def display(order, txtbox):
  txtbox.delete("1.0", tk.END)

  for item in order.furn_set:
    txtbox.insert(tk.END, item.desc + " x " + str(order.furn_set[item]) +"\t\t" +str(item.price * order.furn_set[item]) + "\n")

  txtbox.insert(tk.END, "------------------------------")
  txtbox.insert(tk.END, "Subtotal: \t\t%.2f\n" % order.subtotal)
  txtbox.insert(tk.END, "Delivery: \t\t%.2f\n " % order.del_fee)
  txtbox.insert(tk.END, "Total:\t\t%.2f\n" % (order.subtotal + order.del_fee))

#submits order information to db and adds total price to daily income
def submit(db, order, store):
  order.id = db.next_id()
  db.insert(order)
  store.daily_inc += (order.subtotal + order.del_fee)
  
#clears out all text fields and resets pending order to empty
def clear(labels, fields, txtbox, order):
  for label in labels:
    label.config(text="")
  for field in fields:
    field.delete(0, tk.END)
  txtbox.delete("1.0", tk.END)
  order.id = 0
  order.furn = furniture.Furniture("", "", "")
  order.furn_set = {}
  order.subtotal = 0

#creates order screen and associated widgets
def ord_screen(db, store):
  window = comp.newWindow("Order Options")

  #starts an empty order
  ord_in_prog = Order(customer.Customer("","","", 0), store)

  title = comp.newLabel(window, "Orders", 16)
  title.grid(column=2, row=0,)
  labels = []
  fields = []   
  
  #customer search labels, text fields and button
  lbl_cust = comp.newLabel(window, "Customer #: ", 10)
  lbl_cust.grid(column=0, row=1, sticky="E", padx=10)
  ent_cust = tk.Entry(window, width=10)
  ent_cust.grid(column=1, row=1, sticky="W", padx=10)
  fields.append(ent_cust)
 
  lbl_name = comp.newLabel(window, "", 8)
  lbl_name.grid(column=2, row=1, sticky="N")
  labels.append(lbl_name)
  lbl_phone = comp.newLabel(window, "", 8)
  lbl_phone.grid(column=2, row=1)
  labels.append(lbl_phone)
  lbl_addr = comp.newLabel(window, "", 8)
  lbl_addr.grid(column=2, row=1, sticky="S")
  labels.append(lbl_addr)
  
  btn_cust = comp.newButton(window, "Customer Search")
  btn_cust.grid(column=0, row=1, columnspan=2, sticky="S")
  btn_cust.configure(command=lambda: cust_search(db, int(ent_cust.get()), labels, ord_in_prog, store))    

  #furniture search labels, text fields, and button
  lbl_furn = comp.newLabel(window, "Item #: ", 10)
  lbl_furn.grid(column=0, row=2, sticky="E", padx=10)
  ent_furn = tk.Entry(window, width=10)
  ent_furn.grid(column=1, row=2, sticky="W", padx=10)
  fields.append(ent_furn)

  lbl_desc = comp.newLabel(window, "", 8)
  lbl_desc.grid(column=2, row=2, sticky="W")
  labels.append(lbl_desc)
  lbl_price = comp.newLabel(window, "", 8)
  lbl_price.grid(column=2, row=2, sticky="E")
  labels.append(lbl_price)
  lbl_stock = comp.newLabel(window, "", 8)
  lbl_stock.grid(column=2, row=2, sticky="S")
  labels.append(lbl_stock)

  btn_furn = comp.newButton(window, "Item Search")
  btn_furn.grid(column=0, row=2, columnspan=2, sticky="S")
  btn_furn.configure(command=lambda: furn_search(db, int(ent_furn.get()), labels, ord_in_prog))

  #order search label, field, and button
  lbl_ord = comp.newLabel(window, "Order #: ", 10)
  lbl_ord.grid(column=3, row=1, sticky="E", padx=10)
  ent_ord = tk.Entry(window, width=10)
  ent_ord.grid(column=4, row=1, sticky="W", padx=10)
  fields.append(ent_ord)
  btn_ord = comp.newButton(window, "Order Search")
  btn_ord.config(command=lambda: ord_search(db, int(ent_ord.get()), fields, labels, ord_text, ord_in_prog, store))
  btn_ord.grid(column=3, row=1, columnspan=2, sticky="S")

  #text box for displaying order
  ord_text = tk.Text(window, width = 1, height = 1)
  ord_text.grid(column=3, row=2, sticky="nsew", columnspan=2, rowspan=4, padx=10, pady=5)

  #button for adding active furniture item to order
  btn_add = comp.newButton(window, "Add Item ->")
  btn_add.config(command=lambda: add_item(ord_in_prog, ord_text))
  btn_add.grid(column=2, row=3)

  #button for removing active furniture item from order
  btn_rem = comp.newButton(window, "<- Remove Item")
  btn_rem.config(command=lambda: rem_item(ord_in_prog, ord_text))
  btn_rem.grid(column=2, row=4)

  #button to submit current order
  btn_submit = comp.newButton(window, "Submit Order")
  btn_submit.grid(column=3, row=6, columnspan=2)
  btn_submit.config(command=lambda: submit(db, ord_in_prog, store))

  #button to cancel out and close window
  btn_cancel = comp.newButton(window, "Cancel")
  btn_cancel.grid(column=0, row=6, columnspan=2)
  btn_cancel.configure(command=window.destroy)

  #button to clear out fields and reset
  btn_clear = comp.newButton(window, "Clear")
  btn_clear.config(command=lambda: clear(labels, fields, ord_text, ord_in_prog))
  btn_clear.grid(column=2, row=6)
  