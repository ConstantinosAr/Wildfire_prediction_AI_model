import numpy
import math
import csv
import requests
from io import StringIO
from tkinter import *
from tkcalendar import *
from tktimepicker import AnalogPicker
import os
from interface_functions import *

#=========================================
#       INITIATION OF INTERFACE                                  
#=========================================


app = Tk()

timer = AnalogPicker(app)
timer.pack(pady = 10)

cal = Calendar(app, selectmode='day', year=2021, month=10, day=3)
cal.pack(pady=20)



calculate_btn = Button(app, text='Calculate', width=20, command=calculate)
calculate_btn.pack(pady = 10)

app.title('Warning System')
app.geometry('500x400')


app.mainloop()  
