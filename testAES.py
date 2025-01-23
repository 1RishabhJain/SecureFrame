import ast
from PIL import Image
import io
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from PIL.PngImagePlugin import PngInfo

def encryptImage(imagePath, left, upper, right, lower):
    image = Image.open(imagePath);

    cropped_image = image.crop((left, upper, right, lower))
    img_byte_array = io.BytesIO()
    cropped_image.save(img_byte_array, format="PNG")
    cropped_img_bytes = img_byte_array.getvalue()
    for y in range(upper, lower):
        for x in range(left, right):
            # Set the pixel to black (0, 0, 0 in RGB)
            image.putpixel((x, y), (0, 0, 0))

    key = get_random_bytes(16);

    iv = get_random_bytes(16)

    padded_data = pad(cropped_img_bytes, AES.block_size)

    cipher = AES.new(key, AES.MODE_CBC, iv)

    encrypted_data = cipher.encrypt(padded_data)
    print(type(encrypted_data))
    metadata = PngInfo()
    metadata.add_text("coordinates", f"{left}, {upper}, {right}, {lower}")
    metadata.add_text("encrypted_data", f"{encrypted_data}")

    image.save("modified_image.png", "PNG", pnginfo=metadata)

    print(key)
    print(iv)
    return key, iv

def decryptImage(imagePath, key, iv):

    image = Image.open(imagePath)
    metadata = image.info

    encryptedPixels = ast.literal_eval(metadata["encrypted_data"])
    coordinates = metadata["coordinates"].split(", ")
    print(type(encryptedPixels))

    cipher_decrypt = AES.new(key, AES.MODE_CBC, iv)

    decrypted_data = unpad(cipher_decrypt.decrypt(encryptedPixels), AES.block_size)

    img = Image.open(io.BytesIO(decrypted_data));

    pixels1 = img.load();
    pixels2 = image.load();

    a = 0
    b = 0
    image.show();
    for y in range(upper, lower):
        b = 0
        for x in range(left, right):
            pixels2[x, y] = pixels1[b,a];
            b = b + 1
        a = a + 1

    image.show();
    image.save("recreated_Image.png")

left = 1000
upper = 1000
right = 2000
lower = 2000

key, iv = encryptImage("image.png", left, upper, right, lower)

decryptImage("modified_image.png", key, iv)



