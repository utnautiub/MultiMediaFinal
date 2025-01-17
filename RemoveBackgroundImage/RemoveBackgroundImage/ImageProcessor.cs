using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Drawing;

namespace RemoveBackgroundImage
{
    internal class ImageProcessor
    {
        public static Bitmap RemoveBackground(Bitmap image)
        {
            int width = image.Width;
            int height = image.Height;
            Bitmap processedImage = new Bitmap(width, height);
            
            for (int y = 0; y < height; y++)
            {
                for (int x = 0; x < width; x++)
                {
                    Color pixelColor = image.GetPixel(x, y);
                    int gray = (int)(pixelColor.R * 0.3 + pixelColor.G * 0.59 + pixelColor.B * 0.11);

                    if (gray < 128)
                    {
                        processedImage.SetPixel(x, y, Color.FromArgb(128, gray, gray, gray));
                    }
                    else 
                    {
                        processedImage.SetPixel(x, y, pixelColor);
                    }
                }
            }

            return processedImage;
        }
    }
}
