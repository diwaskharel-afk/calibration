import numpy as np
import cv2

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
# Compute homography from image -> robot plane
H, mask = cv2.findHomography(img_pts, robot_pts, method=0)

print("Homography matrix H:")
print(H)
def pixel_to_robot(u, v, H):
    # Input: u, v as floats, H as 3x3 homography
    p = np.array([u, v, 1.0], dtype=np.float32).reshape(3, 1)
    pr = H @ p
    pr = pr / pr[2, 0]  # divide by last coordinate to normalize
    X = pr[0, 0]
    Y = pr[1, 0]
    return X, Y

# Test with one of the calibration points
X_pred, Y_pred = pixel_to_robot(894,453 , H)
print("Predicted:", X_pred, Y_pred, "Actual:", 325,-6)