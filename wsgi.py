import sys
import os
path = os.path.dirname(__file__)  # Получаем путь к текущему файлу
if path not in sys.path:
    sys.path.append(path)

from app import app as application
