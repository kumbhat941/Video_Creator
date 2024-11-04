from pathlib import Path
import pandas as pd
import cv2
import os

# Function to convert seconds to HH:MM:SS format
def seconds_to_hms(seconds):
    hours, remainder = divmod(int(seconds), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

# Function to read time and temperature data from the first CSV file
def read_time_temp_data(csv_file_path):
    try:
        df = pd.read_csv(csv_file_path, delimiter=';', header=0, encoding='utf-8')
        df.columns = df.columns.str.strip()

        if 'Timestamp' not in df.columns or 'Channel 1 Temp (C)' not in df.columns:
            print("Error: Required columns not found in the CSV.")
            return None, None

        time_data = df['Timestamp'].apply(lambda x: float(str(x).replace(',', '.'))).tolist()
        temperature_data = df['Channel 1 Temp (C)'].apply(lambda x: float(str(x).replace(',', '.'))).tolist()
        return time_data, temperature_data

    except Exception as e:
        print(f"Error reading time/temp CSV file: {e}")
        return None, None


# Function to read height data from the second CSV file
def read_height_data(height_csv_path):
    try:
        df = pd.read_csv(height_csv_path, delimiter=',', header=0)

        # Assuming the column names are 'Image', 'Height (pixels)', 'Height (mm)', and 'Confidence'
        image_names = df['Image'].tolist()
        height_data = df['Height (mm)'].tolist()

        return image_names, height_data

    except Exception as e:
        print(f"Error reading height CSV file: {e}")
        return None, None



# Define the path where the video will be saved
video_filepath = Path(r'C:\AlliedVision\Python_Files\Chirag_Files\Experiments_Oct')  # Update to your desired output path

# Function to create video frames with overlayed text
# Function to create video frames with overlayed text
def create_video(image_folder, time_data, temperature_data, height_data, video_filename, fps):
    image_paths = sorted(
        (f for f in os.listdir(image_folder) if f.endswith(('.tiff', '.png', '.jpg'))),
        key=lambda x: int(os.path.splitext(x)[0].split('.')[0])
    )
    image_paths = [os.path.join(image_folder, f) for f in image_paths]

    num_frames = min(len(image_paths), len(time_data), len(temperature_data), len(height_data))
    first_image = cv2.imread(image_paths[0])
    height, width, _ = first_image.shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # Convert Path object to string
    video_writer = cv2.VideoWriter(str(video_filename), fourcc, fps, (width, height))

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 3  # Set to 3 for larger text
    font_thickness = 5  # Set to 5 for thicker text
    text_color = (0, 255, 0)
    text_margin_x = 50 #width - 400
    text_margin_y = 100  # Adjusted for larger font size
    line_spacing = 90  # Increased line spacing to avoid overlap

    for i in range(num_frames):
        image_path = image_paths[i]
        image = cv2.imread(image_path)

        time_text = f"Time: {seconds_to_hms(time_data[i])}"
        temperature_text = f"Temp: {temperature_data[i]:.2f} C"
        height_text = f"Height: {height_data[i]} mm" if height_data[i] is not None else "Height: N/A mm"

        cv2.putText(image, time_text, (text_margin_x, text_margin_y), font, font_scale, text_color, font_thickness)
        cv2.putText(image, temperature_text, (text_margin_x, text_margin_y + line_spacing), font, font_scale, text_color, font_thickness)
        cv2.putText(image, height_text, (text_margin_x, text_margin_y + line_spacing * 2), font, font_scale, text_color, font_thickness)

        video_writer.write(image)

    # Release the video writer object
    video_writer.release()

    # Confirm the save location
    if os.path.exists(video_filename):
        print(f"Video successfully saved at: {video_filename}")
    else:
        print("Error: Video file was not saved.")


# Main section
time_temp_csv = Path(r'C:\AlliedVision\Python_Files\Chirag_Files\Experiments_Oct\Schaumglass_29.10_3(Expo_4_Apt_5.6)_Treated\roi_image_temperature_data.csv')  # First CSV for time and temperature
height_csv = Path(r'D:\chirag\29.10\height.csv')  # Second CSV for height
image_folder = Path(r'C:\AlliedVision\Python_Files\Chirag_Files\Experiments_Oct\Schaumglass_29.10_3(Expo_4_Apt_5.6)_Treated')  # Folder containing images
video_filename = video_filepath / "Video_Final_Height1.mp4"  # Name of the output video file
fps = 15  # Frames per second for the video

time_data, temperature_data = read_time_temp_data(time_temp_csv)
image_names, height_data = read_height_data(height_csv)

if time_data and temperature_data and height_data:
    create_video(image_folder, time_data, temperature_data, height_data, video_filename, fps)
else:
    print("Error: Failed to read CSV data.")