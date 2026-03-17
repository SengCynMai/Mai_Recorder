import cv2 as cv

# 1. Open the default camera
cap = cv.VideoCapture(0)

# 2. Check if camera opened successfully
if not cap.isOpened():
    print("Cannot open camera")
    exit()

# 3. Get frame width and height from the camera
width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

# 4. Set video recording options
fps = 20.0
fourcc = cv.VideoWriter_fourcc(*'mp4v')
output_file = 'output.mp4'

# 5. Create video writer
writer = cv.VideoWriter(output_file, fourcc, fps, (width, height))

# 6. Start in preview mode
recording = False
flip_mode = False #flip mode
gray_mode = False #gray

screenshot_count = 0

print("Press SPACE to start/stop recording.")
print("Press F to flip camera")
print("Press G to grayscale filter")
print("Press S to capture screenshot")
print("Press ESC to quit.")

while True:
    # 7. Read one frame from camera
    ret, frame = cap.read()

    if not ret:
        print("Cannot receive frame")
        break
    
    if flip_mode:
        frame = cv.flip(frame, 1)
        
    if gray_mode:
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        frame = cv.cvtColor(gray, cv.COLOR_GRAY2BGR)

    # 8. If recording mode, draw red circle and REC text
    if recording:
        cv.circle(frame, (30, 30), 10, (0, 0, 255), -1)
        cv.putText(frame, "REC", (50, 35), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        # 9. Save frame to video file
        writer.write(frame)
    else:
        cv.putText(frame, "PREVIEW", (20, 35), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # 10. Show the frame
    cv.imshow("Video Recorder", frame)

    # 11. Read keyboard input
    key = cv.waitKey(1)

    # 12. ESC key to quit
    if key == 27:
        break

    # 13. SPACE key to toggle preview/record mode
    elif key == ord(' '):
        recording = not recording
    
    elif key == ord('f'):
        flip_mode = not flip_mode
    
    elif key == ord('g'):
        gray_mode = not gray_mode

    elif key == ord('s'):
        filename = f"screenshot_{screenshot_count}.png"
        cv.imwrite(filename, frame)
        print(f"Saved {filename}")
        screenshot_count += 1
    

# 14. Release resources
cap.release()
writer.release()
cv.destroyAllWindows()