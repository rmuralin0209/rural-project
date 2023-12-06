from PIL import Image
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr
import os
from cryptography.fernet import Fernet
import numpy as np

def encrypt_data(data, key):
    cipher = Fernet(key)
    encrypted_data = cipher.encrypt(data)
    return encrypted_data

def decrypt_data(encrypted_data, key):
    cipher = Fernet(key)
    decrypted_data = cipher.decrypt(encrypted_data)
    return decrypted_data

def compress_and_encrypt_image(input_path, output_path, target_size_kb, target_ssim, target_psnr, encryption_key):
    # Open the image file
    with Image.open(input_path) as img:
        img = img.convert('RGB')
        # Save the image with different compression qualities until the target size is met
        for quality in range(1, 101):
            temp_output_path = output_path.replace('.jpg', f'_temp_q{quality}.jpg')
            img.save(temp_output_path, 'JPEG', quality=quality)

            # Check the size of the compressed image
            compressed_size_kb = os.path.getsize(temp_output_path) / 1024

            # If the compressed size is within the target threshold, check SSIM and PSNR
            if compressed_size_kb <= target_size_kb:
                compressed_img = np.array(Image.open(temp_output_path))

                # Convert the original image to NumPy array
                original_img = np.array(img)

                # Ensure the shapes match
                if original_img.shape != compressed_img.shape:
                    raise ValueError("Shapes of the original and compressed images do not match.")

                win_size = 7  # Adjust this value based on the size of your images

                # Calculate SSIM
                ssim_value = 0
                #ssim_value = ssim(original_img, compressed_img, win_size=win_size, full=True, multichannel=True)['ssim']

                # Calculate PSNR
                psnr_value = psnr(original_img, compressed_img)

                print(f"Quality: {quality}, Size: {compressed_size_kb:.2f} KB, SSIM: {ssim_value:.4f}, PSNR: {psnr_value:.2f}")


                # Check if SSIM and PSNR are within the specified thresholds
                if ssim_value >= target_ssim and psnr_value >= target_psnr:
                    # Convert compressed image to bytes
                    with open(temp_output_path, 'rb') as f:
                        compressed_data = f.read()

                    # Encrypt the compressed data
                    encrypted_data = encrypt_data(compressed_data, encryption_key)

                    # Save the encrypted data
                    with open(output_path, 'wb') as f:
                        f.write(encrypted_data)

                    print("Image compressed, encrypted, and meets SSIM and PSNR thresholds.")
                    break

            # Delete the temporary file
            os.remove(temp_output_path)

if __name__ == "__main__":
    # Specify the input image path
    input_image_path = 'socialnetwork/resources/apple.png'

    # Specify the output image path
    output_image_path = 'output_compressed_encrypted_image.jpg'

    # Specify the target size in kilobytes
    target_size_kb = 100  # Adjust this value based on your bandwidth constraints

    # Specify the target SSIM and PSNR values
    target_ssim = 0.95  # Adjust based on acceptable SSIM
    target_psnr = 30.0  # Adjust based on acceptable PSNR

    # Generate a random encryption key (replace with a secure key management solution in a production environment)
    encryption_key = Fernet.generate_key()

    # Compress, encrypt, and save the image
    compress_and_encrypt_image(input_image_path, output_image_path, target_size_kb, target_ssim, target_psnr, encryption_key)