# FileFlux (ffx)

[![License](https://img.shields.io/badge/License-MIT-red?style=flat-square)](LICENSE)   [![Python](https://img.shields.io/badge/Python-3.8%2B-darkgreen?style=flat-square)]()   [![Platform](https://img.shields.io/badge/Platform-Windows%20-blue?style=flat-square)]()   [![GitHub Stars](https://img.shields.io/github/stars/ikeshavvarshney/FileFlux?style=flat-square&color=yellow)]()  
```
██████╗██╗██╗     ██████╗██████╗██╗    ██╗   ██╗██╗  ██╗
██╔═══╝██║██║     ██╔═══╝██╔═══╝██║    ██║   ██║╚██╗██╔╝
████╗  ██║██║     ████╗  ████╗  ██║    ██║   ██║ ╚███╔╝
██╔═╝  ██║██║     ██╔═╝  ██╔═╝  ██║    ██║   ██║ ██╔██╗
██║    ██║██████╗ ██████╗██║    ██████╗╚██████╔╝██╔╝ ██╗
╚═╝    ╚═╝╚═════╝ ╚═════╝╚═╝    ╚═════╝ ╚═════╝ ╚═╝  ╚═╝
```
**Author:** [Keshav Varshney](https://github.com/ikeshavvarshney)  
**Version:** 1.3

**FileFlux** is a sleek CLI tool designed to **manage files, folders, and paths efficiently**. It simplifies complex file operations, adds interactive search capabilities, and even includes a lightweight password manager. Built for developers, power users, and productivity enthusiasts, FileFlux makes terminal-based file management fast, safe, and intuitive.

---

## ✨ Features
- 📁 **File Operations:** Copy, move, delete, rename, and create directories with smart disk-space checks and warnings.
- 🗂️ **Path Shortcuts:** Save favorite directories and jump to them instantly.
- 🔍 **Search:** Search inside files or by filename, with pattern matching and interactive fuzzy search.
- 📦 **Archive & Extract:** Compress folders and files or extract archives with ease.
- 📋 **Clipboard Integration:** Copy text or passwords directly to the system clipboard.
- 🎛️ **Interactive Fuzzy Search:** Filter and select files visually in the terminal with fallback support.
- 🔐 **Password Manager:** Save and retrieve passwords securely inside the CLI database.
- 🎨 **Rich CLI UI:** Color-coded outputs, warnings, and a stylish banner/logo for a professional terminal experience.

---

## ⚙️ Why Use FileFlux?
- Safety-first: Checks disk space and file conflicts before operations  
- Fast workflow: Path saving, jumping, and interactive searches streamline tasks  
- Lightweight: Minimal dependencies, optional enhancements only  

---

## 🛠️ Tech Stack
- **Python 3.8+**  
- **Standard Python libraries:** `os`, `sys`, `shutil`, `json`, `argparse`, `subprocess`, `zipfile`, `mimetypes` 
- **External Libraries:** `colorama`, `pyperclip` 

---

## 📂 Folder Structure
```
FileFlux/
├── ffx.py           # Main CLI script
├── ffx.bat          # Batch wrapper for Windows
├── run.md           # Commands & usage guide
├── README.md        # Project documentation
└── LICENSE          # License file
```

# 🚀 Installation & Setup

This guide helps you get **FileFlux** up and running on your system quickly.  

---

## ⚙️ Prerequisites

- Python 3.x installed  
- Windows 10 or above
- Libraries: `colorama`, `pyperclip`
  
---

## 📝 Installation Steps

1. **Clone the repository or download the files**  

   ```
   git clone https://github.com/ikeshavvarshney/FileFlux.git
   cd FileFlux
   ```
2. **Install required libraries**
   ```
   pip install colorama pyperclip
   ```
3. Run FileFlux
   - Option 1 (basic): Run commands using Python:
     ```
     python ffx.py <command> [args]
     ```
   - Option 2 (optional): Add FileFlux to your system PATH for global usage with direct commands:
     ```
     ffx <command> [args]
     ```
<p align='center'>"Efficiency is not about doing more, it's about doing it smarter."</p>  
