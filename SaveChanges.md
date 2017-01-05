# 変更を保存しますか？

ここでは誤って編集中のファイルを破棄してしまわぬよう、確認ダイアログを表示するようにします。

ファイルに変更があるかどうかは`get_modified`メソッドで確認出来ます。  
まずは以下のメソッドを`EditorWindow`クラスに追加してください。

```python
def check_modified(self):
    if self.buffer.get_modified():
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION,
                            (Gtk.STOCK_CANCEL,
                             Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_NO,
                             Gtk.ResponseType.NO,
                             Gtk.STOCK_YES,
                             Gtk.ResponseType.YES))
        dialog.set_markup(self.filename+"への変更を保存しますか？")

        response = dialog.run()
        result = False
        if response == Gtk.ResponseType.NO:
            result = True
        elif response == Gtk.ResponseType.YES:
            result = self.save()

        dialog.destroy()
        return result
    else:
        return True
```

そして`on_open`メソッドと`on_quit`メソッドを以下のように変更します。

```python
def on_open(self, action, param):
    if self.check_modified() == False:
        return
    (略)

def on_quit(self, action, param):
    if self.check_modified():
        self.close()
```

以上で変更の保存を確認されるようになりました。  
フールプルーフの基本ですね。ほぼ前頁の応用なので簡単だったと思います。