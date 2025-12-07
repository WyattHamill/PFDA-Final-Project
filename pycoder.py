import os
import glob
import sys
from moviepy import ImageSequenceClip
import OpenImageIO as oiio

def ask_for_inputs():
    print("=== Pycoder: PNG Sequence to MP4 Converter ===")

    folder = input("Enter the folder path of the PNG sequence: ").strip()
    if not os.path.isdir(folder):
        print("Error: That folder doesn't exist.")
        return None, None, None

    while True:
        fps_input = input("Set MP4 frames per second (FPS): ").strip()
        try:
            fps = int(fps_input)
            if fps > 0:
                break
            else:
                print("FPS must be a positive number.")
        except:
            print("Please enter a valid whole number.")

    file_name = input("Set MP4 file name: ").strip()
    if file_name == "":
        print("Error: File name cannot be empty.")
        return None, None, None
    if not file_name.lower().endswith(".mp4"):
        file_name = file_name + ".mp4"
    return folder, fps, file_name


def load_png_sequence(folder):
    png_files = sorted(glob.glob(os.path.join(folder, "*.png")))
    if len(png_files) == 0:
        print("No PNG files found in that folder.")
        return None
    print("Found", len(png_files), "PNG files.")
    return png_files


def build_mp4(png_files, fps, output_path):
    print("Pycoder - Creating your MP4...")
    clip = ImageSequenceClip(png_files, fps=fps)
    clip.write_videofile(output_path, codec="libx264")

    print("\n------------------------------")
    print("Pycoder - PNG sequence to MP4 successfully created!")
    print("Saved as:", output_path)
    print("------------------------------\n")


def create_mp4():
    folder, fps, file_name = ask_for_inputs()
    if not folder:
        return

    png_files = load_png_sequence(folder)
    if not png_files:
        return

    output_path = os.path.join(folder, file_name)
    build_mp4(png_files, fps, output_path)


def detect_input_type(path):
    if os.path.isdir(path):
        pngs = glob.glob(os.path.join(path, "*.png"))
        exrs = glob.glob(os.path.join(path, "*.exr"))
        if len(pngs) > 0 or len(exrs) > 0:
            return "sequence"
    else:
        if path.lower().endswith(".png") or path.lower().endswith(".exr"):
            return "single_file"

def convert_single_image(input_file, new_ext):
    print("Pycoder - Converting your image...")
    img_input = oiio.ImageInput.open(input_file)
    if not img_input:
        print("Could not read:", input_file)
        return
    
    spec = img_input.spec()
    pixels = img_input.read_image()
    img_input.close()
    output_file = os.path.splitext(input_file)[0] + "." + new_ext
    out = oiio.ImageOutput.create(output_file)
    if not out:
        print("Could not create output file:", output_file)
        return
    
    out.open(output_file, spec)
    out.write_image(pixels)
    out.close()
    print("Saved:", output_file)


def convert_image_sequence(folder, new_ext):
    print("Pycoder - Converting your image sequence...")
    files = sorted(glob.glob(os.path.join(folder, "*.png"))) + \
            sorted(glob.glob(os.path.join(folder, "*.exr")))
    if len(files) == 0:
        print("No PNG or EXR images found to convert.")
        return
    out_folder = os.path.join(folder, "pycoder_" + new_ext + "_conversion")
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
    for sequence in files:
        img_input = oiio.ImageInput.open(sequence)
        spec = img_input.spec()
        pixels = img_input.read_image()
        img_input.close()
        base = os.path.splitext(os.path.basename(sequence))[0]
        out_path = os.path.join(out_folder, base + "." + new_ext)
        out = oiio.ImageOutput.create(out_path)
        if not out:
            print("Failed to write:", out_path)
            continue

        out.open(out_path, spec)
        out.write_image(pixels)
        out.close()

        print("Converted:", base, "->", out_path)

    print("\n------------------------------")
    print("Pycoder - Image conversion successful!")
    print("Saved as:", out_folder)
    print("------------------------------\n")

def img_convert():
    print("=== Pycoder - Image Format Converter ===")

    path = input("Enter a file or folder path to convert: ").strip()
    input_type = detect_input_type(path)
    new_ext = input("Set converted file format:").strip().lower()
    print(new_ext)
    if new_ext != "png" and new_ext != "exr":
        print("Invalid choice. File format must be png or exr.")
        return
    
    if input_type == "single_file":
        convert_single_image(path, new_ext)
    elif input_type == "sequence":
        convert_image_sequence(path, new_ext)


def main():
    if len(sys.argv) < 2:
        print("Usage: python pycoder.py <command>")
        print("Commands:")
        print("   create_mp4   - Turn a PNG sequence into an MP4 video")
        print("   img_convert  - Convert PNG <-> EXR file or sequence")
        return
    command = sys.argv[1]
    if command == "create_mp4":
        create_mp4()
    elif command == "img_convert":
        img_convert()
    else:
        print("Unknown command:", command)
        print("Available commands: create_mp4, img_convert")


if __name__ == "__main__":
    main()