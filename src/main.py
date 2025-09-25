#!/usr/bin/env python3
"""
Главный файл для развертывания Wazzup-Podio интеграции
"""

import sys
import os
from pathlib import Path

# Добавляем корневую директорию в путь
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

# Импортируем приложение
try:
    from app import app
except ImportError:
    # Альтернативный способ импорта
    import importlib.util
    spec = importlib.util.spec_from_file_location("app", root_dir / "app.py")
    app_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app_module)
    app = app_module.app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
