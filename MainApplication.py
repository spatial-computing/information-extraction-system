__author__ = 'shilpagulati'
from Tkinter import *
import tkMessageBox
from PIL import ImageTk, Image
import json
import PdfToText
import backup


def get_similar_data(input_query, country_name):
    backup.main(input_query, country_name)


def ok():
    global country
    value = dropDown.get()
    country = value
    screen.destroy()


def get_input():

    input_string = e.get()

    if input_string != "":
        input_string = input_string.strip()
        root.destroy()
        get_similar_data(input_string, country)
    else:
        tkMessageBox.showwarning(title="Error", message="Enter keywords from the regulations, you interested in knowing more !")


def show_data(texts):
    global e
    global root
    root = Tk()
    root.title("Regulation Document")
    root.geometry("%dx%d+%d+%d" % (650, 450, 300, 150))
    text=Text(root,width=450)
    text.insert(INSERT,texts)
    text.pack()

    e = Entry(root)

    e.focus_set()
    e.pack()

    input_string = e.get()
    b = Button(root, text="Get More Information", width=20, command=get_input)
    b.pack()
    root.mainloop()

screen = Tk()

screen.geometry("%dx%d+%d+%d" % (600, 400, 300, 150))
screen.title('Welcome to the world of drones')

im = Image.open("Image3.jpg")
backgroundImage = ImageTk.PhotoImage(im)

background_label = Label(screen, image=backgroundImage,text="Search Regulations", fg="Black",font=('Helvetica',18))
background_label.photo = backgroundImage
background_label.place(x=0, y=0)


dropDown = StringVar(screen)
dropDown.set("Select")
choices = ["LA", "IRELAND"]
option = OptionMenu(screen, dropDown, *choices)
option.pack(side='top', padx=80, pady=60)

button = Button(screen, text="Submit", command=ok)

button.pack(side='top', padx=50, pady=0,)

screen.mainloop()


# get the document for the country and send it for conversion from pdf to text.

JsonObj = open("DroneDocumentDatabase.json").read()
data = json.loads(JsonObj)

if country in data:
    document = data[country]
    PdfToText.main(document)
    with open("RawCorpus2.txt") as Infile:
        text = Infile.read()
        show_data(text)

else:
    tkMessageBox.showwarning(title="Error",message="No Selection Made! Retry !")
    print "Wrong selection"
