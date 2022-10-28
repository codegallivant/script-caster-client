#pip modules
import sys
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import pyautogui #Required for tkinter.ttk
import threading   
import ctypes
import datetime
import subprocess
import PIL
import pystray
import tkinter as tk
import tkinter.font
import tkinter.filedialog
# import sv_ttk
import socket
import atexit
import shutil
import json
from cryptography.fernet import Fernet
from github import Github 

#local imports
import CLIENT_CONSTANTS
import src.exterior_connection as exterior_connection
from src.server_connection import Server

		
