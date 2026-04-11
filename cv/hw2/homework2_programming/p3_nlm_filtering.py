"""
CS 6384 Homework 2 Programming: Part 4 - non-local means filter
Implement the nlm_filtering() function in this python script
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

def nlm_filtering(
    img: np.uint8,
    intensity_variance: float,
    patch_size: int,
    window_size: int,
) -> np.uint8:
    """
    Homework 2 Part 4
    Compute the filtered image given an input image, kernel size of image patch, spatial variance, and intensity range variance
    """

    img = img / 255
    img = img.astype("float32")
    window_half = window_size // 2
    patch_half = patch_size // 2
    pad_size = patch_half + window_half
    img = zero_pad(img, pad_size)    
    sizeX, sizeY = img.shape
    img_filtered = np.zeros(img.shape) # Placeholder of the filtered image
    
    # Todo: For each pixel position [i, j], you need to compute the filtered output: img_filtered[i, j] using a non-local means filter
    # step 1: compute window_sizexwindow_size filter weights of the non-local means filter in terms of intensity_variance. 
    # step 2: compute the filtered pixel img_filtered[i, j] using the obtained kernel weights and the pixel values in the search window
    # Please see slides 30 and 31 of lecture 6. Clarification: the patch_size refers to the size of small image patches (image content in yellow, 
    # red, and blue boxes in the slide 30); intensity_variance denotes sigma^2 in slide 30; the window_size is the size of the search window as illustrated in slide 31.
    # Tip: use zero-padding to address the black border issue. 

    # ********************************
    # Your code is here.
    # ********************************
    
    
    
    
    
    def ssd(a, b) -> float:
        d = a - b
        d2 = np.multiply(d, d)
        s = d2.sum()
        return s
    
    for pi in range(window_half + patch_half, sizeX - window_half - patch_half):
        for pj in range(window_half + patch_half, sizeY - window_half - patch_half):
            target_patch = img[pi-patch_half:pi+patch_half+1, pj-patch_half:pj+patch_half+1]
            window = img[pi-window_half:pi+window_half+1, pj-window_half:pj+window_half+1]
            w = np.zeros((window_size, window_size)) # w[i, j] means the weight of the patch centered at [i, j] OF the window
            # the target pixel is at [window_half, window_half]
            for qi in range(pi-window_half, pi+window_half+1):
                for qj in range(pj-window_half, pj+window_half+1):
                    ref_patch = img[qi-patch_half:qi+patch_half+1, qj-patch_half:qj+patch_half+1]
                    i_index = qi - pi + window_half
                    j_index = qj - pj + window_half
                    w[i_index, j_index] = np.exp(-ssd(target_patch, ref_patch)/(2*intensity_variance))
            
            w /= w.sum()
            img_filtered[pi, pj] = np.multiply(window, w).sum()
            
    img_filtered = img_filtered * 255
    img_filtered = np.uint8(img_filtered)
    img_filtered = remove_pad(img_filtered, pad_size)
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
    intensity_variance = 1
    patch_size = 5 # small image patch size
    window_size = 15 # serach window size
    img_bi = nlm_filtering(img_noise, intensity_variance, patch_size, window_size)
    cv2.imwrite('results/im_nlm.png', img_bi)