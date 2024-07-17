from PIL import Image

# Open a JPEG image
jpeg_image_path = r'D:\celery_basic\image.jpg'
img = Image.open(jpeg_image_path)

# Convert the image to PNG and save it
png_image_path = r'D:\celery_basic\image.png'
img.save(png_image_path, 'PNG')

print(f"Image converted to PNG and saved at {png_image_path}")
