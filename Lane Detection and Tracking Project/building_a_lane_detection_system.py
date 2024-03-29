import cv2
import matplotlib.pyplot as plt
import numpy as np

def canny(image):                                   # Defining Canny Edge Detection
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)  # Grayscale conversion
    blur = cv2.GaussianBlur(gray, (5,5), 0)         # Gaussian Blur
    canny = cv2.Canny(blur, 50, 150)               # Canny Edge Detection
    return canny

def display_lines(image, lines):                    # Function to display lines
    line_image = np.zeros_like(image)               # Copying same image with all zeroes/Black
    if lines is not None:
        for x1, y1, x2, y2 in lines:
            cv2.line(line_image, (x1,y1), (x2,y2), (0, 255, 0), 10) # joining points with color and thickness
    return line_image

def region_of_interest(image):                      # Function for ROI
    height = image.shape[0]                         # Extracting image height
    polygons = np.array([
        [(200,height),(1100,height),(500,250)]
        ])                                          # Marking the polygon with height starting from top
    mask = np.zeros_like(image)                     # Copying same image with all zeroes/Black
    cv2.fillPoly(mask,polygons,255)                 # Filling the polygon mask with 255's(11111111)/White
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

def make_coordinates(image, line_parameters):
    try:
        slope, intercept = line_parameters
    except TypeError:
        slope, intercept = 0.001,0

    y1 = image.shape[0]
    y2 = int(y1*(3/7))
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    return np.array([x1,y1,x2,y2])

def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []
    for line in lines:
        x1,y1,x2,y2 = line.reshape(4)
        parameters = np.polyfit((x1,x2), (y1,y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope<0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))
    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)
    left_line = make_coordinates(image, left_fit_average)
    right_line = make_coordinates(image, right_fit_average)
    return np.array([left_line, right_line])
        
# image = cv2.imread("sample lane image.jpg")
# lane_image = np.copy(image)
# canny_image = canny(lane_image)
# cropped_image = region_of_interest(canny_image)
# lines = cv2.HoughLinesP(cropped_image,2,np.pi/180,150,np.array([]),minLineLength=10,maxLineGap=20) # Finding imp lines
# averaged_lines = average_slope_intercept(lane_image,lines)
# line_image = display_lines(lane_image,averaged_lines)        # Display on the image
# combo_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 1) # Adding weight to the lines on the img
# plt.imshow(combo_image)
# plt.show()

cap = cv2.VideoCapture("Lane Detection and Tracking Project/test2.mp4")
while(cap.isOpened()):
    _, frame = cap.read()
    canny_image = canny(frame)
    cropped_image = region_of_interest(canny_image)
    lines = cv2.HoughLinesP(cropped_image,2,np.pi/180,150,np.array([]),minLineLength=10,maxLineGap=20) # Finding imp lines
    averaged_lines = average_slope_intercept(frame,lines)
    line_image = display_lines(frame,averaged_lines)        # Display on the image
    combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1) # Adding weight to the lines on the img
    # plt.imshow(combo_image)
    # plt.show()
    cv2.imshow("result",combo_image)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()