from tkinter import END

def alphabeticallyInsert(listbox, valueToInsert):
    for x in range(listbox.size()):
        listboxValueAtX = listbox.get(x)
        if listboxValueAtX.lower() > valueToInsert.lower():
            listbox.insert(x, valueToInsert)
            return
    listbox.insert(END, valueToInsert)
