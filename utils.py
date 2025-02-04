import os

def get_project_root() -> str:
    """Returns the absolute path to the project root directory"""
    return os.path.dirname(os.path.abspath(__file__))

def get_data_path() -> str:
    """Returns the absolute path to the data directory"""
    return os.path.join(get_project_root(), "data", "TPI ASCOR data - 13012025")
