import cloudinary
import cloudinary.uploader
import os

# Import Config if your API keys are stored in config.py
try:
    from config import Config

    cloudinary.config(
        cloud_name=Config.CLOUDINARY_CLOUD_NAME,
        api_key=Config.CLOUDINARY_API_KEY,
        api_secret=Config.CLOUDINARY_API_SECRET,
        secure=True
    )
except ImportError:
    # If Config is not available, manually set the credentials
    cloudinary.config(
        cloud_name="your_cloud_name",
        api_key="your_api_key",
        api_secret="your_api_secret",
        secure=True
    )

def test_cloudinary_upload():
    """Uploads a test image to Cloudinary and prints the URL."""
    test_image_path = "static/uploads/Chitra_Rathore.jpg"  # Change this to any local image path

    # Check if the image file exists
    if not os.path.exists(test_image_path):
        print(f"Error: The file '{test_image_path}' does not exist. Place a valid image in the directory.")
        return

    try:
        # Upload image to Cloudinary
        response = cloudinary.uploader.upload(test_image_path)
        secure_url = response.get("secure_url")

        if secure_url:
            print(f"✅ Image uploaded successfully! View it here: {secure_url}")
        else:
            print("❌ Upload failed. No secure URL returned.")

    except Exception as e:
        print(f"❌ Error uploading image: {str(e)}")

if __name__ == "__main__":
    test_cloudinary_upload()
