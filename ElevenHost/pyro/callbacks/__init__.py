import os
import sys

current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)

for file in os.listdir(current_dir):
  if file.endswith(".py") and file != "__init__.py":
    module_name = file[:-3]
    module = __import__(module_name)
