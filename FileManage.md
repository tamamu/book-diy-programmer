# ファイルを開いて、名前を付けて保存

ここから、メニューバーにアクションを設定していきます。  
ファイルを開いたり保存したり出来るようになるので、メモ帳卒業ですね。

まずは`EditorWindow`クラスに、項目が選択された時に実行されるメソッドを追加しましょう。

```python
def on_open(self, action, param):
    print("ファイルを開く")

def save_as(self):
    print("ファイルに名前を付けて保存")

def on_quit(self, action, param):
    self.close()
```

そして`Application`クラスの`do_activate`メソッドを以下のように書き換えます。

```python
def do_activate(self):
    if not self.win:
        self.win = EditorWindow(application=self,
                                title="DIY Editor")
        action = Gio.SimpleAction.new("open", None)
        action.connect("activate", self.win.on_open)
        self.win.add_action(action)
        self.add_accelerator("<Primary>O", "win.open", None)

        action = Gio.SimpleAction.new("save_as", None)
        action.connect("activate", self.win.on_save_as)
        self.win.add_action(action)
        self.add_accelerator("<Primary><Shift>S", "win.save_as", None)

        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.win.on_quit)
        self.win.add_action(action)
        self.add_accelerator("<Primary>Q", "win.quit", None)

    self.win.present()
```

ここで注目してほしいのが`action = Gio.SimpleAction.new("アクション名", None)`から`self.win.add_action(action)`までのブロックです。  
ここのアクション名は`MENU_XML`の`<attribute name="action">プレフィックス.アクション名</attribute>`と紐づいています。  
プレフィックスは操作対象を識別するために付けるもので、あまり気にしなくても大丈夫です。

そして`action.connect("activate", コールバック関数)`で実際にメニューアクションとメソッドをリンクさせています。  
`self.add_accelerator("ショートカットキー", "プレフィックス.アクション名", None)`ではショートカットキーを設定しています。

メニューバーからの操作とショートカットキーでの操作、両方共ちゃんと動作しましたか？

ここまで出来ていれば、やっとメニューバーの機能の実装に入れます。  
長かった！

それでは、まずは`名前を付けて保存`を実装しましょう。  
`EditorWindow`クラスの`__init__`メソッドに以下の行を追加してください。

```python
self.path = ""
self.filename = "Untitled"
```

これは編集中のファイルのパスとファイル名を格納しておくために使います。  
ここで定義した`self.filename`が仮のファイル名として表示に使われます。  
次に、以下のメソッドを`EditorWindow`クラスに追加してください。  
`on_save_as`メソッドとは別なので注意を。

```python
def save_as(self):
    dialog = Gtk.FileChooserDialog("名前を付けて保存", self,
                                    Gtk.FileChooserAction.SAVE,
                                    (Gtk.STOCK_CANCEL,
                                    Gtk.ResponseType.CANCEL,
                                    Gtk.STOCK_SAVE,
                                    Gtk.ResponseType.OK))

    response = dialog.run()
    result = False
    if response == Gtk.ResponseType.OK:
        self.path = dialog.get_filename()
        if not os.path.isabs(self.path):
            self.path = os.path.abspath(self.path)
        self.filename = os.path.basename(self.path)
        source = self.buffer.get_text(self.buffer.get_start_iter(),
                                      self.buffer.get_end_iter(),
                                      True)
        f = open(self.path, "w")
        f.write(source)
        f.close()
        self.buffer.set_modified(False)
        result = True

    dialog.destroy()
    return result
```

`dialog = Gtk.FileChooserDialog(...)`でファイル選択ダイアログを生成して`dialog`に格納しています。  
第一引数がダイアログ名、第二引数が親ウィジェット、第三引数がダイアログタイプ、第四引数が操作ボタンタイプのタプルです。  
少し分かりにくいのが第四引数でしょうか。簡単に表すと以下の形になります。

```python
# ファイル選択ダイアログには2つのボタンがある。タプルの中身は以下の通り。
(ボタン1のラベル,ボタン1を押した時の返り値,ボタン2のラベル,ボタン2を押した時の返り値)
```

つまり、`Gtk.STOCK_CANCEL`としたところを`"ほげ"`にしたらボタンのラベルが「ほげ」になるというわけですね。  
返り値も同様ですが、ここではGTKの流儀に倣うことにしましょう。

生成したダイアログは`dialog.run()`で実行することが出来ます。  
返り値もあるので単独では利用せず、変数に格納する形で利用しましょう。

返り値が`Gtk.ResponseType.OK`、すなわちファイルが選択された時はダイアログからファイル名が取得出来ます。  
`self.path = dialog.get_filename()`の部分がそれです。  
ここで`self.path`にファイル名を代入しておくことで、上書き保存をする時に困らないようにします。

保存する内容は`self.buffer`から取得します。  
これはテキストボックスの編集内容を扱うためのものでした。  
`self.buffer.get_text()`の引数は、取得するテキストの範囲を示す値で、ここではテキストの開始から終了まで全てを取得します。  
後の保存処理は定型なので解説するまでもありませんね。

最後に、`dialog.destroy()`でダイアログを閉じるのを忘れずに！

さて、これで`save_as`メソッドは完成しましたが、実行されるのは`on_save_as`メソッドです。  
`on_save_as`を以下のように書き換えましょう。

```python
def on_save_as(self, action, param):
    self.save_as()
```

なぜこんな回りくどいことをしているかというと、ズバリ`上書き保存`のためです。  
新しいファイルを上書き保存しようとすると、自動的に`名前を付けて保存`と同じ挙動になりますよね。  
ここまで書けたら`上書き保存`も簡単に実装出来てしまいます。

まずは`MENU_XML`に`上書き保存`の項目を追加してください。

```xml
<item>
    <attribute name="action">win.save</attribute>
    <attribute name="label" translatable="yes">上書き保存</attribute>
    <attribute name="icon">document-save</attribute>
</item>
```

そして`EditorWindow`クラスに上書き保存のメソッドを追加します。  
もし`self.path`が空だったら`名前を付けて保存`と同じ動作をさせます。

```python
def save(self):
    if self.path != "":
        source = self.buffer.get_text(self.buffer.get_start_iter(),
                                      self.buffer.get_end_iter(),
                                      True)
        f = open(self.path, "w")
        f.write(source)
        f.close()
        self.buffer.set_modified(False)
        return True
    else:
        return self.save_as()

def on_save(self, action, param):
    self.save()
```

最後に`Application`クラスの`do_activate`メソッドでアクションを追加するのを忘れずに。

```python
action = Gio.SimpleAction.new("save", None)
action.connect("activate", self.win.on_save)
self.win.add_action(action)
self.add_accelerator('<Primary>S', 'win.save', None)
```

これで保存は完璧ですね。  
あとはファイルを開けるようにするだけです！

`on_open`メソッドを以下のように書き換えてください。  
今回は色々な事情があって、少し長くなってしまいました。

```python
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
        self.filename = os.path.basename(self.path)
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
```

かなり長いですよね。  
今回問題となったのは、ファイルを開く時の文字コードです。  
世のソースコードの大半はUTF-8で書かれているのですが、たまに違う形式のコードが混ざっていることがあります。  
なのでここでは、ファイルが正常に読み込めるまで文字コードを変えてみるという方法を取っています。  
なかなかゴリ押しに感じますが、Pythonではこの方法が一番簡単なんだそうです。

ファイルの文字コードが分かったら、そのまま中身を読み込んでバッファに反映させています。  
`self.buffer.begin_not_undoable_action()`...`self.end_not_undoable_action()`で囲まれた部分はアンドゥで操作出来なくなります。  
さらに`self.buffer.set_modified(False)`でバッファを未変更の状態にし、次の行でカーソルを先頭に移動させています。

以上でファイルの入出力が出来るようになりました！  
変更済みのファイルの保存を促したりはしてくれませんが、コードを書くには十分な出来です。  
次の頁ではその部分を実装していきます。