
import json
import cv2
from pathlib import Path
import pathlib

from collections import Counter

import numpy as np
from tqdm import tqdm

class Palitre:
	def __init__(self, colors, conf_path) -> None:
		self.colors = dict(sorted(colors.items(), key=lambda item: item[1], reverse=True))
		self.length = len(colors)
		self.conf_path = conf_path
		
	def __str__(self) -> str:
		return str(self.colors)

def get(img_path: pathlib.PosixPath, config_path: str | None = None):

	if config_path is None:
		config_path = str(img_path.parent)  + "/" +  str(img_path.stem) + ".conf"

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

	ready_colors = {tuple([int(i) for i in uniq.astype("i")[i]]) : int(counts[i]) for i in range(len(uniq))}

	return Palitre(ready_colors, config_path)

