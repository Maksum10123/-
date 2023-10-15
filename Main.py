import tkinter as tk
from tkinter import ttk
import random
import sqlite3
from PIL import Image, ImageTk
from tkinter import filedialog

# Сохранение мемов
def add_meme():
    category = category_var.get()
    file_path = filedialog.askopenfilename()
    if file_path:
        conn = sqlite3.connect('memes.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO memes (category, file_path) VALUES (?, ?)", (category, file_path))
        conn.commit()
        conn.close()

# Отображения случайного мема
def show_random_meme():
    category = category_var.get()
    conn = sqlite3.connect('memes.db')
    cursor = conn.cursor()
    cursor.execute("SELECT file_path FROM memes WHERE category = ? ORDER BY RANDOM() LIMIT 1", (category,))
    result = cursor.fetchone()
    conn.close()

    if result:
        file_path = result[0]
        image = Image.open(file_path)
        image = image.resize((300, 300), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        meme_label.config(image=photo)
        meme_label.photo = photo
    else:
        meme_label.config(text="Нет мемов в этой категории.")

# Главное окно
root = tk.Tk()
root.geometry("350x400")
root.iconbitmap(default="icon.ico")
root.title("Мемасы от Джека")

# Списки категорий
categories = ["Джек", "Роблокс", "Люди", "Остальное"]
category_label = ttk.Label(root, text="Выберите категорию:")
category_label.pack()
category_var = tk.StringVar()
category_combobox = ttk.Combobox(root, textvariable=category_var, values=categories)
category_combobox.pack()

# Кнопка для показа мемов
show_button = ttk.Button(root, text="Показать случайный мем", command=show_random_meme)
show_button.pack()

# Отображения мема
meme_label = ttk.Label(root)
meme_label.pack()

# Кнопка для добавления мемов
add_button = ttk.Button(root, text="Добавить мем", command=add_meme)
add_button.pack()

# SQLite
conn = sqlite3.connect('memes.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS memes (id INTEGER PRIMARY KEY, category TEXT, file_path TEXT)''')
conn.commit()
conn.close()

root.mainloop()
