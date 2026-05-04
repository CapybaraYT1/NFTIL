import subprocess

# запускаем сайт
subprocess.Popen(["python", "server.py"])

# запускаем бота
subprocess.Popen(["python", "bot.py"])

# держим контейнер живым
while True:
    pass
