# ウィンドウを作る

早速作っていきましょう。

まずはウィンドウを作成します。  
[さっきのコード](BeforeDIY.md)を覚えているでしょうか？

```python
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

win = Gtk.Window()
win.set_default_size(640, 480)
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
```

上の3行はGTKを利用するためのライブラリを読み込む部分なので、実際にウィンドウを生成する部分には関係ありません。  
重要なのは`win = Gtk.Window()`で、ここがウィンドウ生成部分です。  
※Windowの頭文字が大文字であることに注意しましょう。

これはウィンドウの実体をwinという変数に格納しています。
`win.set_default_size(640, 480)`ではウィンドウの初期サイズ(幅・高さ)を指定しています。  
次の行の`win.connect("delete-event", Gtk.main_quit)`は、ウィンドウの×ボタンを押した時に`Gtk.main_quit`を実行するという意味です。  
`Gtk.main_quit`は関数で、`Gtk.main`に対して正常な終了を要求するものです。

ここで覚えて欲しいのは、`*.connect`というメソッドの使い方です。  
これはGTKウィジェットに対してイベントハンドラを設定するもので、頻繁に登場します。  
先ほど見たようにこのメソッドは以下の2つの引数をとります。

```python
*.connect("シグナル名", コールバック関数)
```

今回のシグナルは全てのGTKウィジェットに共通して存在し、トップレベルのウィンドウが閉じられる直前に通知されるものです。  

ウィジェット共通のシグナルについてはAPIリファレンスの以下のページに全て載っています。  
http://lazka.github.io/pgi-docs/#Gtk-3.0/classes/Widget.html#signals