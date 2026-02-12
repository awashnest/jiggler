"""
Generate coffee cup icon file (.ico) for the application.
"""

from PIL import Image, ImageDraw

def create_coffee_icon():
    """Create a coffee cup icon at multiple sizes for .ico file."""
    sizes = [16, 32, 48, 64, 128, 256]
    images = []
    
    for size in sizes:
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Scale factor
        s = size / 64
        
        # Colors - warm brown coffee colors
        cup_color = (139, 90, 43)  # Saddle brown
        coffee_color = (101, 67, 33)  # Dark brown
        steam_color = (180, 180, 180, 180)  # Light gray steam
        highlight = (180, 130, 70)  # Lighter brown for highlights
        
        # Draw steam (three wavy curves)
        if size >= 32:
            for i, x_offset in enumerate([20, 32, 44]):
                for j in range(3):
                    y = 6 + j * 5
                    offset = 3 if (j + i) % 2 == 0 else -3
                    x = int((x_offset + offset) * s)
                    y_scaled = int(y * s)
                    r = max(1, int(2 * s))
                    draw.ellipse([x - r, y_scaled, x + r, y_scaled + int(3 * s)], 
                               fill=steam_color)
        
        # Cup dimensions
        cup_top = int(22 * s)
        cup_bottom = int(54 * s)
        cup_left = int(12 * s)
        cup_right = int(48 * s)
        
        # Cup body with rounded corners
        radius = max(1, int(5 * s))
        draw.rounded_rectangle([cup_left, cup_top, cup_right, cup_bottom], 
                              radius=radius, fill=cup_color)
        
        # Coffee surface (dark brown)
        coffee_top = cup_top + int(3 * s)
        coffee_height = int(10 * s)
        draw.rectangle([cup_left + int(4 * s), coffee_top, 
                       cup_right - int(4 * s), coffee_top + coffee_height], 
                       fill=coffee_color)
        
        # Highlight on cup
        highlight_width = max(1, int(3 * s))
        draw.rectangle([cup_left + int(2 * s), cup_top + int(15 * s),
                       cup_left + int(2 * s) + highlight_width, cup_bottom - int(5 * s)],
                       fill=highlight)
        
        # Cup handle
        handle_left = cup_right - int(2 * s)
        handle_right = cup_right + int(12 * s)
        handle_top = cup_top + int(8 * s)
        handle_bottom = cup_bottom - int(8 * s)
        handle_width = max(2, int(4 * s))
        
        draw.arc([handle_left, handle_top, handle_right, handle_bottom], 
                 start=-90, end=90, fill=cup_color, width=handle_width)
        
        # Saucer
        saucer_top = cup_bottom - int(2 * s)
        saucer_bottom = cup_bottom + int(8 * s)
        draw.ellipse([int(8 * s), saucer_top, int(52 * s), saucer_bottom], 
                    fill=cup_color)
        
        images.append(img)
    
    # Save as .ico with all sizes
    images[0].save('coffee_cup.ico', format='ICO', 
                   sizes=[(s, s) for s in sizes],
                   append_images=images[1:])
    
    print("Created coffee_cup.ico successfully!")
    return 'coffee_cup.ico'

if __name__ == "__main__":
    create_coffee_icon()
