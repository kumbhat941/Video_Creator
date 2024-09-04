#this program will require''''' directly the images and the excel file'''''
# the  setting is depending on the excel file data if there are 41 time stamps  and only 10 images then it will take only 10 time stamps and 10 images.
import pandas as pd
import cv2
import os

# Excel reader (limiting data to first 10 rows)
def read_data(Excel_file_path):
  try:
    df = pd.read_csv(Excel_file_path, header=0)
    time_data = df.iloc[0:, 0].tolist()
    temperature_data = df.iloc[0:, 1].tolist()
    return time_data, temperature_data
  except:
    print("File not found or reading failed.")
    return None, None

# Define video output path
video_output_path = r"C:\AlliedVision\Python_Files\Chirag_Files\Video_Output"

# Creating video
def create_video(image_folder, time_data, temperature_data, video_filename, fps):
  # Check if image folder exists
  if not os.path.exists(image_folder):
    print(f"Error: Image folder '{image_folder}' does not exist.")
    return

  # Get image paths with natural sorting
  image_paths = sorted(os.listdir(image_folder), key=lambda x: int(x.split(".")[0]))
  image_paths = [os.path.join(image_folder, f) for f in image_paths if f.endswith(('.tiff', '.png'))]

  # Validate image count (optional)
  if len(image_paths) > len(time_data) or len(image_paths) > len(temperature_data):
    print(f"Warning: Number of images ({len(image_paths)}) exceeds data length ({min(len(time_data), len(temperature_data))}). Using only first {min(len(time_data), len(temperature_data))} data points.")

  # Use minimum of image count and data length
  num_frames = min(len(image_paths), len(time_data), len(temperature_data))

  # Get first image dimensions for video size
  first_image = cv2.imread(image_paths[0])
  height, width, channels = first_image.shape

  # Create video writer
  fourcc = cv2.VideoWriter_fourcc(*'mp4v')
  video_filepath = os.path.join(video_output_path, video_filename)  # Combine video filename with path
  video_writer = cv2.VideoWriter(video_filepath, fourcc, fps, (width, height))

  # Font and text position parameters (adjust as needed)
  font = cv2.FONT_HERSHEY_SIMPLEX
  font_scale = 3
  font_thickness = 5
  text_color = (0, 255, 0)  # green text color (BGR format)
  text_margin_x = width - 800
  text_margin_y = 200

  # Iterate over images and create video frames (using num_frames)
  for i in range(num_frames):
    if image_paths is not None:  # Check if image_paths is not None before using it
      image_path = image_paths[i]
      print(image_path)  # Optional: Print image path for debugging

      image_number = image_path.split("\\")[-1].split(".")[0]  # Split by path separator and extension

      time_value = time_data[i]
      temperature_value = temperature_data[i]

      # Load the image
      image = cv2.imread(image_path)

      # Prepare text strings (adjust formatting as needed)
      time_text = f"Time: {time_value}"
      temperature_text = f"Temp: {temperature_value}"
      Image_text = f"Image_no: {image_number}"

      # Put time text on the image
      cv2.putText(image, time_text, (text_margin_x, text_margin_y), font, font_scale, text_color, font_thickness)

      # Put temperature text below time text (adjust vertical spacing as needed)
      cv2.putText(image, temperature_text, (text_margin_x, text_margin_y + font_scale * 30), font, font_scale, text_color, font_thickness)

      # Put file name on the image
      cv2.putText(image, Image_text, (text_margin_x, text_margin_y + font_scale * 60), font, font_scale, text_color, font_thickness)

      # Write the overlaid frame to the video
      video_writer.write(image)

  # Release video writer
  video_writer.release()
  print(f"Video created: {video_filename}")

# Main section (replace with your file paths,


# The main
# Replace with your actual file paths and video parameters
    
Excel_file_path = r'C:\AlliedVision\Python_Files\Chirag_Files\CSV_collection\20240523 Feinglas Anlage 2 + 2SiC.csv' #give the file path for the excel
image_folder = r'C:\AlliedVision\Python_Files\Chirag_Files\Image Output'
video_filename = "202405123 Feinanteil Anlage 2 + 2SiC.mp4v"
fps = 15 #this frame rate can be adjusted as per the requirement for studying
# Read data from Excel file (calling read_data function)
time_data, temperature_data = read_data(Excel_file_path)

# Create the video with time and temperature data overlaid (calling create_video function)
create_video(image_folder, time_data, temperature_data, video_filename, fps)
