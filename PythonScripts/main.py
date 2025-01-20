import numpy as np
import argparse
from scipy.ndimage import binary_fill_holes
from PIL import Image
import cv2
import os


# Trần Văn Hải - 2151163686
# -------------------------------
# Thresholding
def apply_thresholding(image):
    # Chuyển ảnh RGB sang Grayscale
    gray = rgb_to_grayscale(image)

    # Tìm ngưỡng tốt nhất sử dụng tiêu chí Otsu
    best_thresh = find_best_threshold(gray)

    # Áp dụng ngưỡng để tạo mask
    mask = np.zeros_like(gray)
    mask[gray >= best_thresh] = 255  # Các pixel lớn hơn ngưỡng giữ lại
    return mask

def threshold_image(im, th):
    # Áp dụng ngưỡng để tạo mask
    thresholded_im = np.zeros(im.shape, dtype=np.uint8)
    thresholded_im[im >= th] = 1
    return thresholded_im

def compute_otsu_criteria(im, th):
    # Phân loại ảnh theo ngưỡng th
    thresholded_im = threshold_image(im, th)
    nb_pixels = im.size

    # Đếm số pixel thuộc hai lớp
    nb_pixels1 = np.count_nonzero(thresholded_im)
    weight1 = nb_pixels1 / nb_pixels
    weight0 = 1 - weight1

    # Nếu một lớp không tồn tại, trả về vô cực
    if weight1 == 0 or weight0 == 0:
        return np.inf

    # Tính phương sai của mỗi lớp
    val_pixels1 = im[thresholded_im == 1]
    val_pixels0 = im[thresholded_im == 0]
    var0 = np.var(val_pixels0) if len(val_pixels0) > 0 else 0
    var1 = np.var(val_pixels1) if len(val_pixels1) > 0 else 0

    # Tiêu chí Otsu
    return weight0 * var0 + weight1 * var1

def find_best_threshold(im):
    # Tìm ngưỡng tốt nhất trong phạm vi giá trị pixel
    threshold_range = range(np.max(im) + 1)
    criterias = [compute_otsu_criteria(im, th) for th in threshold_range]
    best_threshold = threshold_range[np.argmin(criterias)]
    return best_threshold

# Tạo video đầu ra và thêm nền
def remove_background_and_add_background(video_path, background_path, output_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter("temp_video.mp4", fourcc, fps, (width, height), isColor=True)

    background = cv2.imread(background_path)
    background = cv2.resize(background, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        mask = apply_thresholding(frame)
        # Create transparent output
        rgba_frame = create_transparent_output(frame, mask)

        # Convert RGBA frame to BGR for blending
        bgr_frame = cv2.cvtColor(rgba_frame, cv2.COLOR_RGBA2BGR)

        # Create a mask for the foreground
        foreground_mask = rgba_frame[:, :, 3] / 255.0  # Normalize alpha channel (range 0 to 1)
        foreground_mask_3ch = np.stack((foreground_mask,) * 3, axis=-1)

        # Composite the frame onto the background
        composite_frame = (bgr_frame * foreground_mask_3ch + background * (1 - foreground_mask_3ch)).astype(np.uint8)


        out.write(composite_frame.astype(np.uint8))

    cap.release()
    out.release()

    os.system(f"ffmpeg -i temp_video.mp4 -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p {output_path}")
    os.remove("temp_video.mp4")
    print(f"Video with removed background and new background saved at {output_path}")

# -------------------------------


# Bùi Tuấn Tú - 2151163736
# -------------------------------
# 3. Phát hiện biên
def apply_edge_detection(image):
    gray = rgb_to_grayscale(image)
    gx = sobel_filter(gray, axis=0)
    gy = sobel_filter(gray, axis=1)
    gradient_magnitude = np.sqrt(gx**2 + gy**2)
    edge_mask = (gradient_magnitude > 100).astype(np.uint8) * 255
    return edge_mask

# Chuyển đổi RGB sang grayscale
def rgb_to_grayscale(image):
    return (0.299 * image[:, :, 0] + 0.587 * image[:, :, 1] + 0.114 * image[:, :, 2]).astype(np.uint8)

# Chuyển đổi RGB sang HSV
def rgb_to_hsv(image):
    # Chuẩn hóa ảnh RGB về khoảng [0, 1]
    image = image / 255.0
    r, g, b = image[:, :, 0], image[:, :, 1], image[:, :, 2]

    # Tính Hue (H) theo công thức
    numerator = np.sqrt(3) * (g - b)
    denominator = 2 * r - g - b
    hue = np.arctan2(numerator, denominator)  # Tính arctan với 2 tham số để xác định góc chính xác
    hue = np.degrees(hue)  # Chuyển đổi từ radian sang độ
    hue[hue < 0] += 360  # Đảm bảo Hue nằm trong khoảng [0, 360]

    # Tính Saturation (S)
    sum_rgb = r + g + b
    min_rgb = np.minimum(np.minimum(r, g), b)
    saturation = np.where(sum_rgb == 0, 0, 1 - (3 * np.divide(min_rgb, sum_rgb, out=np.zeros_like(sum_rgb), where=sum_rgb != 0)))

    # Tính Value (V)
    value = np.maximum(np.maximum(r, g), b)

    # Kết hợp H, S, V thành một mảng
    hsv_image = np.stack([hue / 360, saturation, value], axis=-1)  # Chia H cho 360 để chuẩn hóa về [0, 1]

    return hsv_image

# Bộ lọc Sobel
def sobel_filter(image, axis):
    if axis == 0:
        kernel = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    elif axis == 1:
        kernel = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    else:
        raise ValueError("Invalid axis for Sobel filter")

    padded_image = np.pad(image, ((1, 1), (1, 1)), mode="edge")
    result = np.zeros_like(image, dtype=np.float32)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            region = padded_image[i : i + 3, j : j + 3]
            result[i, j] = np.sum(region * kernel)
    return result

# Tạo ảnh đầu ra với nền trong suốt
def create_transparent_output(image, edge_mask):
    # Tạo mặt nạ vùng bên trong biên
    inside_mask = create_inside_mask(edge_mask)

    # Tạo mặt nạ bên ngoài (lật lại inside_mask)
    outside_mask = np.logical_not(inside_mask > 0).astype(np.uint8) * 255

    # Tách các kênh màu RGB
    r, g, b = image[:, :, 0], image[:, :, 1], image[:, :, 2]

    # Tạo kênh alpha: Vùng bên trong biên giữ nguyên (255), bên ngoài làm trong suốt (0)
    alpha = np.where(outside_mask == 255, 0, 255).astype(np.uint8)

    # Kết hợp các kênh RGB và alpha thành ảnh RGBA
    rgba_image = np.stack([r, g, b, alpha], axis=-1)
    return rgba_image

# def create_inside_mask(edge_mask):
#     filled = edge_mask.copy()
#     h, w = edge_mask.shape
#     for i in range(h):
#         for j in range(w):
#             if i == 0 or j == 0 or i == h - 1 or j == w - 1:
#                 if edge_mask[i, j] == 0:
#                     flood_fill(filled, i, j)
#     return np.logical_not(filled).astype(np.uint8) * 255

def create_inside_mask(edge_mask):
    # Điền vào các vùng bên trong đường biên
    inside_mask = binary_fill_holes(edge_mask > 0).astype(np.uint8) * 255
    return inside_mask

def flood_fill(image, i, j):
    h, w = image.shape
    stack = [(i, j)]
    while stack:
        x, y = stack.pop()
        if 0 <= x < h and 0 <= y < w and image[x, y] == 0:
            image[x, y] = 255
            stack.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])

# -------------------------------

# Nguyễn Trung Hiếu - Nguyễn Trung Hiếu
# -------------------------------
# 2. Không gian màu
def apply_color_space(image):
    hsv = rgb_to_hsv(image)
    lower_bound = np.array([0, 30, 30]) / 255  # Normalize to [0, 1]
    upper_bound = np.array([1, 1, 1])
    mask = np.logical_and(hsv >= lower_bound, hsv <= upper_bound).all(axis=-1)
    return (mask * 255).astype(np.uint8)

# 4. Kết hợp cả 3
def combine_methods(image):
    mask1 = apply_thresholding(image)
    mask2 = apply_color_space(image)
    mask3 = apply_edge_detection(image)
    combined_mask = np.logical_and(np.logical_or(mask1, mask2), mask3)
    return (combined_mask * 255).astype(np.uint8)

# Thêm nền vào ảnh đã tách nền
def add_background(foreground_path, background_path, output_path):
    # Đọc ảnh foreground (ảnh đã tách nền)
    foreground = Image.open(foreground_path).convert("RGBA")

    # Đọc ảnh nền
    background = Image.open(background_path).convert("RGBA")
    background = background.resize(foreground.size)

    # Lấy kênh alpha của foreground
    alpha = foreground.split()[-1]

    # Kết hợp ảnh foreground và background dựa trên alpha
    combined = Image.composite(foreground, background, alpha)

    # Lưu kết quả
    combined.save(output_path, "PNG")
# -------------------------------

def main():
    parser = argparse.ArgumentParser(description="Image Background Removal")
    parser.add_argument(
        "-m", "--method", type=int, required=True,
        help="Method: 1 = Thresholding, 2 = Color Space, 3 = Edge Detection, 4 = Combine All, 5 = Add Background (Image), 6 = Remove Background and Add Background (Video)"
    )
    parser.add_argument("-i", "--input", type=str, required=True, help="Input image/video path")
    parser.add_argument("-o", "--output", type=str, required=True, help="Output image/video path")
    parser.add_argument(
        "-b", "--background", type=str, required=False,
        help="Background image path (required for method 5 and 6)"
    )
    args = parser.parse_args()

    # Kiểm tra phần mở rộng file để xử lý
    file_extension = args.input.split('.')[-1].lower()

    if file_extension in ["jpg", "jpeg", "png", "bmp"]:
        # Xử lý ảnh
        image = np.array(Image.open(args.input).convert("RGB"))
        
        if args.method == 1:
            mask = apply_thresholding(image)
        elif args.method == 2:
            mask = apply_color_space(image)
        elif args.method == 3:
            mask = apply_edge_detection(image)
            np.savetxt('mask.txt', mask, fmt='%d', delimiter=' ')
            print("Mask has been saved as 'mask.txt'")
        elif args.method == 4:
            mask = combine_methods(image)
        elif args.method == 5:
            if not args.background:
                print("Error: Background image path is required for method 5.")
                return
            add_background(args.input, args.background, args.output)
            return
        else:
            print("Error: Invalid method selected!")
            return

        # Tạo ảnh đầu ra với nền trong suốt
        transparent_output = create_transparent_output(image, mask)
        output_image = Image.fromarray(transparent_output.astype(np.uint8))
        output_image.save(args.output, "PNG")

    elif file_extension in ["mp4", "avi", "mov", "mkv"]:
        # Xử lý video
        if args.method == 6:
            if not args.background:
                print("Error: Background image path is required for method 6.")
                return
            remove_background_and_add_background(args.input, args.background, args.output)
        else:
            print("Error: Invalid method selected for video processing!")
    else:
        print("Error: Unsupported file type!")

if __name__ == "__main__":
    main()


# Sử dụng: python main.py -m <method> -i <input_path> -o <output_path> -b <background_path>
