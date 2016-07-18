try:
    from classes.forms import MainScreen
    from classes.processor import Anonymizer
except ImportError:
    print("Could not import classes package, exitting.")
    exit()

try:
    import os
except ImportError:
    print("Could not import core library, exitting.")
    exit()

anonymizer = Anonymizer("Nothing")   # Control object
main_form = MainScreen(anonymizer)    # View object

main_form.title("Anonymizer")

main_form.mainloop()