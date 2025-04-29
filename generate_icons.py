from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size):
    # Create a new image with a transparent background
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Draw a film strip frame
    frame_color = (66, 133, 244)  # Google Blue
    border_width = max(1, size // 16)
    
    # Draw the main rectangle
    draw.rectangle(
        [(border_width, border_width), (size - border_width, size - border_width)],
        fill=frame_color
    )
    
    # Draw the film strip holes
    hole_size = size // 8
    hole_spacing = size // 4
    for i in range(3):
        y = size // 2 - hole_size // 2
        x = hole_spacing * (i + 1)
        draw.ellipse(
            [(x - hole_size//2, y - hole_size//2), (x + hole_size//2, y + hole_size//2)],
            fill=(255, 255, 255)
        )
    
    return image

def main():
    # Create the images directory if it doesn't exist
    os.makedirs('new-moview-finder-extension/images', exist_ok=True)
    
    # Generate icons in different sizes
    sizes = [16, 48, 128]
    for size in sizes:
        icon = create_icon(size)
        icon.save(f'new-moview-finder-extension/images/icon{size}.png')

if __name__ == '__main__':
    main() 