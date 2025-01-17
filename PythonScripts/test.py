import numpy as np
import cv2
import argparse

def threshold_image(im, th):
    thresholded_im = np.zeros(im.shape)
    thresholded_im[im >= th] = 1
    return thresholded_im

def compute_otsu_criteria(im, th):
    thresholded_im = threshold_image(im, th)
    nb_pixels = im.size
    nb_pixels1 = np.count_nonzero(thresholded_im)
    weight1 = nb_pixels1 / nb_pixels
    weight0 = 1 - weight1
    if weight1 == 0 or weight0 == 0:
        return np.inf
    val_pixels1 = im[thresholded_im == 1]
    val_pixels0 = im[thresholded_im == 0]
    var0 = np.var(val_pixels0) if len(val_pixels0) > 0 else 0
    var1 = np.var(val_pixels1) if len(val_pixels1) > 0 else 0
    return weight0 * var0 + weight1 * var1

def find_best_threshold(im):
    threshold_range = range(np.max(im) + 1)
    criterias = [compute_otsu_criteria(im, th) for th in threshold_range]
    best_threshold = threshold_range[np.argmin(criterias)]
    return best_threshold

def main():
    parser = argparse.ArgumentParser(description="Image Background Removal")
    parser.add_argument("-m", "--method", type=int, required=True,
                        help="Method: 1 = Thresholding, 2 = Color Space, 3 = Edge Detection, 4 = Combine All")
    parser.add_argument("-i", "--input", type=str, required=True, help="Input image path")
    parser.add_argument("-o", "--output", type=str, required=True, help="Output image path")
    parser.add_argument("--low_hue", type=int, default=30, help="Lower bound for hue (method 2 and 4)")
    parser.add_argument("--high_hue", type=int, default=90, help="Upper bound for hue (method 2 and 4)")
    args = parser.parse_args()

    if args.method == 1:  # Thresholding method
        # 1. Đọc ảnh màu đầu vào
        img_color = cv2.imread(args.input)
        img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

        # 2. Tạo mask từ ảnh grayscale
        best_thresh = find_best_threshold(img_gray)
        thresholded_img = threshold_image(img_gray, best_thresh)
        thresholded_img = (thresholded_img * 255).astype(np.uint8)

        # **Đảo ngược mask nếu cần thiết (tùy thuộc vào ảnh đầu vào)**
        # Nếu nền sáng hơn vật thể, hãy bỏ comment dòng dưới
        # thresholded_img = cv2.bitwise_not(thresholded_img)

        # 3. Sử dụng mask để trích xuất chủ thể từ ảnh màu gốc
        foreground = cv2.bitwise_and(img_color, img_color, mask=thresholded_img)

        # 4. Tạo ảnh nền trong suốt
        background = np.zeros((img_color.shape[0], img_color.shape[1], 4), dtype=np.uint8)

        # 5. Kết hợp chủ thể và nền trong suốt
        # Tạo ảnh 4 kênh từ ảnh 3 kênh
        img_color_bgra = cv2.cvtColor(img_color, cv2.COLOR_BGR2BGRA)

        # Áp dụng mask cho kênh alpha của ảnh màu gốc
        img_color_bgra[:, :, 3] = thresholded_img

        # Kết hợp ảnh màu gốc (có mask alpha) với nền trong suốt
        result_image = cv2.add(img_color_bgra, background)
        # Hoặc có thể bỏ qua bước add vì img_color_bgra đã có nền trong suốt
        # result_image = img_color_bgra

        # Lưu ảnh đã xóa phông (định dạng .png để hỗ trợ trong suốt)
        cv2.imwrite(args.output, result_image)
        print(f"Image saved to {args.output}")
    else:
        print("This code only implements Thresholding (method 1).")

if __name__ == "__main__":
    main()