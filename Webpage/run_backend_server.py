from backend import create_app ## pobieramu funkcje z backend - w folderze mamy __init__.py w którym jest właśnie funkcja create app
import subprocess # pozwala programowi Python na interakcję z systemem operacyjnym i uruchamianie innych procesów
import webbrowser
import time
import os # zarządzanie środowiskiem bierzącego procesu
from threading import Thread

app = create_app()

def choose_mode():
    print("\033[93mWybierz tryb servera\033[0m")
    print("\033[92m1. Development (Flask dev server)\033[0m")
    print("\033[91m2. Production (Gunicorn) - nie działa na systemie Windows. Tylko Linux (VPS, WSL2, Docker itd.)\033[0m")
    
    while True:
        choice = input("").strip()
        
        if choice == '1':
            return 'development'
        elif choice == '2':
            return 'production'
        else:
            print("Błędna wartość. Wpisz 1 lub 2.")

# funkcja sluży do uruchomienia serwera w trybie produkcyjnym
# cmd to lista z poleceniem uruchomieni gunicorn
# dunicorn - uruchamia serwer , --worker-class gevent- ustawia klasę workerów na gevent, co pozwala na obsługę asynchronicznych żądań,
#  --bind', '0.0.0.0:8000 - nasłuchiwanie na wszystkich interfejsach sieciowych port 8000 , start:app - wskazuje, że aplikacja znajduje się w pliku i jest obiektem app.

def run_production():
    print("Uruchamiam w trybie Production z Gunicorn...")
    print("* Serving Flask app 'website'")
    print("\033[93mPress CTRL+C to quit\033[0m")
    try:
        cmd = [
            'gunicorn', 
            '--worker-class', 'gevent',
            '--workers', '4',
            '--bind', '0.0.0.0:8000',
            'start:app'
        ]
        subprocess.run(cmd)
    except FileNotFoundError:
        print("Gunicorn nie jest zainstalowany!")
    
def run_development():
    try:
        app.run(debug=True, host='127.0.0.1', port=5000)
    except KeyboardInterrupt:
        print("Flask server is shutting down...")

# funkcja służąca do otwarcia przeglądarki internetowej z pewnym opuźneiniem
# Thread(target=delayed_open, daemon=True).start() uruchamia funkcję delayed_open() w osobnym wątku jako tzw. wątek demona. 
# Dzięki temu opóźnienie i otwarcie przeglądarki nie blokuje głównego programu
# udogodnienie developerskie
browser_opened = False

def open_browser(url, delay):
    def delayed_open():
        time.sleep(delay)
        webbrowser.open(url)
    Thread(target=delayed_open, daemon=True).start()

# if __name__ == '__main__': ten blok kodu wykona się tylko jeżeli zostanie uruchomiony bezpośrednio
# WERKZEUG_RUN_MAIN zmienna środowiskowa o wartości none przed uruchomieniem start.py. Po pierwszym uruchomieniu zmienia wartość na 1
# serwer deweloperski Flask automatycznie restartuje proces przy włączonym debugowaniu, aby móc przeładować kod po zmianach
# aby uniknąc ponownego załadowania się funkcji choose_mode() zastosowano warunek w o parciu o jej wartość
# Zmienne środowiskowe są automatycznie dziedziczone przez podprocesy, więc gdy Flask/Werkzeug restartuje aplikację, nowy proces odczytuje wartość SERVER_MODE bez dodatkowych zabiegów.

if __name__ == '__main__':
    if os.environ.get('WERKZEUG_RUN_MAIN') is None:
        mode = choose_mode()
        os.environ['SERVER_MODE'] = mode


        """if mode == 'development':
            open_browser("http://127.0.0.1:5000/api/utils/health", 2)"""
    else:
        mode = os.environ.get('SERVER_MODE')

    if mode == 'development':
        run_development()
    elif mode == 'production':
        run_production()

