using System;
using System.Diagnostics;
using System.Drawing;
using System.Windows.Forms;

namespace RemoveBackgroundImage
{
    public partial class RemoveBackgroundImage : Form
    {
        private Bitmap originalImage; 
        private Bitmap processedImage; 

        public RemoveBackgroundImage()
        {
            InitializeComponent();

            // Thêm các phương pháp vào ComboBox
            comboRemoveBackground.Items.Add("Thresholding");
            comboRemoveBackground.Items.Add("Không gian màu");
            comboRemoveBackground.Items.Add("Phát hiện biên");
            comboRemoveBackground.Items.Add("Kết hợp");
            comboRemoveBackground.SelectedIndex = -1;
            comboRemoveBackground.Enabled = false;
            comboRemoveBackground.SelectedIndexChanged += ComboRemoveBackground_SelectedIndexChanged; // Gắn sự kiện
        }

        private void btnLoadImage_Click(object sender, EventArgs e)
        {
            using (OpenFileDialog ofd = new OpenFileDialog())
            {
                ofd.Filter = "Image Files|*.jpg;*.png;*.bmp";
                if (ofd.ShowDialog() == DialogResult.OK)
                {
                    if (processedImage != null)
                    {
                        processedImage.Dispose();
                        processedImage = null;
                        pictureBoxProcessed.Image = null;
                    }
                    originalImage = new Bitmap(ofd.FileName);
                    pictureBoxOriginal.Image = originalImage;
                    comboRemoveBackground.Enabled = true;
                    comboRemoveBackground.SelectedIndex = -1;
                }
            }
        }
        private void ComboRemoveBackground_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (originalImage == null)
            {
                MessageBox.Show("Hãy tải ảnh trước!", "Thông báo", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            if (comboRemoveBackground.SelectedIndex == -1) return;

            // Lấy phương pháp xử lý từ ComboBox
            int methodParam = comboRemoveBackground.SelectedIndex + 1; // Index 0-3 -> method 1-4

            // Lưu ảnh gốc tạm thời để xử lý bằng Python
            string inputPath = "temp_input.png";
            string outputPath = "temp_output.png";

            try
            {
                // Giải phóng file output nếu đang bị khóa
                if (processedImage != null)
                {
                    processedImage.Dispose();
                    processedImage = null;
                }

                // Lưu ảnh gốc tạm thời
                originalImage.Save(inputPath);

                // Gọi script Python
                string pythonPath = "python"; // Đảm bảo rằng Python đã được thêm vào PATH
                string scriptPath = "main.py"; // Đường dẫn tới file Python

                string arguments = $"-m {methodParam} -i \"{inputPath}\" -o \"{outputPath}\"";

                Process process = new Process();
                process.StartInfo.FileName = pythonPath;
                process.StartInfo.Arguments = $"{scriptPath} {arguments}";
                process.StartInfo.RedirectStandardOutput = true;
                process.StartInfo.RedirectStandardError = true;
                process.StartInfo.UseShellExecute = false;
                process.StartInfo.CreateNoWindow = true;

                process.Start();
                string output = process.StandardOutput.ReadToEnd();
                string error = process.StandardError.ReadToEnd();
                process.WaitForExit();

                if (!string.IsNullOrEmpty(error))
                {
                    MessageBox.Show($"Lỗi trong quá trình xử lý:\n{error}", "Lỗi", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }

                // Cập nhật ảnh đã xử lý
                processedImage = new Bitmap(outputPath);
                pictureBoxProcessed.Image = processedImage;
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Lỗi khi chạy script Python: {ex.Message}", "Lỗi", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void btnSave_Click(object sender, EventArgs e)
        {
            if (processedImage == null)
            {
                MessageBox.Show("Hãy xử lý ảnh trước khi lưu!", "Thông báo", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            using (SaveFileDialog sfd = new SaveFileDialog())
            {
                sfd.Filter = "Image Files|*.jpg;*.png;*.bmp";
                if (sfd.ShowDialog() == DialogResult.OK)
                {
                    processedImage.Save(sfd.FileName);
                    MessageBox.Show("Lưu ảnh thành công!", "Thông báo", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
            }
        }

        private void pictureBoxProcessed_Paint(object sender, PaintEventArgs e)
        {
            if (processedImage == null) return;

            // Vẽ nền checkerboard (ô vuông)
            int cellSize = 10; // Kích thước mỗi ô
            for (int y = 0; y < pictureBoxProcessed.Height; y += cellSize)
            {
                for (int x = 0; x < pictureBoxProcessed.Width; x += cellSize)
                {
                    Color color = ((x / cellSize + y / cellSize) % 2 == 0) ? Color.LightGray : Color.White;
                    using (Brush brush = new SolidBrush(color))
                    {
                        e.Graphics.FillRectangle(brush, x, y, cellSize, cellSize);
                    }
                }
            }

            // Vẽ ảnh đã xử lý lên trên nền checkerboard, giữ tỷ lệ gốc
            if (processedImage != null)
            {
                // Tính toán kích thước và vị trí ảnh để giữ tỷ lệ
                Rectangle destRect = GetImageBounds(pictureBoxProcessed.ClientRectangle, processedImage.Width, processedImage.Height);
                e.Graphics.DrawImage(processedImage, destRect);
            }
        }

        private Rectangle GetImageBounds(Rectangle containerRect, int imageWidth, int imageHeight)
        {
            float containerAspect = (float)containerRect.Width / containerRect.Height;
            float imageAspect = (float)imageWidth / imageHeight;

            int drawWidth, drawHeight;
            if (imageAspect > containerAspect)
            {
                // Ảnh rộng hơn khung chứa
                drawWidth = containerRect.Width;
                drawHeight = (int)(containerRect.Width / imageAspect);
            }
            else
            {
                // Ảnh cao hơn khung chứa
                drawHeight = containerRect.Height;
                drawWidth = (int)(containerRect.Height * imageAspect);
            }

            int x = (containerRect.Width - drawWidth) / 2;
            int y = (containerRect.Height - drawHeight) / 2;
            return new Rectangle(x, y, drawWidth, drawHeight);
        }

    }
}