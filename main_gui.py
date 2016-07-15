try:
    from classes.forms import MainScreen
except ImportError:
    print("Could not import classes package, exitting.")
    exit()

try:
    import os
except ImportError:
    print("Could not import core library, exitting.")
    exit()

main_form = MainScreen()
main_form.title("Anonymizer")

main_form.mainloop()