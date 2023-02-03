import cv2
import matplotlib.pyplot as plt
import numpy as np

def canny(image):                                   # Defining Canny Edge Detection
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)  # Grayscale conversion
    blur = cv2.GaussianBlur(gray, (5,5), 0)         # Gaussian Blur
    canny = cv2.Canny(blur, 200, 300)               # Canny Edge Detection
    return canny

def display_lines(image, lines):                    # Function to display lines
    line_image = np.zeros_like(image)               # Copying same image with all zeroes/Black
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)        # Extracting points for each line
            cv2.line(line_image, (x1,y1), (x2,y2), (0, 255, 0), 10) # joining points with color and thickness
    return line_image

def region_of_interest(image):                      # Function for ROI
    height = image.shape[0]                         # Extracting image height
    polygons = np.array([
        [(0,height-300),(4000,height-300),(2100,1550)]
        ])                                          # Marking the polygon with height starting from top
    mask = np.zeros_like(image)                     # Copying same image with all zeroes/Black
    cv2.fillPoly(mask,polygons,255)                 # Filling the polygon mask with 255's(11111111)/White
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image
    
image = cv2.imread("sample lane image.jpg")
lane_image = np.copy(image)
canny = canny(lane_image)
cropped_image = region_of_interest(canny)
lines = cv2.HoughLinesP(cropped_image,2,np.pi/180,150,np.array([]),minLineLength=10,maxLineGap=20) # Finding imp lines
line_image = display_lines(lane_image,lines)        # Display on the image
combo_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 1) # Adding weight to the lines on the img
plt.imshow(combo_image)
plt.show()