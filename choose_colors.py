import json

import numpy as np

import get_colors

def bgr_to_hex(b, g, r):
    # Reorder to RGB
    red = r
    green = g
    blue = b

    hex_color = f"#{red:02X}{green:02X}{blue:02X}"
    return hex_color

def bgra_to_hex(b, g, r, a=255):
    # Reorder to RGBA
    red = r
    green = g
    blue = b
    alpha = a

    hex_color = f"#{red:02X}{green:02X}{blue:02X}{alpha:02X}"
    return hex_color

def cosine_similarity(a, b):
	np_a = np.array(a) + 1
	np_b = np.array(b) + 1
	dot_product =  np.dot(np_a, np_b)

	norm_a = np.linalg.norm(np_a)
	norm_b = np.linalg.norm(np_b)

	return dot_product / (norm_a * norm_b)

def choose(palitre: get_colors.Palitre):
	def sortfunc(color, main_color):

		return cosine_similarity(main_color, color)
		
	#print(sortfunc(list(palitre.colors.keys())[0]))

	ready_colors = sorted(list(palitre.colors.items()), reverse=True, key=lambda a: sortfunc(a[0], list(palitre.colors.keys())[0]))

	#print(ready_dict)

	ready_json = {bgr_to_hex(*key) : value for key, value in ready_colors}
	main_color = max(ready_colors[:3], key=lambda a: a[1])[0]
	secondary_color = max(ready_colors[3:-3], key=lambda a: a[1])[0]
	text_color = max(ready_colors[-3:], key=lambda a: a[1])[0]
	

	save_conf = {
		"all_colors": ready_json,
		"eww": {
			"main_color": bgr_to_hex(*(main_color)[:3]),
			"secondary_color": bgr_to_hex(*(secondary_color)[:3]),
			"text_color": bgr_to_hex(*(text_color)[:3]),
		},
		"hyprland": {
			"active_border_color_1": bgra_to_hex(*secondary_color),
			"active_border_color_2": bgra_to_hex(*text_color),
			"inactive_border_color_1": bgra_to_hex(*main_color),
			"inactive_border_color_2": bgra_to_hex(*main_color),
		}
	}
	

	with open(palitre.conf_path, 'w') as f:
		json.dump(save_conf, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
	a = get_colors.Palitre(
		{(10, 10, 17): 243157, (90, 90, 107): 70347, (49, 49, 62): 60714, (26, 27, 37): 38603, (66, 66, 81): 28985, (114, 114, 133): 6139, (198, 198, 217): 9, (157, 157, 176): 8, (225, 225, 244): 5, (182, 181, 201): 3},
		"test.conf"
	)

	choose(a)


