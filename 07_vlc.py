import subprocess
import os
import PySimpleGUI as sg
import sys

url = sys.argv[1]

    
vlc_caminhos = [
    "C:/Program Files/VideoLAN/VLC/vlc.exe",
    "C:/Program Files (x86)/VideoLAN/VLC/vlc.exe",
    "C:/Arquivos de Programas/VideoLAN/VLC/vlc.exe",
    "C:/Arquivos de Programas (x86)/VideoLAN/VLC/vlc.exe"

]

for vlc_caminhos in vlc_caminhos:
    if os.path.isfile(vlc_caminhos):
        subprocess.call([vlc_caminhos, url])
        break
else:
    sg.popup_no_titlebar('\n    VLC não encontrado!\n\n Ele precisa estar instalado em um desses caminhos:\n\nC:/Program Files/VideoLAN/VLC/vlc.exe\n\nC:/Program Files (x86)/VideoLAN/VLC/vlc.exe\n\nC:/Arquivos de Programas/VideoLAN/VLC/vlc.exe\n\nC:/Arquivos de Programas (x86)/VideoLAN/VLC/vlc.exe')