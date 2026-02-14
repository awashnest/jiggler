"""
Mouse Jiggler - System Tray Application
Keeps your computer awake by periodically moving the mouse cursor.
"""

import threading
import time
import sys
import ctypes
from ctypes import wintypes

# Windows API imports for mouse movement (no external dependencies needed)
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

# Execution state flags to prevent sleep/display off
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002

class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

def get_cursor_pos():
    """Get current cursor position."""
    pt = POINT()
    user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y

def set_cursor_pos(x, y):
    """Set cursor position."""
    user32.SetCursorPos(x, y)

def move_mouse():
    """Move mouse slightly and return to original position.
    Uses mouse_event instead of SetCursorPos so Windows registers real input
    and resets the idle timer.
    """
    MOUSEEVENTF_MOVE = 0x0001
    # Move 1 pixel right, then 1 pixel left (relative movement)
    user32.mouse_event(MOUSEEVENTF_MOVE, 1, 0, 0, 0)
    time.sleep(0.05)
    user32.mouse_event(MOUSEEVENTF_MOVE, -1, 0, 0, 0)
    # Also explicitly reset the idle timer as a safety net
    kernel32.SetThreadExecutionState(
        ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED
    )

class MouseJiggler:
    def __init__(self):
        self.running = False
        self.jiggle_thread = None
        self.interval = 30  # seconds between jiggles
        self.icon = None
        
    def jiggle_loop(self):
        """Main jiggle loop that runs in background thread."""
        while self.running:
            move_mouse()
            # Sleep in small increments to respond faster to stop
            for _ in range(int(self.interval * 10)):
                if not self.running:
                    break
                time.sleep(0.1)
    
    def start_jiggling(self):
        """Start the mouse jiggling."""
        if not self.running:
            self.running = True
            # Tell Windows to keep the system and display awake
            kernel32.SetThreadExecutionState(
                ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED
            )
            self.jiggle_thread = threading.Thread(target=self.jiggle_loop, daemon=True)
            self.jiggle_thread.start()
            self.update_icon()
    
    def stop_jiggling(self):
        """Stop the mouse jiggling."""
        self.running = False
        # Allow Windows to sleep again
        kernel32.SetThreadExecutionState(ES_CONTINUOUS)
        if self.jiggle_thread:
            self.jiggle_thread.join(timeout=1)
        self.update_icon()
    
    def toggle_jiggling(self, icon=None, item=None):
        """Toggle jiggling on/off."""
        if self.running:
            self.stop_jiggling()
        else:
            self.start_jiggling()
    
    def update_icon(self):
        """Update the system tray icon based on state."""
        if self.icon:
            self.icon.icon = create_icon(self.running)
            self.icon.title = "Mouse Jiggler - Active" if self.running else "Mouse Jiggler - Paused"
    
    def quit_app(self, icon=None, item=None):
        """Quit the application."""
        self.running = False
        # Restore normal sleep behavior on exit
        kernel32.SetThreadExecutionState(ES_CONTINUOUS)
        if self.icon:
            self.icon.stop()

def create_icon(active=False):
    """Create a coffee cup icon."""
    from PIL import Image, ImageDraw
    
    # Create image with transparency
    size = 64
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Colors
    if active:
        cup_color = (139, 90, 43)  # Brown when active
        steam_color = (100, 100, 100, 200)  # Gray steam
    else:
        cup_color = (100, 100, 100)  # Gray when paused
        steam_color = (150, 150, 150, 100)  # Lighter steam
    
    coffee_color = (101, 67, 33) if active else (80, 80, 80)
    
    # Draw steam (three wavy lines) when active
    if active:
        for i, x_offset in enumerate([20, 32, 44]):
            for j in range(3):
                y = 8 + j * 4
                offset = 2 if (j + i) % 2 == 0 else -2
                draw.ellipse([x_offset + offset - 2, y, x_offset + offset + 2, y + 3], 
                           fill=steam_color)
    
    # Draw cup body (rounded rectangle)
    cup_top = 22
    cup_bottom = 54
    cup_left = 12
    cup_right = 48
    
    # Cup body
    draw.rounded_rectangle([cup_left, cup_top, cup_right, cup_bottom], 
                          radius=5, fill=cup_color)
    
    # Coffee inside (dark brown rectangle)
    draw.rectangle([cup_left + 4, cup_top + 3, cup_right - 4, cup_top + 12], 
                   fill=coffee_color)
    
    # Cup handle (arc on the right side)
    handle_left = cup_right - 2
    handle_right = cup_right + 12
    handle_top = cup_top + 8
    handle_bottom = cup_bottom - 8
    
    # Outer handle
    draw.arc([handle_left, handle_top, handle_right, handle_bottom], 
             start=-90, end=90, fill=cup_color, width=4)
    
    # Saucer (ellipse at bottom)
    draw.ellipse([8, cup_bottom - 2, 52, cup_bottom + 8], fill=cup_color)
    
    return img

def create_menu(jiggler):
    """Create the system tray menu."""
    from pystray import MenuItem as item
    
    def get_status_text():
        return "Active - Click to Pause" if jiggler.running else "Paused - Click to Start"
    
    return (
        item(lambda text: get_status_text(), jiggler.toggle_jiggling, default=True),
        item('Quit', jiggler.quit_app),
    )

def main():
    """Main entry point."""
    try:
        import pystray
        from PIL import Image
    except ImportError:
        print("Required packages not found. Please install: pip install pystray pillow")
        sys.exit(1)
    
    jiggler = MouseJiggler()
    
    # Create the system tray icon
    icon = pystray.Icon(
        "mouse_jiggler",
        create_icon(False),
        "Mouse Jiggler - Paused",
        menu=pystray.Menu(*create_menu(jiggler))
    )
    
    jiggler.icon = icon
    
    # Start jiggling by default
    jiggler.start_jiggling()
    
    # Run the icon (this blocks)
    icon.run()

if __name__ == "__main__":
    main()
