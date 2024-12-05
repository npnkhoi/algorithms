from PIL import Image
import numpy as np
import sys
from tqdm import tqdm

if __name__ == '__main__':
    source_image, k, dest_image = sys.argv[1], int(sys.argv[2]), sys.argv[3]

    # Load the image
    image = Image.open(source_image).convert('RGB')
    image = np.array(image)

    # Flatten the image
    h, w, c = image.shape
    image = image.reshape((h * w, c))

    # Initialize the centroids
    centroids = np.random.randint(0, 256, (k, c))

    # Run the K-means algorithm
    for iteration in tqdm(range(100)):
        # Assign each pixel to the closest centroid
        distances = np.linalg.norm(image[:, None] - centroids, axis=2)
        labels = np.argmin(distances, axis=1)

        # Update the centroids
        convergence = True
        for i in range(k):
            mask = labels == i
            if np.sum(mask) == 0:
                continue
            new_value = np.mean(image[mask], axis=0)
            if np.linalg.norm(new_value - centroids[i]) < 1:
                continue
            convergence = False
            centroids[i] = new_value
        
        if convergence:
            print(f'Converged at iteration {iteration}')
            break
    
    # Assign each pixel to the closest centroid
    distances = np.linalg.norm(image[:, None] - centroids, axis=2)
    labels = np.argmin(distances, axis=1)

    # Create the new image
    new_image = np.zeros_like(image)
    for i in range(k):
        new_image[labels == i] = centroids[i]
    new_image = new_image.reshape((h, w, c))

    # Save the new image
    new_image = Image.fromarray(new_image)
    new_image.save(dest_image)

