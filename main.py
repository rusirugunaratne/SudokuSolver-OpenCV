from app_utils import process_image

def main():
    path_image = "resources/16.png"
    height_img = 576
    width_img = 576
    board_size = 16

    result_board = process_image(path_image, height_img, width_img, board_size)
    print(result_board)

if __name__ == "__main__":
    main()
