# ImageComparison
Compare all images (jpg &amp; png) in a folder, and any dumplicates are moved to the specified folder.  If two images closely match each other, a window displaying the two images is shown, and the user can select to move either or them, or leave them both in the original directory.

Run the script as follows:

    python3 imagecheck.py <directory containing the images> <directory where you want duplicates moved to>
    
You need to have the following installed via pip:
  1. skimage,
  2. numpy,
  3. opencv-python (cv2)
  4. tkinter (which is the windows manager used by the script)
  5. Pillow (pil)
  6. shutil

Notes:
  1. The script uses tkinter to produce the window and fucntion as the manager.  This has been tested under linux, but should work under Windows or MacOS.
  2. The script compares images using the ssim and mse comparisons.  Lines 150 and 151 define how 'close' the images need to be, to be considered similar.
  3. MSE produces a value from 0 upwards, with the lower the value, the closer the images are (0 implies an exact match).
  4. SSIM produces a value between -1 and 1, with -1 or 1 being a perfect match and 0 being competely different.
  5. By default these values are set to 100 and 0.8.
  6. Program is designed to run on a 1080p minimum monitor, as the size of the window is hardcored into the script.
