
import cv2
from pathlib import Path
import pathlib

from collections import Counter

import numpy as np
from tqdm import tqdm

def bgr_to_hex(b, g, r):
    """
    Converts a BGR color tuple to a hexadecimal color string.

    Args:
        b (int): Blue component (0-255).
        g (int): Green component (0-255).
        r (int): Red component (0-255).

    Returns:
        str: The hexadecimal color string (e.g., "#RRGGBB").
    """
    # Reorder to RGB
    red = r
    green = g
    blue = b

    # Convert each component to a two-digit hexadecimal string
    hex_color = f"#{red:02X}{green:02X}{blue:02X}"
    return hex_color

def main(img_path: pathlib.PosixPath, config_path: pathlib.PosixPath | None = None):
	if config_path is None:
		config_path = img_path.parent

	img: np.ndarray | None = cv2.imread(str(img_path))
	if img is None:
		raise FileNotFoundError(f"File {img_path} is not exist")

	img_vector = img.reshape(-1, 3)
	uniq, counts = np.unique(img_vector, axis=0, return_counts=True)

	neighborhood=10
	neighborhood_step=2
	max_neighborhood=50

	need_colors = 10

	while True:
		n = len(uniq)
		used = np.zeros(n, dtype=bool)
		merged_colors = []
		merged_counts = []

		for i in tqdm(range(n)):
			if used[i]:
				continue
		
			diff = np.abs(uniq - uniq[i])
			mask = np.all(diff <= neighborhood, axis=1)

			used |= mask

			weights = counts[mask][:, None]
			weighted_avg = np.sum(uniq[mask] * weights, axis=0) / np.sum(weights)

			merged_colors.append(weighted_avg)
			merged_counts.append(np.sum(counts[mask]))

		if len(uniq) == len(merged_colors) and neighborhood < max_neighborhood + neighborhood_step:
			neighborhood += neighborhood_step
		elif len(uniq) == len(merged_colors) and neighborhood >= max_neighborhood + neighborhood_step:
			break

		if len(uniq) <= need_colors:
			break
		uniq = np.array(merged_colors)
		counts = np.array(merged_counts)

	ready_colors = {bgr_to_hex(*uniq.astype("i")[i]) : int(counts[i]) for i in range(len(uniq))}

	print(len(uniq), sorted(ready_colors.items(), key=lambda item: item[1], reverse=True))


	
a=[('#BE7372', 2311051), ('#BB71B1', 1363333), ('#29142D', 750201), ('#DFA8B2', 564479), ('#FAE6E1', 556846), ('#6A3943', 194473), ('#7E777B', 30038), ('#E9262F', 549), ('#424C95', 352), ('#AB1877', 327), ('#B41127', 259), ('#F85E60', 205), ('#95D6D5', 48), ('#A88DEA', 7)]

if __name__ == "__main__":
	#img_path = Path("/home/hypoxie/images/wallpapers/n_girl_overdose.jpg")

	img_path = Path("./test_image.png")
	main(img_path) # type:ignore