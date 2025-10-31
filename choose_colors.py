import json

import numpy as np

import get_colors

def bgr_to_hex(b, g, r):
    # Reorder to RGB
    red = r
    green = g
    blue = b

    # Convert each component to a two-digit hexadecimal string
    hex_color = f"#{red:02X}{green:02X}{blue:02X}"
    return hex_color

def cosine_similarity(a, b):
	np_a = np.array(a) + 1
	np_b = np.array(b) + 1
	dot_product =  np.dot(np_a, np_b)

	norm_a = np.linalg.norm(np_a)
	norm_b = np.linalg.norm(np_b)

	return dot_product / (norm_a * norm_b)

def choose(palitre: get_colors.Palitre):
	def sortfunc(color):
		black = (0, 0, 0)

		return cosine_similarity(black, color)
		
	print(sortfunc(list(palitre.colors.keys())[0]))

	print(dict(sorted(list(palitre.colors.items()), key=lambda a: sortfunc(a[0]))))

	#with open(palitre.conf_path, 'w') as f:
	#	json.dump(dict(sorted(palitre.colors.items(), key=lambda item: item[1], reverse=True)), f)

if __name__ == "__main__":
	a = get_colors.Palitre(
		{(10, 10, 17): 243157, (90, 90, 107): 70347, (49, 49, 62): 60714, (26, 27, 37): 38603, (66, 66, 81): 28985, (114, 114, 133): 6139, (198, 198, 217): 9, (157, 157, 176): 8, (225, 225, 244): 5, (182, 181, 201): 3},
		"test.conf"
	)

	choose(a)


