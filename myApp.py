import tkinter as tk
from tkinter import *
from tkinter.colorchooser import askcolor
import sqlite3


#creating the sqlite database
def createDataBase():
    conn = sqlite3.connect('test.db')
    
    conn.execute('''CREATE TABLE IF NOT EXISTS NOTES
            (ID INTEGER PRIMARY KEY     AUTOINCREMENT,
            TYPE             TEXT   NOT NULL,
            TITLE            TEXT   NOT NULL,
            NOTE_CONTENT     TEXT   NOT NULL,
            COLOR            TEXT);''') 
    
    conn.commit()
    conn.close()

#functions related to the notes
    
#creating a new note
def newNote():
    newModal = Toplevel(main)
    newModal.title("New Note")
    newModal.geometry("700x600")
    newModal.configure(background="#c0edc2")

    #note title label
    titleLabel = Label(newModal, background="#c0edc2", text="Title:", font=("Arial", 15), fg="#0d520f")
    titleLabel.pack(pady=5)

    #note title input
    titleOfTheNote = Text(newModal, height=1, width=500, background="white", cursor="heart", font=("Arial", 15), fg="#0d520f")
    titleOfTheNote.pack(padx=5)

    #content of the note label
    textLabel = Label(newModal, background="#c0edc2", text="Write your note here:", font=("Arial", 15), fg="#0d520f")
    textLabel.pack(pady=10)

    #content of the note input
    contentOfTheNote = Text(newModal, height=15, width=500, background="white", cursor="heart", font=("Arial", 15), fg="#0d520f")
    contentOfTheNote.pack(padx=5)

    #button for choosing the color of the note (showing when the viewAll() function is called)
    colorButton = Button(newModal, height=2, width=10, text="Color", command=lambda: getColor(colorButton, newModal), cursor="heart", relief="flat", fg="#0d520f", background="#3CB371")
    colorButton.pack(pady=10)

    #saving the note into the database
    doneButton = Button(newModal, height=2, width=10, text="Save", command=lambda: insertNote(titleOfTheNote, contentOfTheNote, newModal, colorButton.cget("bg")), cursor="heart", relief="flat", fg="#0d520f", background="#3CB371")
    doneButton.pack(pady=10)

#updating the note if it was modified
def changeNote(idNote, title, contentOfTheNote, newModal, color):
    conn = sqlite3.connect('test.db')

    #obtains the text from the given widgets
    #"1.0", "end-1c" -> from the beginning to the end
    titleContent = title.get("1.0", "end-1c")
    textContent = contentOfTheNote.get("1.0", "end-1c")
    
    conn.execute("UPDATE NOTES SET TITLE = ?, NOTE_CONTENT = ?, COLOR = ? WHERE ID = ?", (titleContent, textContent, color, idNote))
    conn.commit()

    conn.close()
    newModal.destroy()
    viewAll()

#modify the contents of a note
def changeContentnewModal(idNote, newModal):
    newModal.destroy()

    newModal = Toplevel(main)
    newModal.title("Edit Note")
    newModal.geometry("900x700")
    newModal.configure(background="#c0edc2")

    #when we open the new window to modify the old contents of a note, the previous information will appear in its corresponding place
    conn = sqlite3.connect('test.db')
    cursor = conn.execute("SELECT title, note_content, color FROM NOTES WHERE ID = ?", (idNote,))
    row = cursor.fetchone()
    conn.close()

    #title of the note label
    titleLabel = Label(newModal, background="#c0edc2", text="Title:", font=("Arial", 15), fg="#0d520f")
    titleLabel.pack(pady=5)

    #title of the note input
    titleOfTheNote = Text(newModal, height=1, width=500, background="white", cursor="heart", font=("Arial", 15), fg="#0d520f")
    titleOfTheNote.pack(padx=5)
    #the old title is the first in row 
    titleOfTheNote.insert(END, row[0])

    #note contents label
    textLabel = Label(newModal, background="#c0edc2", text="Write your note here:", font=("Arial", 15), fg="#0d520f")
    textLabel.pack(pady=10)

    #note contents input
    contentOfTheNote = Text(newModal, height=15, width=500, background="white", cursor="heart", font=("Arial", 15), fg="#0d520f")
    contentOfTheNote.pack(padx=5)
    #the old information is the second in row
    contentOfTheNote.insert(END, row[1])

    #the changing the color button
    colorButton = Button(newModal, height=2, width=10, text="Color", command=lambda: getColor(colorButton, newModal), cursor="heart", relief="flat", fg="#0d520f", background="#c0edc2")     
    colorButton.pack(pady=10)
    #the old color is in the third place in row
    colorButton.configure(bg=row[2])  

    #deleting the whole note
    deleteButton = Button(newModal, height=2, width=10, text="Delete", command=lambda: deleteNote(idNote, newModal), cursor="heart", relief="flat", fg="white", background="#b02828")                    
    deleteButton.pack(pady=10)

    #saving all the changes 
    doneButton = Button(newModal, height=2, width=10, text="Save", command=lambda: changeNote(idNote, titleOfTheNote, contentOfTheNote, newModal, colorButton.cget("bg")), cursor="heart", relief="flat", fg="#0d520f", background="#3CB371")
    doneButton.pack(pady=10)

#ask for a color and sets the 'Color' button to the chosen color
def getColor(colorButton, main):

    #the user cannot interact with other windows until the modal window is closed
    main.grab_set()

    #opens a color picker dialog, allowing the user to select a color 
    #it returns a tuple ([1] is the hexadecimal representation of the selected color)
    color = askcolor()[1]
    #change the configuration of the widget
    colorButton.configure(bg=color)
    #the user can interact with other windows
    main.grab_release()

#deletes the note
def deleteNote(idNote, newModal):
    conn = sqlite3.connect('test.db')
    conn.execute("DELETE FROM NOTES WHERE ID = ?", (idNote,))
    conn.commit()
    conn.close()
    newModal.destroy()

    viewAll()

#inserts the note into the database
def insertNote(title, text, newModal, color):
    conn = sqlite3.connect('test.db')

    #.strip() -> removes any leading or trailing whitespace from the text
    titleContent = title.get("1.0", "end-1c").strip()
    textContent = text.get("1.0", "end-1c").strip()

    #checks if the title or the content of the note is empty
    if not titleContent or not textContent:
        #if one of them is empty, the note is not going to be saved
        newModal.destroy() 
        conn.close()
        return

    conn.execute("INSERT INTO NOTES (TYPE, TITLE, NOTE_CONTENT, COLOR) VALUES (?, ?, ?, ?)", ("Note", titleContent, textContent, color))
    conn.commit()
    conn.close()
    newModal.destroy()
    #viewAll()

#functions related to the lists
    
#this function creates a new list
def newList():
    modal = Toplevel(main)
    modal.title("New Note")
    modal.geometry("900x800")
    modal.configure(background="#c0edc2")
   
    #title label
    titleLabel = Label(modal, background="#c0edc2", text="Title: ", font=("Arial", 15), fg="#0d520f")
    titleLabel.pack(pady = 3)

    #title input
    titleOfTheList = Entry(modal, width=75)
    titleOfTheList.pack(padx=3)

    #new item to be added label
    itemLabel = Label(modal, background="#c0edc2", text="Item: ", font=("Arial", 15), fg="#0d520f")
    itemLabel.pack(pady = 3)

    #new item to be added input
    itemOfTheList = Entry(modal, width=75)
    itemOfTheList.pack(pady=3)

    #button to add the item to the list
    addToList = Button(modal, height=1, width=10, text="Add item to list", command=lambda: addItem(contentOfTheList, itemOfTheList), cursor="heart", relief="flat", fg="#0d520f", background="#3CB371")
    addToList.pack(pady = 3)

    #the list contents label
    contentLabel = Label(modal, background="#c0edc2", text="Your list:", font=("Arial", 15), fg="#0d520f")
    contentLabel.pack(pady=3)

    #the list contents listbox
    contentOfTheList = Listbox(modal, height=15, width=500, background="white", cursor="heart", font=("Arial", 15), fg="#0d520f")
    contentOfTheList.pack(pady=3)

    #the button for changing the color of the list in the View All window 
    colorButton = Button(modal, height=2, width=15, text="Color", command=lambda: getColor(colorButton, modal), cursor="heart", relief="flat", fg="#0d520f", background="#3CB371")
    colorButton.pack(pady=3)

    #the button for deleting the selected item from the list
    deleteButton = tk.Button(modal, height=2, width=15, text="Delete selected item", command=lambda: deleteItem(contentOfTheList), cursor="heart", relief="flat", fg="white", background="#b02828")
    deleteButton.pack(pady=3)

    #the button for saving the list in the database
    saveButton = Button(modal, height=2, width=15, text="Save", command=lambda: insertList(titleOfTheList, contentOfTheList, modal, colorButton.cget("bg")), cursor="heart", relief="flat", fg="#0d520f", background="#3CB371")
    saveButton.pack(pady=3)

#adding an item to the list
def addItem(list, itemName):
    item = itemName.get()

    if item:
        itemName.delete(0, END)

        list.insert(END, item)

#deletes the selected item from the list
def deleteItem(list):
    selected = list.curselection()
    if selected:
        index = selected[0]
        list.delete(index)

#deletes a list
def deleteList(idNote, newModal):
    conn = sqlite3.connect('test.db')
    conn.execute("DELETE FROM NOTES WHERE ID = ?", (idNote,))
    conn.commit()
    conn.close()
    newModal.destroy()
    viewAll()

#updating the list in the database when it was modified
def changeList(idList, title, listContent, newModal, color):
    
    conn = sqlite3.connect('test.db')

    titleContent = title.get()
    allItems = listContent.get(0, END)

    textContent = "\n".join(allItems)

    if not titleContent or not textContent:
        newModal.destroy() 
        conn.close()
        return
    
    conn.execute("UPDATE NOTES SET TITLE = ?, NOTE_CONTENT = ?, COLOR = ? WHERE ID = ?", (titleContent, textContent, color, idList))
    conn.commit()
    conn.close()
    newModal.destroy()
    
    viewAll()

#modifies the contents of a list (opens a new modal for changes with the previous information still in its place)
def changeListNewModal(idList, newModal):
    newModal.destroy()

    newModal = Toplevel(main)
    newModal.title("Edit List")
    newModal.geometry("900x800")
    newModal.configure(background="#c0edc2")

    conn = sqlite3.connect('test.db')
    cursor = conn.execute("SELECT title, note_content, color FROM NOTES WHERE ID = ?", (idList,))
    row = cursor.fetchone()
    conn.close()

    #title of the list label
    titleLabel = Label(newModal, background="#c0edc2", text="Title: ", font=("Arial", 15), fg="#0d520f")
    titleLabel.pack(pady = 3)

    #title of the list input
    titleOfTheList = Entry(newModal, width=75)
    titleOfTheList.pack(padx=3)
    #the previous title of the list 
    titleOfTheList.insert(END, row[0])

    #label for the new item to be added
    itemLabel = Label(newModal, background="#c0edc2", text="Item: ", font=("Arial", 15), fg="#0d520f")
    itemLabel.pack(pady = 3)

    #input for the new item to be added
    itemOfTheList = Entry(newModal, width=75)
    itemOfTheList.pack(pady=3)

    #the button to add to the list
    addToList = Button(newModal, height=1, width=10, text="Add item to list", command=lambda: addItem(contentOfTheList, itemOfTheList), cursor="heart", relief="flat", fg="#0d520f", background="#3CB371")
    addToList.pack(pady = 3)

    #the label for the content of the list
    contentLabel = Label(newModal, background="#c0edc2", text="Your list:", font=("Arial", 15), fg="#0d520f")
    contentLabel.pack(pady=3)

    #the listbox with the contents of the list
    contentOfTheList = Listbox(newModal, height=15, width=500, background="white", cursor="heart", font=("Arial", 15), fg="#0d520f")
    contentOfTheList.pack(pady=3)

    #added the old information in the listbox with newline (as it was first added)
    for item in row[1].split("\n"):
        contentOfTheList.insert(END, item)

    #the button for changing the color
    colorButton = Button(newModal, height=2, width=15, text="Color", command=lambda: getColor(colorButton, newModal), cursor="heart", relief="flat", fg="#0d520f", background="#3CB371")
    colorButton.pack(pady=3)
    #the old color is added as bg for the button
    colorButton.configure(bg=row[2])  

    #the button to delete a selected item
    deleteButton = tk.Button(newModal, height=2, width=15, text="Delete selected item", command=lambda: deleteItem(contentOfTheList), cursor="heart", relief="flat", fg="white", background="#b02828")
    deleteButton.pack(pady=3)

    #the button to delete the whole list
    deleteListButton = tk.Button(newModal, height=2, width=15, text="Delete list", command=lambda: deleteList(idList, newModal), cursor="heart", relief="flat", fg="white", background="#b02828")
    deleteListButton.pack(pady=3)

    #the button to save the changes
    saveButton = Button(newModal, height=2, width=15, text="Save", command=lambda: changeList(idList, titleOfTheList, contentOfTheList, newModal, colorButton.cget("bg")), cursor="heart", relief="flat", fg="#0d520f", background="#3CB371")
    saveButton.pack(pady=3)

#deletes the list
def deleteList(idList, newModal):
    conn = sqlite3.connect('test.db')
    conn.execute("DELETE FROM NOTES WHERE ID = ?", (idList,))
    conn.commit()
    conn.close()
    newModal.destroy()

#inserts the list into the database
def insertList(title, listContent, newModal, color):
    
    conn = sqlite3.connect('test.db')

    titleContent = title.get()
    allItems = listContent.get(0, END)

    #joins all the items together into the textContent variable -> added in the database
    textContent = "\n".join(allItems)

    conn.execute("INSERT INTO NOTES (TYPE, TITLE, NOTE_CONTENT, COLOR) VALUES (?, ?, ?, ?)",
             ("List", titleContent, textContent, color))
    
    conn.commit()
    conn.close()
    newModal.destroy()
    
#tprints all the notes and the lists that still exist in the database (the new modal for when the View All button is selected from the main window)
def viewAll():
    #creating the modal
    newModal = Toplevel(main)
    newModal.title("View All Notes and Lists")
    newModal.geometry("750x500")
    newModal.configure(background="#c0edc2")
    
    #label for the title
    title = Label(newModal, background="#c0edc2", text="Here are all of your notes and lists", font=("Arial", 20), fg="#0d520f")
    title.pack(pady=10, padx=5)

    #the order is desc because the list of lists and notes will be printed to the newest (the last in the database) to the oldest (the first one in the database)
    conn = sqlite3.connect('test.db')
    cursor = conn.execute("SELECT type, ID, title, note_content, color FROM NOTES ORDER BY ID DESC")
    rows = cursor.fetchall()

    #iterating over the rows in the cursor
    #for every row, it will create a button that has the color of the list/note (it was chosen at the creation of said note/list bt selecting the Color button)
    #it is a button because, when pressed, it will direct to a new window in which the list/note can be modified/deleted
    for row in rows:
        #if the type of the entry is "Note", here are the specific things to the notes:
        # (the "Note: " at the beginning of the title and, when pressed, the button will direct to the modal in which the list can be modified or deleted)
        if row[0] == 'Note':
            Button(
                newModal, 
                background=row[4], 
                height=2, 
                width=600, 
                command=lambda r=row: changeContentnewModal(r[1], newModal), 
                cursor="heart", 
                relief="flat", 
                text=f"Note: {row[2]}", 
                font=("Arial", 15), 
                fg="#0d520f", 
                anchor="w"
            ).pack(pady=5, padx=5)
        #if the type of the entry is "List", here are the specific things to lists: 
        # (the "List: " at the beginning of the title and, when pressed, the button will direct to the modal in which the note can be modified or deleted)
        elif row[0] == 'List':
            Button(
                newModal, 
                background=row[4], 
                height=2, 
                width=600, 
                command=lambda r=row: changeListNewModal(r[1], newModal), 
                cursor="heart", 
                relief="flat", 
                text=f"List: {row[2]}", 
                font=("Arial", 15), 
                fg="#0d520f", 
                anchor="w"
            ).pack(pady=5, padx=5)

    conn.close()


#the beginning of the application
createDataBase()
#here is the main windows of the app
main = tk.Tk()

main.title("Memo")
main.geometry("750x500")
main.configure(background="#3CB371")

#title label
titleLabel = Label(main, background="#3CB371", text="Welcome to your notes!", font=("Arial", 30), fg="#0d520f")
titleLabel.pack(pady=50, padx=10) 

#the 3 buttons from the main window
button1 = Button(main, height=2, width=20, text="New Note", command = newNote, cursor="heart", relief="flat", fg="#0d520f", background="#c0edc2").pack(pady=20)
button2 = Button(main, height=2, width=20, text="New List", command = newList, cursor="heart", relief="flat", fg="#0d520f", background="#c0edc2").pack(pady=20)
button3 = Button(main, height=2, width=20, text="View all", command = viewAll, cursor="heart", relief="flat", fg="#0d520f", background="#c0edc2").pack(pady=20)
main.mainloop()







