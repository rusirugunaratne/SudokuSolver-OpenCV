import cv2
import numpy as np


def predict_numbers(boxes, model):
    numbers = []
    for box in boxes:
        # Preprocess the box image for YOLO
        box_img = cv2.resize(box, (640, 640))  # Adjust size if needed
        results = model(box_img)  # Run YOLO detection

        # Extract the predicted number
        if results.xyxy[0].shape[0] > 0:  # Check if any detections
            number_confidence, number_class, _, _ = results.xyxy[0][0].tolist()
            number = int(number_class)  # Convert class ID to number
            numbers.append(number)
        else:
            numbers.append(0)  # No detection, append 0

    return numbers


def preProcess(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, 1, 1, 11, 2)
    return imgThreshold


def biggestContour(contours):
    biggest = np.array([])
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 50:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area
    return biggest, max_area


def reorder(points):
    points = points.reshape((4, 2))
    pointsNew = np.zeros((4, 1, 2), dtype=np.int32)
    add = points.sum(1)
    pointsNew[0] = points[np.argmin(add)]
    pointsNew[3] = points[np.argmax(add)]
    diff = np.diff(points, axis=1)
    pointsNew[1] = points[np.argmin(diff)]
    pointsNew[2] = points[np.argmax(diff)]
    return pointsNew


def splitBoxes(img, grid_size=9):
    rows = np.vsplit(img, grid_size)
    boxes = []
    for r in rows:
        cols = np.hsplit(r, grid_size)
        for box in cols:
            boxes.append(box)
    return boxes


def print_sudoku_board(sudoku_board, grid_size):
    # Determine the width of each cell based on the grid_size
    cell_width = 2 + int(grid_size ** 0.5)

    # Print the Sudoku board
    for i in range(grid_size):
        if i > 0 and i % int(grid_size ** 0.5) == 0:
            print("-" * (cell_width * grid_size + int(grid_size ** 0.5) - 1))

        for j in range(grid_size):
            if j > 0 and j % int(grid_size ** 0.5) == 0:
                print("|", end=" ")

            value = sudoku_board[i * grid_size + j]

        print()
