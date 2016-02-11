# coding=utf-8
#!/usr/bin/env python

import os
from gi.repository import Gtk

from Config import Config
from dbController import Worker

class ViewState:
    NEW = 1
    NEXT = 2
    PREV = 3

    def __init__(self, main_page, secondary_stack=None, secondary_page=None):
        self.main_page = main_page
        self.secondary_stack = secondary_stack
        self.secondary_page = secondary_page

class MainWindowHandler:
    def __init__(self, builder):
        self.menu_button = builder.get_object("menu_button")
        self.menu_content = builder.get_object("ez_pts")
        self.MainStack = builder.get_object("main_stack")
        self.HeaderStack = builder.get_object("header_stack")
        self.WorkersStack = builder.get_object("workers_stack")
        self.DBChanged = True

        self.B = builder

        self.go_back_button = builder.get_object("go_back")
        self.go_forward_button = builder.get_object("go_forward")

        self.ViewStack = [ViewState("main_page")]
        self.ViewStackPointer = 0

        self.w_ls = builder.get_object("workers_list_store")

        self.CreateFancyMenu()
        self.LoadCSS()

    def LoadCSS(self):
        from gi.repository.Gdk import Screen

        CSS_FILE_NAME = "{1}{0}main.css".format(os.path.sep, Config["STYLING_DIRECTORY"])
        style_provider = Gtk.CssProvider()

        with open(CSS_FILE_NAME, "rb") as css_file:
            css_data = css_file.read()

        style_provider.load_from_data(css_data)
        Gtk.StyleContext.add_provider_for_screen(
            Screen.get_default(), style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def SyncHeaderStack(self):
        current_page = self.MainStack.get_visible_child_name()
        self.HeaderStack.set_visible_child_name(current_page)

    #Optimize
    def ChangeView(self, change_source, main_page=None, secondary_stack=None, secondary_page=None):
        #Rebuild it, make it so, prev button, and next button could simply gg wp, lanaya
        #Hadnle history is needed
        if (change_source == ViewState.NEW):
            self.ViewStack = self.ViewStack[:self.ViewStackPointer + 1]
            self.ViewStack.append(ViewState(main_page, secondary_stack, secondary_page))
            self.ViewStackPointer = len(self.ViewStack) - 1
        elif (change_source == ViewState.PREV):
            self.ViewStackPointer -= 1
        else:
            self.ViewStackPointer += 1

        NewView = self.ViewStack[self.ViewStackPointer]

        #Optimize
        if (NewView.secondary_stack):
            new_secondary_stack = self.B.get_object(NewView.secondary_stack)
            new_secondary_stack.set_visible_child_name(NewView.secondary_page)
        self.MainStack.set_visible_child_name(NewView.main_page)
        self.SyncHeaderStack()

        #Optimize
        if (self.ViewStackPointer != 0):
            self.go_back_button.set_sensitive(True)
        else:
            self.go_back_button.set_sensitive(False)

        if (self.ViewStackPointer == (len(self.ViewStack) - 1)):
            self.go_forward_button.set_sensitive(False)
        else:
            self.go_forward_button.set_sensitive(True)

    def prev_view(self, btn):
        self.ChangeView(ViewState.PREV)

    def next_view(self, btn):
        self.ChangeView(ViewState.NEXT)


    def CreateFancyMenu(self):
        popover = Gtk.Popover.new(self.menu_button)
        popover.add(self.menu_content)
        self.menu_button.set_popover(popover)

    def CreateFancyTable(self):
        self.store = Gtk.ListStore(int, str, str, str, str, str)
        self.workers_table = Gtk.TreeView(model=self.store)

        column_names = ["Имя", "Фамилия", "Отчество", "Пост", "Филиалы"]
        for column_id, column_name in enumerate(column_names, start=1):
            renderer = Gtk.CellRendererText(xalign=0.5)
            column = Gtk.TreeViewColumn(column_name, renderer, text=column_id)
            column.set_sort_column_id(column_id)
            self.workers_table.append_column(column)

        self.workers_table.connect("row-activated", self.wt_worker_selected)
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(
            Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.add(self.workers_table)

        scrolled_window.show_all()
        self.B.get_object("workers_list_align").add(scrolled_window)

    def go_to_all(self, data):
        if (self.DBChanged):
            self.CreateFancyTable()

            for worker in Worker.select(Worker.name, Worker.surname, Worker.lastname, Worker.post, Worker.department, Worker.id):
                self.store.append([
                    worker.id,
                    worker.name,
                    worker.surname,
                    worker.lastname,
                    worker.post.type,
                    worker.department.name
                ])

        self.ChangeView(ViewState.NEW, "workers_page", "workers_stack", "ws_list_page")

    def wt_worker_selected(self, widget, row, col):
        i = self.store[row][1]
        print i


    def on_close(self, *args):
        Gtk.main_quit()
