import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, '../static'))
print(STATIC_ROOT)
