import numpy as np
import easyocr

def digit_recognizer(boxes, board_size, margin=2):
    reader = easyocr.Reader(['en'])

    board = np.zeros((board_size, board_size), dtype=int)

    for i in range(board_size):
        for j in range(board_size):
            roi = boxes[i * board_size + j]

            # Crop a small margin from the borders of the box
            roi_height, roi_width = roi.shape[:2]
            roi = roi[margin:roi_height-margin, margin:roi_width-margin]

            # Use EasyOCR to recognize the digit
            result = reader.readtext(roi)

            # Extract recognized digit (assuming one digit per box)
            if result:
                digit = int(result[0][-2])
                board[i, j] = digit

    return board


