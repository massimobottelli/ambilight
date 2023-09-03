from colorthief import ColorThief
from PIL import Image
import tempfile
import cv2
import numpy as np


def get_color(current_frame):

    # Convert the BGR format to RGB
    frame_rgb = cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB)
    webcam_image = Image.fromarray(frame_rgb)

    # Resize the image for faster processing
    resized_image = resize_image(webcam_image, 640)

    # Save the resized image as a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_image:
        resized_image.save(temp_image, format="JPEG")

    # Extract palette from image using ColorThief
    ct = ColorThief(temp_image.name)
    dominant_color = ct.get_color()

    return dominant_color


def resize_image(webcam_image, new_width):

    # Resize the image while maintaining the aspect ratio
    aspect_ratio = webcam_image.width / webcam_image.height
    new_height = int(new_width / aspect_ratio)
    resized_image = webcam_image.resize((new_width, new_height), Image.NEAREST)
    return resized_image


# Main loop

# Create a VideoCapture object
cap = cv2.VideoCapture(0)

while True:

    # Capture a frame from the webcam
    ret, frame = cap.read()

    # Extract color palette
    dominant = get_color(frame)

    # Resize the frame
    frame = cv2.resize(frame, (640, int(frame.shape[0] * (640 / frame.shape[1]))))

    # Create a black background frame larger than the webcam frame
    height, width, _ = frame.shape
    border_width = 100
    background = np.zeros((height + 2 * border_width, width + 2 * border_width, 3), dtype=np.uint8)

    # Draw rectangles to create the border with palette color
    background_dominant = (dominant[2], dominant[1], dominant[0])
    background[:border_width, :] = background_dominant  # Top border
    background[-border_width:, :] = background_dominant  # Bottom border
    background[:, :border_width] = background_dominant  # Left border
    background[:, -border_width:] = background_dominant  # Right border

    # Place the resized webcam frame in the center of the background
    x_offset = border_width
    y_offset = border_width
    background[y_offset:y_offset + height, x_offset:x_offset + width] = frame

    # Display the frame with the border
    cv2.imshow("Webcam", background)

    # Check for the 'q' key to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture and close the window
cap.release()
cv2.destroyAllWindows()
