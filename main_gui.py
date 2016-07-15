try:
    from tkinter import Tk
except ImportError:
    print("Could not import core libraries, exitting.")
    exit()

main_form = Tk()
main_form.title("Anonymizer")
main_form.geometry('500x500')
main_form.resizable(0, 0)
main_form.mainloop()