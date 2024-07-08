import os
from PIL import Image
import numpy as np

def swap_pixel_values(image_array, key):
    np.random.seed(key)
    indices = np.arange(image_array.size)
    np.random.shuffle(indices)
    swapped_array = image_array.flatten()[indices].reshape(image_array.shape)
    return swapped_array, indices

def reverse_swap_pixel_values(image_array, indices):
    reversed_array = np.empty_like(image_array.flatten())
    reversed_array[indices] = image_array.flatten()
    return reversed_array.reshape(image_array.shape)

def encrypt_image(image_path, key, output_path):
    # Open the image
    image = Image.open(image_path)
    image_array = np.array(image, dtype=np.int32)

    # Apply a simple encryption by manipulating the pixel values
    encrypted_array = (image_array + key) % 256

    # Apply pixel swapping
    encrypted_array, indices = swap_pixel_values(encrypted_array, key)

    # Create an encrypted image from the array
    encrypted_image = Image.fromarray(np.uint8(encrypted_array))

    # Save the encrypted image
    encrypted_image.save(output_path)

    # Save the indices used for swapping (for decryption)
    indices_output_path = output_path.replace('.png', '_indices.npy')
    np.save(indices_output_path, indices)
    print(f"Encrypted image and indices saved to {output_path} and {indices_output_path}")

def decrypt_image(image_path, key, output_path):
    # Open the encrypted image
    image = Image.open(image_path)
    image_array = np.array(image, dtype=np.int32)

    # Load the indices used for swapping
    indices_input_path = image_path.replace('.png', '_indices.npy')
    indices = np.load(indices_input_path)

    # Reverse pixel swapping
    decrypted_array = reverse_swap_pixel_values(image_array, indices)

    # Apply the decryption by reversing the pixel value manipulation
    decrypted_array = (decrypted_array - key) % 256

    # Create a decrypted image from the array
    decrypted_image = Image.fromarray(np.uint8(decrypted_array))

    # Save the decrypted image
    decrypted_image.save(output_path)
    print(f"Decrypted image saved to {output_path}")

def main():
    choice = input("Enter 'e' to encrypt or 'd' to decrypt: ").lower()
    image_path = input("Enter the image file path: ")
    key = 50  # Fixed key value for simplicity
    output_filename = input("Enter the output file name (with extension, e.g., output.png): ")
    
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, output_filename)

    if choice == 'e':
        encrypt_image(image_path, key, output_path)
    elif choice == 'd':
        decrypt_image(image_path, key, output_path)
    else:
        print("Invalid choice. Please enter 'e' for encryption or 'd' for decryption.")

if __name__ == "__main__":
    main()
