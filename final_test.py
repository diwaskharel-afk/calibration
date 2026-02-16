import cv2
import numpy as np

# -----------------------------
# Load image
# -----------------------------
img = cv2.imread('images\wi.jpeg')
if img is None:
    print("Error: Image not found")
    exit()

# Make a copy for display
img_show = img.copy()

# -----------------------------
# Calibration points
# -----------------------------
img_pts = np.array([(894, 349), (895, 553), (1204, 758), (1303, 141), (481, 455), (272, 664)]
    , dtype=np.float32)


robot_pts = np.array([
    [350.02, -6.189],
    [301.56, -6.189],
    [251.34, -80.11],
    [398.58, -108.1],
    [323.20, 94.713],
    [273.73, 143.24]
], 
dtype=np.float32)

# -----------------------------
# Compute homography
# -----------------------------
H, mask = cv2.findHomography(img_pts, robot_pts)
print("Homography matrix H:")
print(H)

# -----------------------------
# Pixel → Robot conversion
# -----------------------------
def pixel_to_robot(u, v, H):
    p = np.array([u, v, 1.0], dtype=np.float32).reshape(3, 1)
    pr = H @ p
    pr = pr / pr[2, 0]  # normalize
    X = pr[0, 0]
    Y = pr[1, 0]
    return X, Y

points_img = []

# -----------------------------
# Mouse click function
# -----------------------------
def click_event(event, x, y, flags, param):
    global img_show

    if event == cv2.EVENT_LBUTTONDOWN:
        X_robot, Y_robot = pixel_to_robot(x, y, H)
        print("-------------------------------------------------")
        print(f"Original pixel: ({x}, {y})")
        print(f"Robot coordinates: ({X_robot:.2f}, {Y_robot:.2f})")

        points_img.append((x, y))

        # Draw point on img_show
        cv2.circle(img_show, (x, y), 6, (0, 0, 255), -1)

        # Write robot coordinates
        text = f"({x},{y})->({X_robot:.1f},{Y_robot:.1f})"
        cv2.putText(img_show,
                    text,
                    (x + 10, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 0, 0),
                    1,
                    cv2.LINE_AA)

# -----------------------------
# OpenCV window
# -----------------------------
cv2.namedWindow('calib')
cv2.setMouseCallback('calib', click_event)

while True:
    cv2.imshow('calib', img_show)
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC to quit
        break

# Save image with markings
cv2.imwrite("output_with_points.jpg", img_show)
print("Image saved as output_with_points.jpg")
cv2.destroyAllWindows()
print("Collected original points:", points_img)
