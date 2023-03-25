from PIL import Image

image = Image.new("RGB", (2000, 2000), color="white")

image.save("fon.jpg")
# im = Image.open('static/fon.jpg')
# width, height = im.size
#
# # Setting the points for cropped image
# left = 0
# top = 0
# right = 1000
# bottom = 1000
#
# # Cropped image of above dimension
# # (It will not change original image)
# im1 = im.crop((0, 0, 1500, 900))
# im1.save("fon.jpg", "JPEG")