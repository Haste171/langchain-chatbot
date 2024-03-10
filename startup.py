import subprocess
import threading

print('Make sure to set .env variables.')
input('Also make sure you are in the Poetry shell before running this... (enter to start)')

def run_app():
    subprocess.run(['python3', 'app.py'])

def run_streamlit():
    subprocess.run(['streamlit', 'run', 'ui/main.py'])

def run():
    # Run each process in a separate thread
    t1 = threading.Thread(target=run_app)
    t2 = threading.Thread(target=run_streamlit)
    t1.start()
    t2.start()

run()
