import os
import subprocess
import sys

def check_imagemagick_installed():
    try:
        subprocess.run(["convert", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ImageMagick is not installed or not available in PATH.")
        sys.exit(1)

def get_image_dimensions(image_path):
    try:
        result = subprocess.run(
            ["identify", "-format", "%wx%h", image_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        width, height = map(int, result.stdout.strip().split('x'))
        return width, height
    except subprocess.CalledProcessError:
        print(f"Failed to get dimensions of {image_path}")
        sys.exit(1)

def convert_to_portrait(input_path):
    # Validate file
    if not os.path.isfile(input_path):
        print(f"The file '{input_path}' does not exist.")
        sys.exit(1)

    # Output path in same directory with _portrait added
    base_dir = os.path.dirname(input_path)
    base_name = os.path.basename(input_path)
    name, ext = os.path.splitext(base_name)
    output_path = os.path.join(base_dir, f"{name}_portrait{ext}")

    # Get current dimensions
    width, height = get_image_dimensions(input_path)

    # Calculate new height for portrait format (4:3 ratio)
    new_height = int(width * 4 / 3)

    # Run ImageMagick convert
    try:
        subprocess.run([
            "convert",
            input_path,
            "-background", "white",
            "-gravity", "center",
            "-extent", f"{width}x{new_height}",
            output_path
        ], check=True)
        print(f"Portrait image saved to: {output_path}")
    except subprocess.CalledProcessError:
        print("ImageMagick convert failed.")
        sys.exit(1)

if __name__ == "__main__":
    check_imagemagick_installed()
    input_image = input("Enter the full path of the input image: ").strip()
    convert_to_portrait(input_image)
