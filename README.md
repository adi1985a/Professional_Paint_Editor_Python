# 🎨🖌️ Professional Paint Editor: Advanced Image Editor ✨
_A desktop image editing application built with Python and PyQt5, offering a rich set of drawing tools, shape tools, image filters, and effects._

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.6%2B-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![PyQt5](https://img.shields.io/badge/PyQt5-GUI%20Framework-41CD52.svg?logo=qt)](https://riverbankcomputing.com/software/pyqt/intro)
[![Pillow](https://img.shields.io/badge/Pillow-Image%20Processing-9B59B6.svg)]()

## 📋 Table of Contents
1.  [Overview](#-overview)
2.  [Key Features](#-key-features)
    *   [Drawing & Shape Tools](#-drawing--shape-tools)
    *   [Image Effects & Adjustments](#-image-effects--adjustments)
    *   [Core Functionality](#-core-functionality)
3.  [Keyboard Shortcuts](#-keyboard-shortcuts)
4.  [Screenshots (Conceptual)](#-screenshots-conceptual)
5.  [System Requirements & Dependencies](#-system-requirements--dependencies)
6.  [Installation](#️-installation)
7.  [Running the Application](#️-running-the-application)
8.  [File Structure (Actual)](#-file-structure-actual)
9.  [Contributing](#-contributing)
10. [License](#-license)
11. [Author & Contact](#-author--contact)

## 📄 Overview

**Professional Paint Editor**, created by Adrian Lesniak, is a desktop application for image editing, offering a wide set of drawing, shape, filter, and effect tools. Built in **Python** using **PyQt5**, it provides a modern, bright, and user-friendly interface. The program allows you to draw, edit, apply filters, undo/redo changes, and save or open image files. It also features error logging and remembers the user's last settings.

> **What's new:**
> - Bright, pastel interface with icons and decorative elements
> - Info bar with menu descriptions and author
> - Action feedback: after each operation, a message is shown and you return to the menu
> - Error logging system to file
> - Saving and loading user settings

<br>
<p align="center">
  <img src="screenshots/1.gif" width="90%">
</p>
<br>

## ✨ Key Features

### 🖌️ Drawing & Shape Tools
*   **Brush**: Free-form drawing with customizable brush size.
*   **Eraser**: Erase portions of the image.
*   **Spray**: Simulate a spray paint effect.
*   **Line Tool**: Draw straight lines.
*   **Rectangle Tool**: Draw rectangles.
*   **Circle/Ellipse Tool**: Draw circles and ellipses.
*   **Fill Tool (Paint Bucket)**: Fill areas with a selected color.
*   **Text Tool**: Add text overlays on the image.
*   **Gradient Tool**: Create smooth color transitions.
*   **Polygon Tool**: Draw custom multi-sided shapes.
*   **Selection Tool**: (rectangular selection)

### 🪄 Image Effects & Adjustments
*   **Blur**: Apply blur effect.
*   **Sharpen**: Enhance sharpness.
*   **Grayscale**: Convert to grayscale.
*   **Invert Colors**: Invert all colors.
*   **Brightness Adjustment**: Modify brightness.
*   **Contrast Adjustment**: Alter contrast.

### ⚙️ Core Functionality
*   **Color Picker**: Select foreground and background colors.
*   **File Operations**:
    *   Create a **New Image** (Ctrl+N).
    *   **Open** image files (Ctrl+O) (PNG, JPG, BMP).
    *   **Save** the current image (Ctrl+S).
*   **Undo/Redo Support**:
    *   **Undo** (Ctrl+Z).
    *   **Redo** (Ctrl+Y).
*   **Canvas Management**: Central drawing area.
*   **Zoom & Pan**: (Mouse wheel and spacebar supported).
*   **User Settings**: Remembers last used color and tool.
*   **Error Logging**: Logs errors to `error_log.txt`.
*   **Info Bar**: Shows menu options and author at the top.
*   **Action Feedback**: After each action, a message is shown and user returns to menu.
*   **Bright, modern UI**: Pastel colors, icons, decorative frames.
*   **Multi-platform**: Works on Windows, Linux, macOS.
*   **Planned**: Layer support (not yet implemented).

## ⌨️ Keyboard Shortcuts

*   **`Ctrl + N`**: New Image
*   **`Ctrl + O`**: Open Image
*   **`Ctrl + S`**: Save Image
*   **`Ctrl + Z`**: Undo
*   **`Ctrl + Y`**: Redo
*   **Space**: Pan canvas
*   **Mouse wheel**: Zoom canvas

## 🖼️ Screenshots (Conceptual)

_Example screenshots of the Professional Paint Editor application, including: the main interface with a canvas, toolbars, menu bar, color picker, and examples of drawing tools and image effects being applied._

<p align="center">
  <img src="screenshots\1.jpg" width="300"/>
  <img src="screenshots\2.jpg" width="300"/>
  <img src="screenshots\3.jpg" width="300"/>
  <img src="screenshots\4.jpg" width="300"/>
  <img src="screenshots\5.jpg" width="300"/>
  <img src="screenshots\6.jpg" width="300"/>
  <img src="screenshots\7.jpg" width="300"/>
  <img src="screenshots\8.jpg" width="300"/>
  <img src="screenshots\9.jpg" width="300"/>
  <img src="screenshots\10.jpg" width="300"/>
</p>

## ⚙️ System Requirements & Dependencies

### Software:
*   **Python**: Version 3.6 or higher.
*   **Libraries**:
    *   `PyQt5`: GUI framework.
    *   `Pillow`: Image file loading, saving, and manipulation.

### Operating System:
*   Windows, macOS, Linux (multi-platform).

## 🛠️ Installation

1.  **Ensure Python 3.6+ is Installed**:
    Verify by typing `python --version` or `python3 --version` in your terminal. If not installed, download from [python.org](https://www.python.org/).

2.  **Clone or Download the Repository**:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

3.  **Set Up a Virtual Environment (Recommended)**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

4.  **Install Required Libraries**:
    ```bash
    pip install PyQt5 Pillow
    ```

## ▶️ Running the Application

1.  Navigate to the project directory (with `main.py`).
2.  Activate your virtual environment (if used).
3.  Run:
    ```bash
    python main.py
    ```

## 🗂️ File Structure (Actual)

*   `main.py`: Main script, initializes the app, sets up window, menu, toolbars, color picker, and integrates all logic.
*   `canvas.py`: Main drawing canvas widget and image logic (drawing, filters, file operations).
*   `tools.py`: ToolBar logic and tool selection.
*   `color_picker.py`: Color picker widget.
*   `error_logger.py`: Error logging to file.
*   `README.md`: This documentation file.
*   `LICENSE`: License info.

## 📝 Technical Notes

*   **GUI Framework**: Built using PyQt5.
*   **Image Processing**: Pillow (PIL fork) for image manipulation.
*   **Object-Oriented Design**: Classes for tools, canvas, color picker, etc.
*   **Event Handling**: PyQt5 signals/slots for user actions.
*   **Performance**: Undo/redo stack, efficient drawing, and filter application.
*   **Error Logging**: All errors are logged to `error_log.txt`.
*   **User Experience**: Bright, modern UI, icons, info bar, and feedback after actions.

## 🤝 Contributing

Contributions to **Professional Paint Editor** are highly encouraged! If you have ideas for:

*   New drawing tools or effects
*   Layer system (planned)
*   UI/UX improvements
*   Performance enhancements
*   More file formats
*   Documentation

1.  Fork the repository.
2.  Create a new branch for your feature (`git checkout -b feature/LayerSystem`).
3.  Make your changes.
4.  Commit (`git commit -m 'Feature: ...'`).
5.  Push (`git push origin feature/LayerSystem`).
6.  Open a Pull Request.

Please ensure your code is well-commented, follows Python best practices (PEP 8), and includes type hints where appropriate.

## 📃 License

This project is licensed under the **MIT License**.
See the LICENSE file for details.

## 👤 Author & Contact

Application concept by **Adrian Lesniak**.
For questions, feedback, or issues, please open an issue on the GitHub repository or contact the repository owner.

---
🖌️ _Unleash your creativity with a powerful Python-based paint editor!_
