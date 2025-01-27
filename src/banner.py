from rich.console import Console
from rich.text import Text
from rich import box
from rich.panel import Panel
import time
import random
import os
import asyncio

console = Console()

def clear_screen():
    """Clear the terminal screen based on OS"""
    os.system('cls' if os.name == 'nt' else 'clear')

BANNER = """
⠀⠀⠀⠀⠀⠀⠀⢸⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢸⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⢠⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢸⣿⠀⠀⠀⠀⠀⠀⠀⢀⡾⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⢠⡇⢀⣾⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡄⢸⡇⣼⢃⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣷⣸⠁⣿⣸⣿⡿⠀⣤⣤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠐⣎⣿⣿⣰⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿⡦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⢃⣿⣿⣿⣿⣿⢋⣶⣶⣶⣦⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣵⣶⣤⣤⡤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⡇⣿⣿⣿⠿⣛⣩⣭⣭⣭⣭⣉⣙⡛⣋⣩⣥⣴⣶⣶⣶⣶⣶⣶⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⠇⣾⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡿⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠛⠛⣛⡛⠛⠿⠿⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠟⠁⠚⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢋⣡⣴⣾⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡤⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣏⣼⣿⣿⣿⣿⣿⣯⣍⣛⠿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡧⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⡿⠏⢻⣿⣿⣿⣿⣿⣿⣿⠿⠛⢛⣛⠛⠻⠿⣷⣤⡉⠁⠀⠀⠀⠀⠀⠀⣦⠀⠀⣄⠀⠀⣇⠀⠀⠀⣸⡇⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⡇⢰⣿⣿⣿⣿⣶⣷⣦⣝⣷⡄⠀⠀⠀⠀⠀⠀⣿⡆⠀⣿⠀⠀⡝⢧⠀⠀⢼⡉⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⣍⣝⡛⠿⢿⣿⡄⣷⡀⠀⠀⠀⣿⡃⠀⣿⠀⠀⡇⠉⣇⠀⢹⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⣰⣿⣿⣿⣿⣿⡟⣿⣿⡇⢸⣿⣿⣿⣿⠿⢿⣿⣷⣦⣌⠁⢹⡛⣆⡀⠀⣿⠂⠀⣿⠄⠀⡧⠀⠘⡆⣿⠒⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⣿⣿⣿⡟⣸⣿⣿⡇⢸⣿⣿⣿⣿⣿⣷⣦⣌⡙⠛⠗⣸⡇⠹⣆⠀⣿⡂⠀⣿⠄⠀⡇⠀⠀⠼⣿⠆⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣼⢿⣿⣿⣿⣿⣿⢡⣿⣿⣿⠃⢸⣿⣿⣿⣿⣤⣬⣙⡛⠿⢷⡆⢨⡇⠀⠙⣷⣷⠃⠀⢿⠀⠀⣷⠀⠀⠐⣿⡆⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⠇⣘⣩⣿⣿⠀⢸⣿⣿⣿⣿⡛⡻⠿⣿⣶⣤⡀⢸⡇⠀⠀⠈⠻⠀⠀⠀⠀⠀⠙⠀⠀⠀⠁⠃⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣵⣾⣿⣿⣿⣿⠀⢸⣿⣿⣿⣿⣿⣿⣷⣦⣌⡙⠛⢨⡳⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⠿⠟⠛⠻⢿⣿⣿⣿⣿⠀⢾⣿⣿⣿⣿⣴⣮⣍⡛⠻⢿⣦⠘⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠿⠛⠉⣠⣴⣾⠟⣃⣤⠙⣿⣿⣿⡀⠻⠿⢿⣿⣿⣿⣿⣿⣿⣶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣶⡿⢛⣩⣴⣿⣿⣿⣧⠘⣿⣿⣿⣶⣦⣤⣄⣀⣈⠉⠙⠻⢿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠙⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⣠⣤⣴⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⡛⢁⣼⣿⣿⣿⡿⠟⣋⣵⣿⣿⡇⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢠⣾⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣶⣾⣿⣿⣾⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⣼⡟⣿⣿⣿⣿⣿⡿⠟⣠⣿⣿⣿⣿⣿⣿⣿⣟⢻⡉⣛⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠉⠀⠈⠁⠉⠙⠉⠀⠀⠉⠉⠉⢛⠛⠛⠿⠿⠿⢠⢇⣿⣿⣿⣿⣿⣿⡿⢋⣉⣉⠛⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣶⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⣡⣴⣿⣿⣿⣷⣶⣤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⢟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣭⣭⣿⣿⣿⣿⠿⢿⣿⣿⣿⣷⣶⣤⣄⡀⠀⠀⠀⠀⠀⠀⣴⣿⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⡿⣿⣟⣡⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠉⠙⠛⠿⣿⣿⣿⣿⣶⣦⣤⣖⣵⣟⣯⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣼⡟⣡⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣙⣋⣭⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠉⠛⠻⠿⣿⣿⣿⣷⣧⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣸⡟⠰⠿⠿⠿⠿⠿⣿⢿⣿⣿⣿⣿⢃⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡹⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣽⢟⣟⠿⣿⣿⣿⣶⣤⣀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢠⣿⢣⣿⣿⣿⣶⣶⣶⣶⣾⣿⣿⣿⡿⢸⣿⣿⣿⣿⣿⡸⠿⠿⠿⢿⣿⡇⢻⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡯⡿⠃⠀⠀⠉⠙⠻⢿⣿⣿⣷⣦⣀⠀
⠀⠀⠀⠀⠀⠀⣾⡏⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣼⣿⣿⣿⣿⣿⣷⣶⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠽⠃⠀⠀⠀⠀⠀⠀⠀⠈⠙⠻⢿⣿⠧
⠀⠀⠀⠀⠀⠀⣿⡇⠾⢿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⠁⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⢰⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢠⣿⠇⣶⣶⣶⣶⣶⣶⣦⣼⣿⣿⣿⡟⢠⣿⣿⣿⣿⣿⣿⣿⡇⠿⠿⠿⠿⠿⠿⠀⠀⠀⠀⠀⠀⠀⢀⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣿⣿⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢠⣤⣤⣤⣤⣤⣤⣥⣾⣿⣿⡇⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠿⠿⠿⠿⠟⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢼⣿⠿⣿⣿⣿⣿⣿⣿⣿⣿⠃⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

WELCOME = """

システムオンライン
    RONIN-X
                                  
                                暗闇の中の光明
                            Light in the Darkness
                                            
    守護者の道を歩む
Walking the Guardian's Path
                                            
"""

KANJI_CYCLE = ['刀', '命', '義', '武', '誠', '心', '道']
ARTISTIC_STATIC = '艶 流 光 雨 雪 風 月 星 火 水 地 空'

LORE_SNIPPETS = [
    "一期一会 | Each meeting, a once-in-a-lifetime encounter.",
    "明鏡止水 | A mind like a clear mirror, still water.",
    "不動心 | Immovable spirit, unwavering resolve.",
    "活人剣 | The sword that gives life, not takes it.",
    "起死回生 | From death, return to life. Renewal.",
    "折衷之道 | The middle way between extremes."
]

# Add more dramatic color palette
COLORS = ['bright_red', 'red', 'blue', 'cyan', 'magenta']

def generate_artistic_static(width):
    """Generate artistic static using kanji characters"""
    chars = ARTISTIC_STATIC.split()
    return ' '.join(random.choice(chars) for _ in range(width // 2))

async def animate_banner():
    """Display animated banner with enhanced visual effects"""
    clear_screen()
    
    # Initial dramatic pause with single kanji appearing
    center_kanji = "侍"  # Samurai
    console.print("\n" * 10)
    console.print(Text(center_kanji.center(80), style="bright_red"))
    await asyncio.sleep(1)
    clear_screen()
    
    # Scroll in banner with dramatic effect
    banner_lines = BANNER.split('\n')
    for i, line in enumerate(banner_lines):
        style = COLORS[i % len(COLORS)]
        if '███' in line:  # Special effect for solid blocks
            for j in range(len(line)):
                console.print(Text(line[:j], style=style))
                await asyncio.sleep(0.01)
                print('\033[F', end='')
            console.print(Text(line, style=style))
        else:
            console.print(Text(line, style=style))
        await asyncio.sleep(0.1)
    
    # Animate kanji with particle effects
    for _ in range(3):
        for i in range(len(KANJI_CYCLE)):
            particles = ''.join(random.choice('・･*') for _ in range(3))
            console.print(f"\033[{9+i}G{particles} {KANJI_CYCLE[i]} {particles}")
            await asyncio.sleep(0.2)
    
    # Fade in welcome message with matrix-like effect
    welcome_lines = WELCOME.split('\n')
    for line in welcome_lines:
        matrix_line = ''.join(random.choice('01') for _ in range(len(line)))
        console.print(Text(matrix_line, style='green'))
        await asyncio.sleep(0.1)
        print('\033[F', end='')
        console.print(Text(line, style='cyan'))
        await asyncio.sleep(0.05)

async def run_system_checks():
    """Enhanced system check animation"""
    checks = [
        ("システム起動  SYSTEM STARTUP", "bright_green"),
        ("武士道プロトコル  BUSHIDO PROTOCOLS", "bright_red"),
        ("精神同期中  SPIRIT SYNCHRONIZATION", "bright_blue"),
        ("刀剣較正  BLADE CALIBRATION", "bright_magenta"),
        ("影歩確認  SHADOW STEP VERIFICATION", "bright_cyan"),
        ("気配遮断  PRESENCE CONCEALMENT", "bright_red"),
        ("守護結界展開  BARRIER DEPLOYMENT", "bright_green")
    ]
    
    with console.status("[bold red]侍魂 • SAMURAI SPIRIT[/bold red]") as status:
        for check, color in checks:
            # Artistic loading animation
            for phase in '◜◠◝◞◡◟':
                status.update(f"[{color}]{phase} {check}[/{color}]")
                await asyncio.sleep(0.1)
            
            # Completion mark with kanji
            console.print(f"[bright_white]完[/bright_white] [{color}]{check}[/{color}]")
            
            # Random chance for artistic static
            if random.random() < 0.3:
                console.print(Text(generate_artistic_static(60), style="dim"))
            
            await asyncio.sleep(0.3)

async def display_startup_sequence():
    """Enhanced startup sequence with artistic elements"""
    await animate_banner()
    
    # Artistic transition effect
    width = 40
    for i in range(5):
        static = generate_artistic_static(width)
        density = (5 - i) / 5
        static = ' '.join(c if random.random() < density else '  ' for c in static)
        console.print(static, style="dim cyan")
        await asyncio.sleep(0.1)
    
    await run_system_checks()
    
    # Display lore with artistic frame
    lore = random.choice(LORE_SNIPPETS)
    console.print(Panel(
        lore,
        style="cyan",
        box=box.DOUBLE_EDGE,
        title="[bright_red]武士道[/bright_red]",
        subtitle="[bright_white]The Way of the Warrior[/bright_white]"
    ))
    
    # Interactive prompt with style
    prompt = "押して始まる | PRESS ENTER TO BEGIN | Send XMR donations to: 47v1zTEwjAmXCtGSPXz6VCAHsxFzpgNsX3w3bLse9dTVNKbgZ5xJump1hz7z2EEHbuTaqav95vNU47ZHLVPB5yAK3t8AqcK"
    for char in prompt:
        print(char, end='', flush=True)
        await asyncio.sleep(0.03)
    input()

def clear_terminal_preserve_banner():
    """Clear terminal while maintaining banner"""
    clear_screen()
    for line in (BANNER + WELCOME).split('\n'):
        console.print(f"[cyan]{line}[/cyan]")

if __name__ == "__main__":
    asyncio.run(display_startup_sequence())