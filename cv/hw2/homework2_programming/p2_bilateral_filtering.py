"""
CS 6384 Homework 2 Programming: Part 3 - bilateral filter
Implement the bilateral_filtering() function in this python script
"""
 
import cv2
import numpy as np
import math

def zero_pad(
    img: np.uint8,
    pad_size: int
) -> np.uint8:
    sizeX, sizeY = img.shape
    new_img = np.zeros((sizeX + 2 * pad_size, sizeY + 2 * pad_size))
    new_img[pad_size:-pad_size, pad_size:-pad_size] = img
    return new_img

def remove_pad(
    img: np.uint8,
    pad_size: int
) -> np.uint8:
    return img[pad_size:-pad_size, pad_size:-pad_size]


def bilateral_filtering(
    img: np.uint8,
    spatial_variance: float,
    intensity_variance: float,
    kernel_size: int,
) -> np.uint8:
    """
    Homework 2 Part 3
    Compute the bilaterally filtered image given an input image, kernel size, spatial variance, and intensity range variance
    """

    img = img / 255
    img = img.astype("float32")
    half = kernel_size // 2
    img = zero_pad(img, half)
    sizeX, sizeY = img.shape
    img_filtered = np.zeros(img.shape) # Placeholder of the filtered image
    
    # Todo: For each pixel position [i, j], you need to compute the filtered output: img_filtered[i, j]
    # step 1: compute kernel_sizexkernel_size spatial and intensity range weights of the bilateral filter in terms of spatial_variance and intensity_variance. 
    # step 2: compute the filtered pixel img_filtered[i, j] using the obtained kernel weights and the neighboring pixels of img[i, j] in the kernel_sizexkernel_size local window
    # The bilateral filtering formula can be found in slide 15 of lecture 6
    # Tip: use zero-padding to address the black border issue.

    # ********************************
    # Your code is here.
    # ********************************
    
    for i in range(half, sizeX - half):
        for j in range(half, sizeY - half):
            weights = np.zeros((kernel_size, kernel_size))
            for k in range(-half, half+1):
                for l in range(-half, half+1):
                    d_intensity = (img[i, j] - img[k, l])**2
                    d_space = k**2 + l**2
                    weights[k, l] = np.exp(-d_intensity / (2*intensity_variance)) * np.exp(-d_space / (2 * spatial_variance))
            weights /= weights.sum()
            
            patch = img[i-half:i+half+1, j-half:j+half+1]
            img_filtered[i, j] = np.sum(np.multiply(patch, weights))
    
    img_filtered = remove_pad(img_filtered, half)
    img_filtered = img_filtered * 255
    img_filtered = np.uint8(img_filtered)
    return img_filtered

 
if __name__ == "__main__":
    img = cv2.imread("data/img/butterfly.jpeg", 0) # read gray image
    img = cv2.resize(img, (256, 256), interpolation = cv2.INTER_AREA) # reduce image size for saving your computation time
    cv2.imwrite('results/im_original.png', img) # save image 
    
    # Generate Gaussian noise
    noise = np.random.normal(0,0.6,img.size)
    noise = noise.reshape(img.shape[0],img.shape[1]).astype('uint8')
   
    # Add the generated Gaussian noise to the image
    img_noise = cv2.add(img, noise)
    cv2.imwrite('results/im_noisy.png', img_noise)
    
    # Bilateral filtering
    spatial_variance = 30 # signma_s^2
    intensity_variance = 0.5 # sigma_r^2
    kernel_size = 7
    img_bi = bilateral_filtering(img_noise, spatial_variance, intensity_variance, kernel_size)
    cv2.imwrite('results/im_bilateral.png', img_bi)