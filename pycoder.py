import os
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


def main():
    create_mp4()

if __name__ == "__main__":
    main()