import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw

cap = cv2.VideoCapture("test6.mp4",0)
CHAR_LIST = "#B8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
bg_code = 0
font = ImageFont.truetype("DejaVuSansMono-Bold.ttf", size=int(10 * 1))
num_chars = len(CHAR_LIST)
num_cols = 100

#urmm nhìn chuyên nghiệp nên để vào
def canny(img):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    kernel = 5
    blur = cv2.GaussianBlur(gray, (kernel, kernel), 0)
    canny = cv2.Canny(blur, 50, 150)
    return canny

def main(image, num_cols):
    height, width, _ = image.shape
    cell_width = width / num_cols
    cell_height = 2 * cell_width
    num_rows = int(height / cell_height)
    if num_cols > width or num_rows > height:
        print("Too many columns or rows. Use default setting")
        cell_width = 3
        cell_height = 6
        num_cols = int(width / cell_width)
        num_rows = int(height / cell_height)
    char_width, char_height = 6,12
    out_width = char_width * num_cols
    out_height = 2 * char_height * num_rows
    out_image = Image.new("L", (out_width, out_height), bg_code)
    draw = ImageDraw.Draw(out_image)
    for i in range(num_rows):
        line = "".join([CHAR_LIST[min(int(np.mean(image[int(i * cell_height):min(int((i + 1) * cell_height), height),
                int(j * cell_width):min(int((j + 1) * cell_width),
                width)]) * num_chars / 255), num_chars - 1)]
                for j in range(num_cols)]) + "\n"
        draw.text((0, i * char_height), line, fill=255 - bg_code, font=font)
    cropped_image = out_image.getbbox()
    out_image = out_image.crop(cropped_image)
    out_image = cv2.cvtColor(np.array(out_image), cv2.COLOR_GRAY2BGR)
    out_image = np.array(out_image)
    return out_image

while (cap.isOpened()):
    _, frame = cap.read()
    lane_image = np.copy(cap)
    resize = cv2.resize(frame, (400, 300))
    ascii = main(resize,100)
    canny_image = canny(resize)
    cv2.imshow("result1", ascii)
    cv2.imshow("result", resize)
    cv2.imshow("result2",canny_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()