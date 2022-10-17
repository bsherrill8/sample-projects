#this file contains UI components so they can easily be created the same way each time
import tkinter as tk

def newLabel(window, str, size):
  label = tk.Label(window, text = str, font = ("Arial", size), bg = "lightsteelblue")
  return label

def newButton(window, str):
  button = tk.Button(
    window,
    width = 12,
    text = str,    
  )
  return button
  
def newWindow(name):
  window = tk.Toplevel()
  window.title(name)
  window.configure(bg="lightsteelblue")
  width = 700
  height = 500
  window.geometry("%dx%d" % (width, height))

  for column in range(5):
    window.columnconfigure(column, weight = 1)
  for row in range(7):
    window.rowconfigure(row, weight = 1)
    
  return window