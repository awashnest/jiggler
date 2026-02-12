# Mouse Jiggler ☕

A lightweight Windows system tray application that keeps your computer awake by periodically moving the mouse cursor.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Windows](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## Features

- ☕ **Coffee cup icon** - Brown when active, gray when paused
- 🖥️ **System tray** - Runs minimized in the system tray, out of your way
- 🔄 **Toggle on/off** - Click the tray icon to pause/resume jiggling
- 🚀 **Auto-start** - Starts jiggling immediately when launched
- 👻 **Subtle movement** - Moves mouse just 1 pixel every 30 seconds (invisible to users)

## Download

Download the latest `MouseJiggler.exe` from the [Releases](../../releases) page.

## Usage

1. Double-click `MouseJiggler.exe` to run
2. Look for the coffee cup icon in your system tray (may be in the overflow area ▲)
3. **Left-click** the icon to toggle jiggling on/off
4. **Right-click** for the menu with Quit option

### Add to Windows Startup

To have Mouse Jiggler start automatically with Windows:

1. Press `Win + R`
2. Type `shell:startup` and press Enter
3. Create a shortcut to `MouseJiggler.exe` in this folder

## Building from Source

### Prerequisites

- Python 3.8 or higher
- pip

### Build Steps

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/MouseJiggler.git
cd MouseJiggler

# Install dependencies
pip install -r requirements.txt

# Generate the icon
python create_icon.py

# Build the executable
pyinstaller --onefile --windowed --icon=coffee_cup.ico --name=MouseJiggler mouse_jiggler.py
```

Or simply run `build.bat` on Windows.

The executable will be created in the `dist` folder.

## How It Works

The application uses the Windows API to:
1. Get the current cursor position
2. Move it 1 pixel to the right
3. Move it back to the original position
4. Repeat every 30 seconds

This subtle movement is enough to prevent screen savers, sleep mode, and status changes in communication apps, while being completely invisible to the user.

## License

MIT License - feel free to use, modify, and distribute.

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.
