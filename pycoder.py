import os
import glob
import sys
from moviepy import ImageSequenceClip

# Make function that will turn a png seq into mp4
def create_mp4():
    # Ask for the seq folder
    # Ask for fps value
    # Ask for file name
    # Get the images and make the video
    # Save the output to the folder
    print("=== Pycoder: PNG Sequence to MP4 Converter ===")
    folder = input("Enter the folder path of the PNG sequence: ").strip()
    if not os.path.isdir(folder):
        print("Error: That folder doesn't exist.")
        return
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
        return
    if not file_name.lower().endswith(".mp4"):
        file_name = file_name + ".mp4"

    png_files = sorted(glob.glob(os.path.join(folder, "*.png")))

    if len(png_files) == 0:
        print("No PNG files found in that folder.")
        return

    print("Found", len(png_files), "PNG files.")
    print("Pycoder - Creating your MP4...")

    clip = ImageSequenceClip(png_files, fps=fps)
    output_path = os.path.join(folder, file_name)
    clip.write_videofile(output_path, codec="libx264")

    print("\n------------------------------")
    print("Pycoder - PNG sequence to MP4 successfully created!")
    print("Saved as:", output_path)
    print("------------------------------\n")


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