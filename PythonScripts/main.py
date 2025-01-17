import numpy as np
import argparse
import imageio.v2 as imageio
from scipy.ndimage import binary_fill_holes


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


# 2. Không gian màu
def apply_color_space(image):
    hsv = rgb_to_hsv(image)
    lower_bound = np.array([0, 30, 30]) / 255  # Normalize to [0, 1]
    upper_bound = np.array([1, 1, 1])
    mask = np.logical_and(hsv >= lower_bound, hsv <= upper_bound).all(axis=-1)
    return (mask * 255).astype(np.uint8)


# 3. Phát hiện biên
def apply_edge_detection(image):
    gray = rgb_to_grayscale(image)
    gx = sobel_filter(gray, axis=0)
    gy = sobel_filter(gray, axis=1)
    gradient_magnitude = np.sqrt(gx**2 + gy**2)
    edge_mask = (gradient_magnitude > 100).astype(np.uint8) * 255
    return edge_mask


# 4. Kết hợp cả 3
def combine_methods(image):
    mask1 = apply_thresholding(image)
    mask2 = apply_color_space(image)
    mask3 = apply_edge_detection(image)
    combined_mask = np.logical_and(np.logical_or(mask1, mask2), mask3)
    return (combined_mask * 255).astype(np.uint8)


# Chuyển đổi RGB sang grayscale
def rgb_to_grayscale(image):
    return (0.2989 * image[:, :, 0] + 0.5870 * image[:, :, 1] + 0.1140 * image[:, :, 2]).astype(np.uint8)


# Chuyển đổi RGB sang HSV
def rgb_to_hsv(image):
    image = image / 255.0
    max_val = image.max(axis=-1)
    min_val = image.min(axis=-1)
    delta = max_val - min_val

    hue = np.zeros_like(max_val)
    mask = delta > 0
    r, g, b = image[:, :, 0], image[:, :, 1], image[:, :, 2]
    hue[mask & (max_val == r)] = (60 * (g[mask & (max_val == r)] - b[mask & (max_val == r)]) / delta[mask & (max_val == r)] + 360) % 360
    hue[mask & (max_val == g)] = (60 * (b[mask & (max_val == g)] - r[mask & (max_val == g)]) / delta[mask & (max_val == g)] + 120) % 360
    hue[mask & (max_val == b)] = (60 * (r[mask & (max_val == b)] - g[mask & (max_val == b)]) / delta[mask & (max_val == b)] + 240) % 360

    saturation = np.where(max_val == 0, 0, np.divide(delta, max_val, out=np.zeros_like(delta), where=max_val != 0))
    value = max_val

    return np.stack([hue / 360, saturation, value], axis=-1)


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


def create_inside_mask(edge_mask):
    # Điền vào các vùng bên trong đường biên
    inside_mask = binary_fill_holes(edge_mask > 0).astype(np.uint8) * 255
    return inside_mask


def main():
    # Thiết lập argparse
    parser = argparse.ArgumentParser(description="Image Background Removal")
    parser.add_argument(
        "-m",
        "--method",
        type=int,
        required=True,
        help="Method: 1 = Thresholding, 2 = Color Space, 3 = Edge Detection, 4 = Combine All",
    )
    parser.add_argument("-i", "--input", type=str, required=True, help="Input image path")
    parser.add_argument("-o", "--output", type=str, required=True, help="Output image path")
    args = parser.parse_args()

    # Đọc ảnh đầu vào
    image = imageio.imread(args.input).astype(np.float32)

    # Áp dụng phương pháp xử lý
    if args.method == 1:
        mask = apply_thresholding(image)
    elif args.method == 2:
        mask = apply_color_space(image)
    elif args.method == 3:
        mask = apply_edge_detection(image)
    elif args.method == 4:
        mask = combine_methods(image)
    else:
        print("Error: Invalid method selected!")
        return

    # Tạo ảnh đầu ra với nền trong suốt
    transparent_output = create_transparent_output(image, mask)

    # Lưu ảnh RGBA (PNG hỗ trợ alpha)
    output_format = args.output.split(".")[-1].lower()
    if output_format == "png":
        imageio.imwrite(args.output, transparent_output.astype(np.uint8))
    else:
        print("Error: Only PNG format supports RGBA. Please use a .png output file.")
        return

    print(f"Transparent output saved at {args.output}")


if __name__ == "__main__":
    main()
