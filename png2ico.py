import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image
import os
import json

# 設定ファイルの保存先（PermissionError対策）
DATA_DIR = os.path.join(os.path.expanduser("~"), ".icoconverter")
os.makedirs(DATA_DIR, exist_ok=True)
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")

def save_last_dir(path):
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump({"last_dir": os.path.dirname(path)}, f, indent=4)
    except:
        pass

def load_last_dir():
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f).get("last_dir", "")
    except:
        return ""

def convert_to_ico():
    input_path = file_path_var.get()
    if not input_path or not os.path.exists(input_path):
        messagebox.showerror("エラー", "有効な画像ファイルを選択してください。")
        return

    # 保存先を選択
    initial_dir = load_last_dir() or os.path.dirname(input_path)
    default_name = os.path.splitext(os.path.basename(input_path))[0] + ".ico"
    
    output_path = filedialog.asksaveasfilename(
        title="icoファイルの保存先を選択",
        initialdir=initial_dir,
        initialfile=default_name,
        filetypes=[("Icon files", "*.ico")]
    )

    if not output_path:
        return  # キャンセルされた場合

    try:
        status_label.config(text="変換中...")
        root.update()

        # 画像を開いてICO形式で保存
        img = Image.open(input_path)
        
        # アイコンに含めるサイズ候補（Windows標準の複数サイズ対応）
        # 元画像が小さすぎる場合はそのサイズに合わせる
        icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        
        # ICOとして保存（Pillowが自動でマルチサイズICOを作ってくれます）
        img.save(output_path, format="ICO", sizes=icon_sizes)
        
        save_last_dir(output_path)
        status_label.config(text="状態: 変換成功！")
        messagebox.showinfo("完了", f"変換が完了しました！\n{output_path}")
        
    except Exception as e:
        status_label.config(text="状態: エラー発生")
        messagebox.showerror("エラー", f"変換に失敗しました:\n{str(e)}")

def select_file():
    initial_dir = load_last_dir()
    file_path = filedialog.askopenfilename(
        title="画像ファイルを選択",
        initialdir=initial_dir,
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.webp")]
    )
    if file_path:
        file_path_var.set(file_path)
        status_label.config(text="状態: ファイルが選択されました")

# --- UIの構築 ---
root = tk.Tk()
root.title("PNG ➔ ICO 変換ツール")
root.geometry("450x200")
root.resizable(False, False)

file_path_var = tk.StringVar()

# ファイル選択エリア
frame = ttk.LabelFrame(root, text=" 変換する画像ファイル ")
frame.pack(fill="x", padx=15, pady=15)

entry = ttk.Entry(root, textvariable=file_path_var) # 参照用に分離
entry.pack(in_=frame, side="left", fill="x", expand=True, padx=5, pady=5)

ttk.Button(frame, text="参照...", command=select_file).pack(side="right", padx=5, pady=5)

# 変換ボタン
convert_btn = ttk.Button(root, text="ICO に変換する", command=convert_to_ico)
convert_btn.pack(fill="x", padx=20, pady=10)

# ステータス表示
status_label = ttk.Label(root, text="状態: 待機中")
status_label.pack(pady=5)

root.mainloop()