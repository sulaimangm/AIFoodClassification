import os
import csv
from PIL import Image, ImageTk
import piexif
import tkinter as tk


class ImageMetadataGUI:
    def __init__(self, root, image_paths):
        self.root = root
        self.image_paths = image_paths
        self.current_index = 0

        # Create GUI elements
        self.image_label = tk.Label(root)
        self.image_label.pack()
        self.description_entry = tk.Entry(root, width=50)
        self.description_entry.pack()
        self.next_button = tk.Button(
            root, text="Next", command=self.next_image)
        self.next_button.pack()

        # Load the first image
        self.load_image()

    def load_image(self):
        image_path = self.image_paths[self.current_index]

        # Load and display the image
        image = Image.open(image_path)
        image = image.resize((500, 500))
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo

    def next_image(self):
        # Get the description entered by the user
        description = self.description_entry.get()

        # Save the image metadata to a CSV file
        self.save_metadata(description)

        # Clear the description entry
        self.description_entry.delete(0, tk.END)

        # Load the next image or exit if all images are processed
        self.current_index += 1
        if self.current_index < len(self.image_paths):
            self.load_image()
        else:
            self.root.quit()

    def save_metadata(self, description):
        image_path = self.image_paths[self.current_index]

        # Extract image metadata
        metadata = get_image_metadata(image_path)

        # Add the description to the metadata
        metadata['Description'] = description

        # Save the metadata to the CSV file
        with open('image_metadata.csv', 'a', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=list(metadata.keys()))
            if csv_file.tell() == 0:
                writer.writeheader()
            writer.writerow(metadata)


def get_image_metadata(image_path):
    with Image.open(image_path) as img:
        exif_data = img._getexif()
        if exif_data is None:
            exif_data = {}

        metadata = {
            'Image Name': os.path.basename(image_path),
            'DateTime': exif_data.get(piexif.ExifIFD.DateTimeOriginal, 'N/A'),
            'GPSInfo': exif_data.get(piexif.GPSIFD.GPSAreaInformation, 'N/A')
        }
    return metadata


def filter_images(image_paths):
    filtered_paths = []
    with open('image_metadata.csv', 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if row['Description']:
                filtered_paths.append(row['Image Name'])

    filtered_image_paths = []
    for image_path in image_paths:
        image_name = os.path.basename(image_path)
        if image_name not in filtered_paths:
            filtered_image_paths.append(image_path)

    return filtered_image_paths


def write_image_metadata(image_path):
    with Image.open(image_path) as img:
        exif_data = img._getexif()
        if exif_data is None:
            exif_data = {}

        metadata = {
            'Image Name': os.path.basename(image_path),
            'DateTime': exif_data.get(piexif.ExifIFD.DateTimeOriginal, 'N/A'),
            'GPSInfo': exif_data.get(piexif.GPSIFD.GPSLongitude, 'N/A')
        }

    # Save the metadata to the CSV file
        with open('image_metadata.csv', 'a', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=list(metadata.keys()))
            if csv_file.tell() == 0:
                writer.writeheader()
            writer.writerow(metadata)


def main():
    folder_path = 'D:\McMaster\SEP 799 - Project\Phase 2\Food-min'
    image_paths = []

    # Collect image paths
    for filename in os.listdir(folder_path):
        if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.HEIC'):
            image_paths.append(os.path.join(folder_path, filename))

    for imagepath in image_paths:
        write_image_metadata(imagepath)


'''
    # Filter image paths based on existing descriptions in the CSV file
    filtered_image_paths = filter_images(image_paths)

    # Create the main window
    root = tk.Tk()
    root.title("Image Metadata")

    # Create the GUI object
    gui = ImageMetadataGUI(root, filtered_image_paths)

    # Start the main event loop
    root.mainloop()

    print("Image metadata saved to 'image_metadata.csv'")
'''

if __name__ == '__main__':
    main()
