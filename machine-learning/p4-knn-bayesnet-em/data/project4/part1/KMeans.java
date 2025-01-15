/*** Author: Vibhav Gogate
The University of Texas at Dallas
*****/

import java.awt.AlphaComposite;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import javax.imageio.ImageIO;

public class KMeans {
	static int MAX_ITERATIONS = 20;

	public static void main(String[] args) {
		if (args.length < 3) {
			System.out.println("Usage: Kmeans <input-image> <k> <output-image>");
			return;
		}
		try {
			BufferedImage originalImage = ImageIO.read(new File(args[0]));
			int k = Integer.parseInt(args[1]);
			BufferedImage kmeansJpg = kmeans_helper(originalImage, k);
			ImageIO.write(kmeansJpg, "jpg", new File(args[2]));

		} catch (IOException e) {
			System.out.println(e.getMessage());
		}
	}

	private static BufferedImage kmeans_helper(BufferedImage originalImage, int k) {
		int w = originalImage.getWidth();
		int h = originalImage.getHeight();
		BufferedImage kmeansImage = new BufferedImage(w, h, originalImage.getType());
		Graphics2D g = kmeansImage.createGraphics();
		g.drawImage(originalImage, 0, 0, w, h, null);
		// Read rgb values from the image
		
		int[] rgb = new int[w * h];
		int count = 0;
		for (int i = 0; i < w; i++) {
			for (int j = 0; j < h; j++) {
				rgb[count++] = kmeansImage.getRGB(i, j);
			}
		}
		
		// System.out.println("rgb.length = " + rgb.length);
		// // Print the first 10 values of rgb
		// for (int i = 0; i < 10 && i < rgb.length; i++) {
		// 	System.out.println("rgb[" + i + "] = " + rgb[i]);
		// }

		// Call kmeans algorithm: update the rgb values
		kmeans(rgb, k);

		// Write the new rgb values to the image
		count = 0;
		for (int i = 0; i < w; i++) {
			for (int j = 0; j < h; j++) {
				kmeansImage.setRGB(i, j, rgb[count++]);
			}
		}
		return kmeansImage;
	}

	// Your k-means code goes here
	// Update the array rgb by assigning each entry in the rgb array to its cluster
	// center
	private static void kmeans(int[] rgb, int k) {
		System.out.println("Image size: " + rgb.length);
		
		int minValue = Integer.MAX_VALUE;
		int maxValue = Integer.MIN_VALUE;

		for (int i = 0; i < rgb.length; i++) {
			minValue = Math.min(minValue, rgb[i]);
			maxValue = Math.max(maxValue, rgb[i]);
		}

		System.out.println("minValue = " + minValue);
		System.out.println("maxValue = " + maxValue);

		// Initialize the clusters
		
		// initialize the cluster centers randomly
		// accept that the centers can be identical
		int[] clusterCenters = new int[k];
		for (int i = 0; i < k; i++) {
			clusterCenters[i] = (int) Math.random() * (maxValue - minValue) + minValue;
		}
		
		int[] clusterAssignments = new int[rgb.length];
		int[] clusterSizes = new int[k];
		int[] clusterSums = new int[k];

		for (int iter = 0; iter < MAX_ITERATIONS; iter++) {
			// Reset the cluster sizes and sums
			for (int i = 0; i < k; i++) {
				clusterSizes[i] = 0;
				clusterSums[i] = 0;
			}

			// Assign each pixel to the nearest cluster center
			for (int i = 0; i < rgb.length; i++) {
				int minDist = Integer.MAX_VALUE;
				int minCluster = -1;
				
				// Find the nearest cluster center
				for (int j = 0; j < k; j++) {
					int dist = 0;
					for (int channel = 0; channel < 4; ++channel) {
						int pixelChannel = (rgb[i] >> (8 * channel)) & 0xFF;
						int centerChannel = (clusterCenters[j] >> (8 * channel)) & 0xFF;
						dist += (int) Math.pow(pixelChannel - centerChannel, 2);
						// dist += Math.abs(pixelChannel - centerChannel);
					}

					// int dist = Math.abs(rgb[i] - clusterCenters[j]);

					if (dist < minDist) {
						minDist = dist;
						minCluster = j;
					}
				}
				
				// Update the cluster assignments, sizes, and sums
				clusterAssignments[i] = minCluster;
				clusterSizes[minCluster]++;
				clusterSums[minCluster] += rgb[i];
			}

			// Update the cluster centers
			boolean converged = true;
			for (int i = 0; i < k; i++) {
				if (clusterSizes[i] == 0) {
					// Reinitialize the cluster center if it has no pixels
					clusterCenters[i] = (int) Math.random() * (maxValue - minValue) + minValue;
					continue;
				}
				int newCenter = clusterSums[i] / clusterSizes[i];
				if (newCenter != clusterCenters[i]) {
					converged = false;
					clusterCenters[i] = newCenter;
				}
			}

			if (converged) {
				System.out.println("Converged after " + iter + " iterations");
				break;
			}
		}

		// System.out.println("Final cluster centers:");
		// for (int i = 0; i < k; i++) {
		// 	System.out.println("clusterCenters[" + i + "] = " + clusterCenters[i]);
		// }

		// Assign each pixel to the nearest cluster center
		for (int i = 0; i < rgb.length; i++) {
			// if (i < 10) {
			// 	System.out.println("clusterAssignments[" + i + "] = " + clusterAssignments[i]);
			// }
			rgb[i] = clusterCenters[clusterAssignments[i]];
		}
	}

}
