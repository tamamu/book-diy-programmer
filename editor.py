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
          <attribute name="action">win.open_file</attribute>
          <attribute name="label" translatable="yes">開く</attribute>
        </item>
        <item>
          <attribute name="action">win.save_with_name</attribute>
          <attribute name="label" translatable="yes">名前を付けて保存</attribute>
        </item>
        <item>
          <attribute name="action">win.quit</attribute>
          <attribute name="label" translatable="yes">終了</attribute>
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
        self.window = None
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
        if not self.window:
            self.window = EditorWindow(application=self,
                                       title="DIY Editor")

        self.window.present()




class EditorWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_default_size(640, 480)

        self.buffer = GtkSource.Buffer()
        self.editor = GtkSource.View.new_with_buffer(self.buffer)

        lang_manager = GtkSource.LanguageManager()
        self.buffer.set_language(lang_manager.get_language('python'))
        self.add(self.editor)
        self.editor.show()

        action = Gio.SimpleAction.new_stateful("open_file", None,
                                               GLib.Variant.new_boolean(False))
        action.connect("activate", self.on_open_file)
        self.add_action(action)

        action = Gio.SimpleAction.new("save_with_name", None)
        action.connect("activate", self.on_save_with_name)
        self.add_action(action)

    def on_open_file(self, action, param):
        dialog = Gtk.FileChooserDialog("ファイルを選択", self,
                                       Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL,
                                        Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN,
                                        Gtk.ResponseType.OK))

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            f = GtkSource.File.new()
            f.set_location(dialog.get_file())
            loader = GtkSource.FileLoader().new(self.buffer, f)
            loader.load_async(GLib.PRIORITY_DEFAULT,
                              None,
                              None, None, None, None)

        dialog.destroy()

    def on_save_with_name(self, action, param):
        dialog = Gtk.FileChooserDialog("名前を付けて保存", self,
                                       Gtk.FileChooserAction.SAVE,
                                       (Gtk.STOCK_CANCEL,
                                        Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_SAVE,
                                        Gtk.ResponseType.OK))

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            f = GtkSource.File.new()
            f.set_location(dialog.get_file())
            saver = GtkSource.FileSaver().new(self.buffer, f)
            saver.save_async(GLib.PRIORITY_DEFAULT,
                             None, None, None, None, None)

        dialog.destroy()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
