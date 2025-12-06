import os
import glob
import sys
from moviepy import ImageSequenceClip

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


def main():
    if len(sys.argv) < 2:
        print("Usage: python pycoder.py <command>")
        print("Commands:")
        print("   create_mp4   - Turn a PNG sequence into an MP4 video")
        return
    command = sys.argv[1]
    if command == "create_mp4":
        create_mp4()
    else:
        print("Unknown command:", command)
        print("Available commands: create_mp4")


if __name__ == "__main__":
    main()