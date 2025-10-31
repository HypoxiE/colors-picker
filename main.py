import choose_colors
import get_colors
from pathlib import Path

if __name__ == "__main__":
	#img_path = Path("/home/hypoxie/images/wallpapers/n_girl_overdose.jpg")

	img_path = Path("./a6abe8a35f243509ccbb8c8b8d3444e5.jpg")

	#print(str(img_path.parent) + "/" + (img_path.stem))

	pal = get_colors.get(img_path) # type:ignore

	choose_colors.choose(pal)

	print(pal)

