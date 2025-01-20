namespace RemoveBackgroundImage
{
    partial class RemoveBackgroundImage
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            pictureBoxOriginal = new PictureBox();
            pictureBoxProcessed = new PictureBox();
            label1 = new Label();
            label2 = new Label();
            btnLoadImage = new Button();
            btnSaveImage = new Button();
            btnChangeBackground = new Button();
            comboRemoveBackground = new ComboBox();
            btnBrowseInputVideo = new Button();
            btnBrowseBackgroundImage = new Button();
            btnBrowseOutputVideo = new Button();
            txtInputVideo = new TextBox();
            txtBackgroundImage = new TextBox();
            txtOutputVideo = new TextBox();
            btnRemove = new Button();
            txtStatus = new Label();
            ((System.ComponentModel.ISupportInitialize)pictureBoxOriginal).BeginInit();
            ((System.ComponentModel.ISupportInitialize)pictureBoxProcessed).BeginInit();
            SuspendLayout();
            // 
            // pictureBoxOriginal
            // 
            pictureBoxOriginal.BackColor = Color.Gainsboro;
            pictureBoxOriginal.BorderStyle = BorderStyle.FixedSingle;
            pictureBoxOriginal.Location = new Point(34, 21);
            pictureBoxOriginal.Name = "pictureBoxOriginal";
            pictureBoxOriginal.Size = new Size(330, 330);
            pictureBoxOriginal.SizeMode = PictureBoxSizeMode.Zoom;
            pictureBoxOriginal.TabIndex = 0;
            pictureBoxOriginal.TabStop = false;
            // 
            // pictureBoxProcessed
            // 
            pictureBoxProcessed.BackColor = Color.Gainsboro;
            pictureBoxProcessed.BorderStyle = BorderStyle.FixedSingle;
            pictureBoxProcessed.Location = new Point(408, 21);
            pictureBoxProcessed.Name = "pictureBoxProcessed";
            pictureBoxProcessed.Size = new Size(330, 330);
            pictureBoxProcessed.SizeMode = PictureBoxSizeMode.Zoom;
            pictureBoxProcessed.TabIndex = 0;
            pictureBoxProcessed.TabStop = false;
            pictureBoxProcessed.Paint += pictureBoxProcessed_Paint;
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Location = new Point(155, 363);
            label1.Name = "label1";
            label1.Size = new Size(79, 21);
            label1.TabIndex = 1;
            label1.Text = "Ảnh Gốc";
            // 
            // label2
            // 
            label2.AutoSize = true;
            label2.Location = new Point(515, 363);
            label2.Name = "label2";
            label2.Size = new Size(127, 21);
            label2.TabIndex = 1;
            label2.Text = "Ảnh Sau Xử Lý";
            // 
            // btnLoadImage
            // 
            btnLoadImage.Location = new Point(34, 402);
            btnLoadImage.Name = "btnLoadImage";
            btnLoadImage.Size = new Size(142, 29);
            btnLoadImage.TabIndex = 0;
            btnLoadImage.Text = "Tải Ảnh Lên";
            btnLoadImage.UseVisualStyleBackColor = true;
            btnLoadImage.Click += btnLoadImage_Click;
            // 
            // btnSaveImage
            // 
            btnSaveImage.Location = new Point(596, 402);
            btnSaveImage.Name = "btnSaveImage";
            btnSaveImage.Size = new Size(142, 29);
            btnSaveImage.TabIndex = 3;
            btnSaveImage.Text = "Lưu Ảnh";
            btnSaveImage.UseVisualStyleBackColor = true;
            btnSaveImage.Click += btnSave_Click;
            // 
            // btnChangeBackground
            // 
            btnChangeBackground.Location = new Point(408, 402);
            btnChangeBackground.Name = "btnChangeBackground";
            btnChangeBackground.Size = new Size(142, 29);
            btnChangeBackground.TabIndex = 2;
            btnChangeBackground.Text = "Thay Nền Ảnh";
            btnChangeBackground.UseVisualStyleBackColor = true;
            btnChangeBackground.Click += btnChangeBackground_Click;
            // 
            // comboRemoveBackground
            // 
            comboRemoveBackground.DropDownHeight = 126;
            comboRemoveBackground.DropDownStyle = ComboBoxStyle.DropDownList;
            comboRemoveBackground.Font = new Font("Times New Roman", 14.25F, FontStyle.Regular, GraphicsUnit.Point, 0);
            comboRemoveBackground.FormattingEnabled = true;
            comboRemoveBackground.IntegralHeight = false;
            comboRemoveBackground.Location = new Point(222, 402);
            comboRemoveBackground.Name = "comboRemoveBackground";
            comboRemoveBackground.Size = new Size(142, 29);
            comboRemoveBackground.TabIndex = 1;
            comboRemoveBackground.SelectedIndexChanged += ComboRemoveBackground_SelectedIndexChanged;
            // 
            // btnBrowseInputVideo
            // 
            btnBrowseInputVideo.Location = new Point(34, 453);
            btnBrowseInputVideo.Name = "btnBrowseInputVideo";
            btnBrowseInputVideo.Size = new Size(142, 29);
            btnBrowseInputVideo.TabIndex = 0;
            btnBrowseInputVideo.Text = "Chọn Video";
            btnBrowseInputVideo.UseVisualStyleBackColor = true;
            btnBrowseInputVideo.Click += btnBrowseInputVideo_Click;
            // 
            // btnBrowseBackgroundImage
            // 
            btnBrowseBackgroundImage.Location = new Point(34, 499);
            btnBrowseBackgroundImage.Name = "btnBrowseBackgroundImage";
            btnBrowseBackgroundImage.Size = new Size(142, 29);
            btnBrowseBackgroundImage.TabIndex = 0;
            btnBrowseBackgroundImage.Text = "Chọn Ảnh Nền";
            btnBrowseBackgroundImage.UseVisualStyleBackColor = true;
            btnBrowseBackgroundImage.Click += btnBrowseBackgroundImage_Click;
            // 
            // btnBrowseOutputVideo
            // 
            btnBrowseOutputVideo.Location = new Point(34, 548);
            btnBrowseOutputVideo.Name = "btnBrowseOutputVideo";
            btnBrowseOutputVideo.Size = new Size(142, 29);
            btnBrowseOutputVideo.TabIndex = 0;
            btnBrowseOutputVideo.Text = "Vị Trí Lưu";
            btnBrowseOutputVideo.UseVisualStyleBackColor = true;
            btnBrowseOutputVideo.Click += btnBrowseOutputVideo_Click;
            // 
            // txtInputVideo
            // 
            txtInputVideo.Location = new Point(222, 454);
            txtInputVideo.Name = "txtInputVideo";
            txtInputVideo.Size = new Size(328, 29);
            txtInputVideo.TabIndex = 4;
            // 
            // txtBackgroundImage
            // 
            txtBackgroundImage.Location = new Point(222, 500);
            txtBackgroundImage.Name = "txtBackgroundImage";
            txtBackgroundImage.Size = new Size(328, 29);
            txtBackgroundImage.TabIndex = 4;
            // 
            // txtOutputVideo
            // 
            txtOutputVideo.Location = new Point(222, 549);
            txtOutputVideo.Name = "txtOutputVideo";
            txtOutputVideo.Size = new Size(328, 29);
            txtOutputVideo.TabIndex = 4;
            // 
            // btnRemove
            // 
            btnRemove.Location = new Point(596, 486);
            btnRemove.Name = "btnRemove";
            btnRemove.Size = new Size(142, 55);
            btnRemove.TabIndex = 3;
            btnRemove.Text = "Xóa Phông Video";
            btnRemove.UseVisualStyleBackColor = true;
            btnRemove.Click += btnRemove_Click;
            // 
            // txtStatus
            // 
            txtStatus.AutoSize = true;
            txtStatus.Location = new Point(615, 552);
            txtStatus.Name = "txtStatus";
            txtStatus.Size = new Size(103, 21);
            txtStatus.TabIndex = 5;
            txtStatus.Text = "Thành Công";
            // 
            // RemoveBackgroundImage
            // 
            AutoScaleDimensions = new SizeF(10F, 21F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = Color.White;
            ClientSize = new Size(774, 597);
            Controls.Add(txtStatus);
            Controls.Add(txtOutputVideo);
            Controls.Add(txtBackgroundImage);
            Controls.Add(txtInputVideo);
            Controls.Add(comboRemoveBackground);
            Controls.Add(btnRemove);
            Controls.Add(btnSaveImage);
            Controls.Add(btnChangeBackground);
            Controls.Add(btnBrowseOutputVideo);
            Controls.Add(btnBrowseBackgroundImage);
            Controls.Add(btnBrowseInputVideo);
            Controls.Add(btnLoadImage);
            Controls.Add(label2);
            Controls.Add(label1);
            Controls.Add(pictureBoxProcessed);
            Controls.Add(pictureBoxOriginal);
            Font = new Font("Times New Roman", 14.25F, FontStyle.Regular, GraphicsUnit.Point, 0);
            FormBorderStyle = FormBorderStyle.FixedDialog;
            Margin = new Padding(4);
            MaximizeBox = false;
            Name = "RemoveBackgroundImage";
            StartPosition = FormStartPosition.CenterScreen;
            Text = "Ứng dụng xóa phông";
            ((System.ComponentModel.ISupportInitialize)pictureBoxOriginal).EndInit();
            ((System.ComponentModel.ISupportInitialize)pictureBoxProcessed).EndInit();
            ResumeLayout(false);
            PerformLayout();
        }

        #endregion

        private PictureBox pictureBoxOriginal;
        private PictureBox pictureBoxProcessed;
        private Label label1;
        private Label label2;
        private Button btnLoadImage;
        private Button btnSaveImage;
        private Button btnChangeBackground;
        private ComboBox comboRemoveBackground;
        private Button btnBrowseInputVideo;
        private Button btnBrowseBackgroundImage;
        private Button btnBrowseOutputVideo;
        private TextBox txtInputVideo;
        private TextBox txtBackgroundImage;
        private TextBox txtOutputVideo;
        private Button btnRemove;
        private Label txtStatus;
    }
}
