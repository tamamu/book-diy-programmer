import os
import sys

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '3.0')
from gi.repository import Gtk, GtkSource, GLib, Gio

MENU_XML = """
<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <menu id="menubar">
    <submenu>
      <attribute name="label" translatable="yes">ファイル</attribute>
      <section>
        <item>
          <attribute name="action">win.open</attribute>
          <attribute name="label" translatable="yes">開く</attribute>
          <attribute name="icon">document-open</attribute>
        </item>
        <item>
          <attribute name="action">win.save</attribute>
          <attribute name="label" translatable="yes">上書き保存</attribute>
          <attribute name="icon">document-save</attribute>
        </item>
        <item>
          <attribute name="action">win.save_as</attribute>
          <attribute name="label" translatable="yes">名前を付けて保存</attribute>
          <attribute name="icon">document-save-as</attribute>
        </item>
        <item>
          <attribute name="action">win.quit</attribute>
          <attribute name="label" translatable="yes">終了</attribute>
          <attribute name="icon">application-exit</attribute>
        </item>
      </section>
    </submenu>
  </menu>
</interface>
"""


class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.diy.editor",
#                        flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
                         flags=Gio.ApplicationFlags.FLAGS_NONE,
                         **kwargs)
        self.win = None
#        self.activate()

#        self.add_main_option("open", ord("o"), GLib.OptionFlags.NONE,
#                             GLib.OptionArg.NONE, "Open file", None)

#    def do_command_line(self, command_line):
#        options = command_line.get_options_dict()
#
#        if options.contains("open"):
#            print("Open file!")
#
#        self.activate()
#        return 0

    def do_startup(self):
        Gtk.Application.do_startup(self)

        builder = Gtk.Builder.new_from_string(MENU_XML, -1)
        self.set_menubar(builder.get_object("menubar"))

    def do_activate(self):
        if not self.win:
            self.win = EditorWindow(application=self,
                                    title="DIY Editor")
            action = Gio.SimpleAction.new("open", None)
            action.connect("activate", self.win.on_open)
            self.win.add_action(action)
            self.add_accelerator('<Primary>O', 'win.open', None)

            action = Gio.SimpleAction.new("save", None)
            action.connect("activate", self.win.on_save)
            self.win.add_action(action)
            self.add_accelerator('<Primary>S', 'win.save', None)

            action = Gio.SimpleAction.new("save_as", None)
            action.connect("activate", self.win.on_save_as)
            self.win.add_action(action)
            self.add_accelerator('<Primary><Shift>S', 'win.save_as', None)

            action = Gio.SimpleAction.new("quit", None)
            action.connect("activate", self.win.on_quit)
            self.win.add_action(action)
            self.add_accelerator('<Primary>Q', 'win.quit', None)

        self.win.present()


class EditorWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_default_size(640, 480)

        self.__sw = Gtk.ScrolledWindow()
        self.__sw.set_hexpand(True)
        self.__sw.set_vexpand(True)

        self.buffer = GtkSource.Buffer()
        self.editor = GtkSource.View.new_with_buffer(self.buffer)
        self.path = ""

        lang_manager = GtkSource.LanguageManager()
        self.buffer.set_language(lang_manager.get_language('python'))
        self.__sw.add(self.editor)
        self.add(self.__sw)
        self.show_all()

    def on_open(self, action, param):
        dialog = Gtk.FileChooserDialog("ファイルを選択", self,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL,
                                        Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN,
                                        Gtk.ResponseType.OK))

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.path = dialog.get_filename()
            if not os.path.isabs(self.path):
                self.path = os.path.abspath(self.path)
            dialog.destroy()

            ENC = None
            for enc in ("iso-2022-jp", "euc-jp", "sjis", "utf-8"):
                with open(self.path, encoding=enc) as f:
                    try:
                        f.read()
                    except UnicodeDecodeError:
                        continue
                ENC = enc

            if ENC:
                with open(self.path, "Ur", encoding=ENC) as f:
                    source = f.read()
                self.buffer.begin_not_undoable_action()
                self.buffer.set_text(source)
                self.buffer.end_not_undoable_action()
                self.buffer.set_modified(False)
                self.buffer.place_cursor(self.buffer.get_start_iter())
            else:
                dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
                                           Gtk.ButtonsType.OK, "File Open Error")
                dialog.format_secondary_text(
                    "Cannot open: %r" % self.path)
                dialog.run()
                dialog.destroy()
        else:
            dialog.destroy()

    def save_as(self):
        dialog = Gtk.FileChooserDialog("名前を付けて保存", self,
                                       Gtk.FileChooserAction.SAVE,
                                       (Gtk.STOCK_CANCEL,
                                        Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_SAVE,
                                        Gtk.ResponseType.OK))

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.path = dialog.get_filename()
            source = self.buffer.get_text(self.buffer.get_start_iter(),
                                          self.buffer.get_end_iter())
            f = open(self.path, "w")
            f.write(source)
            f.close()

        dialog.destroy()

    def on_save(self, action, param):
        if self.path != "":
            source = self.buffer.get_text(self.buffer.get_start_iter(),
                                          self.buffer.get_end_iter(),
                                          True)
            f = open(self.path, "w")
            f.write(source)
            f.close()
        else:
            self.save_as()

    def on_save_as(self, action, param):
        self.save_as()

    def on_quit(self, action, param):
        self.close()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
