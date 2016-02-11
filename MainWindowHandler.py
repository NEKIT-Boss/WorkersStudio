from gi.repository import Gtk
from MainWindow import *
class MainWindowHandler:
    def __init__(self, builder):
        self.menu_button = builder.get_object("menu_button")
        self.menu_content = builder.get_object("ez_pts")
        self.MainStack = builder.get_object("menu_stack")
        self.HeaderStack = builder.get_object("header_stack")
        self.w_ls = builder.get_object("workers_list_store")

        self.CreateFancyMenu()
        self.LoadCSS()

        dbController.init_preview_db()

    def LoadCSS(self):
        from gi.repository.Gdk import Screen

        CSS_FILE_NAME = "{}{}main.css".format(CONFIG["STYLING_DIRECTORY"], os.path.sep)
        style_provider = Gtk.CssProvider()

        with open(CSS_FILE_NAME, "rb") as css_file:
            css_data = css_file.read()

        style_provider.load_from_data(css_data)
        Gtk.StyleContext.add_provider_for_screen(
            Screen.get_default(), style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def CreateFancyMenu(self):
        popover = Gtk.Popover.new(self.menu_button)
        popover.add(self.menu_content)
        self.menu_button.set_popover(popover)

    def go_to_all(self, data):
        root_iter = None
        for i in range(50):
            dima = dbController.Worker.select().get()
            self.w_ls.append([dima.name, dima.surname, dima.lastname])

        self.MainStack.set_visible_child_name("workers_stack")
        self.HeaderStack.set_visible_child_name("workers_page") #This could be handled through signal

    def on_close(self, *args):
        Gtk.main_quit(args)
