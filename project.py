import os
import glob
import sys
from moviepy import ImageSequenceClip
import OpenImageIO as oiio
import tkinter as tk
from tkinter import filedialog

def browse_folder():
    root = tk.Tk()
    root.withdraw()
    folder = filedialog.askdirectory()
    root.destroy()
    return folder


def browse_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    root.destroy()
    return file_path


def choose_file_or_folder():
    choice = {"result": None}

    def pick_file():
        choice["result"] = "file"
        win.destroy()

    def pick_folder():
        choice["result"] = "folder"
        win.destroy()

    win = tk.Tk()
    win.title("Pycoder - Choose Option")
    win.geometry("250x120")
    label = tk.Label(win, text="Convert a file or a folder?")
    label.pack(pady=10)
    
    btn_file = tk.Button(win, text="Convert File", command=pick_file, width=15)
    btn_file.pack(pady=5)
    btn_folder = tk.Button(win, text="Convert Folder", command=pick_folder, width=15)
    btn_folder.pack(pady=5)

    win.mainloop()
    return choice["result"]


def ask_for_inputs():
    print("=== Pycoder: Image Sequence to MP4 Converter ===")
    print("Select the folder with the image sequence.")
    folder = browse_folder()
    if not folder or not os.path.isdir(folder):
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
    print("\nPycoder - Creating your MP4...")
    clip = ImageSequenceClip(png_files, fps=fps)
    clip.write_videofile(output_path, codec="libx264")

    print("\n------------------------------")
    print("Pycoder - Image sequence to MP4 successfully created!")
    print("Saved as:", output_path)
    print("------------------------------\n")


def delete_folder(folder):
    if os.path.exists(folder):
        for image in glob.glob(os.path.join(folder, "*")):
            try:
                os.remove(image)
            except:
                pass
        try:
            os.rmdir(folder)
        except:
            pass


def detect_input_type(path):
    if os.path.isdir(path):
        pngs = glob.glob(os.path.join(path, "*.png"))
        exrs = glob.glob(os.path.join(path, "*.exr"))
        jpgs = glob.glob(os.path.join(path, "*.jpg")) + glob.glob(os.path.join(path, "*.jpeg"))
        if len(pngs) > 0 or len(exrs) > 0 or len(jpgs) > 0:
            return "sequence"
        else:
            return "empty_folder"
    else:
        if path.lower().endswith(".png") or path.lower().endswith(".exr") or \
           path.lower().endswith(".jpg") or path.lower().endswith(".jpeg"):
            return "single_file"
        else:
            return "unknown_file"

def convert_single_image(input_file, new_ext):
    print("Converting single image...")
    try:
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

    except Exception as e:
        print("Error converting image:", e)


def convert_image_sequence(folder, new_ext):
    print("Pycoder - Converting your image sequence...")
    files = sorted(glob.glob(os.path.join(folder, "*.png"))) + \
            sorted(glob.glob(os.path.join(folder, "*.exr"))) + \
            sorted(glob.glob(os.path.join(folder, "*.jpg"))) + \
            sorted(glob.glob(os.path.join(folder, "*.jpeg")))

    if len(files) == 0:
        print("No PNG, EXR, or JPG images found to convert.")
        return
    out_folder = os.path.join(folder, "pycoder_" + new_ext + "_conversion")
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)
    for sequence in files:
        try:
            img_input = oiio.ImageInput.open(sequence)
            if not img_input:
                print("Skipping, couldn't read:", sequence)
                continue
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

            print("Converted:", base, "->", new_ext)

        except Exception as e:
            print("Error converting", sequence, "-", e)

    print("\n------------------------------")
    print("Pycoder - Image conversion successful!")
    print("Saved as:", out_folder)
    print("------------------------------\n")

    return out_folder


def create_mp4():
    folder, fps, file_name = ask_for_inputs()
    if not folder:
        return

    pngs = sorted(glob.glob(os.path.join(folder, "*.png")))
    exrs = sorted(glob.glob(os.path.join(folder, "*.exr")))

    if len(exrs) > 0 and len(pngs) == 0:
        print("EXR image sequence found. Converting EXR to PNG for MP4 compatability")
        temp_png_folder = convert_image_sequence(folder, "png")

        png_files = load_png_sequence(temp_png_folder)
        output_path = os.path.join(folder, file_name)
        build_mp4(png_files, fps, output_path)
        print("Cleaning up file conversion...")
        delete_folder(temp_png_folder)
        print("Pycoder - File conversion complete!.\n")
        return

    output_path = os.path.join(folder, file_name)
    build_mp4(pngs, fps, output_path)


def img_convert():
    print("=== Pycoder - Image Format Converter ===")
    print("Pycoder Window - Select whether to convert single file or entire folder.")
    
    user_choice = choose_file_or_folder()
    if user_choice == "file":
        path = browse_file()
    else:
        path = browse_folder()

    if not path:
        print("Nothing was selected.")
        return
    input_type = detect_input_type(path)
    new_ext = input("Set converted file format:").strip().lower()
    if new_ext not in ["png", "exr", "jpg"]:
        print("Invalid choice. File format must be png, exr, or jpg.")
        return

    if input_type == "single_file":
        convert_single_image(path, new_ext)
    elif input_type == "sequence":
        convert_image_sequence(path, new_ext)
    else:
        print("No images found in folder.")


def main():
    print("=== Pycoder - Media Encoding and Conversion ===")

    while True:
        print("\nConversion tool selection index:")
        print("1) Create MP4 - Image sequence to MP4")
        print("2) Image Convert - Convert between PNG, EXR, and JPG")
        print("q) Quit\n")

        choice = input("Select tool number: ").strip().lower()

        if choice == "1":
            create_mp4()
        elif choice == "2":
            img_convert()
        elif choice == "q":
            print("Thanks for using Pycoder!")
            break
        else:
            print("Invalid choice. Please enter a valid tool number. (q to quit)")


if __name__ == "__main__":
    main()