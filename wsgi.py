import os
import sys

# Add the project root and backend to the system path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.app import create_app

app = create_app()
