import pkgutil

DEBUG = False

# If termcolor is installed, these statements will be colored for easy visibility
# If termcolor isn't installed, they will be printed normally
if pkgutil.find_loader('termcolor') is not None:
    from termcolor import colored
else:
    def colored(string, color):
        return string

# Adds debug statements that are toggleable through the DEBUG variable
# If coloring is supported, these statements will be colored
# Includes a "Debug: " tag in front of all print statements to improve readability and identification
if DEBUG:
    def debug(text, color="magenta"): print(colored("Debug: "+str(text), color))
else:
    def debug(text, color=None): pass