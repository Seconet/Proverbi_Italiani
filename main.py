#!/usr/bin/env python3 
import tkinter as tk
from gui.app_proverbi import AppProverbi

def main():
    root = tk.Tk()
    app = AppProverbi(root)
    root.mainloop()

if __name__ == "__main__":
    main()