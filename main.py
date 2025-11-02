import sys
from pathlib import Path
import get_colors  # твои модули
import choose_colors

# допустимые расширения
EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif"}

def process_image(img_path: Path):
    """Обработка одного изображения."""
    print(f"→ In process: {img_path}")
    pal = get_colors.get(img_path)  # type: ignore
    choose_colors.choose(pal)

def main():
    if len(sys.argv) < 2:
        print("Использование: python main.py <файл|папка|шаблон>")
        print("Примеры:")
        print("  python main.py image.jpg")
        print("  python main.py ./images")
        print("  python main.py './*'")
        print("  python main.py ./images/*.png")
        return

    # все аргументы (могут быть развернутыми shell’ом)
    inputs = [Path(arg) for arg in sys.argv[1:]]
    all_files = []

    for inp in inputs:
        if "*" in str(inp.name):  # если шаблон в кавычках
            base = inp.parent if inp.parent != Path("") else Path(".")
            pattern = inp.name
            all_files.extend(base.rglob(pattern))
        elif inp.is_dir():  # если передали папку
            for file in inp.rglob("*"):
                if file.suffix.lower() in EXTENSIONS:
                    all_files.append(file)
        elif inp.is_file():  # конкретный файл
            all_files.append(inp)
        else:
            print(f"⚠️  Пропущено: {inp} (не найдено)")
    
    if not all_files:
        print("❌ Файлы не найдены.")
        return

    all_files = sorted(set(all_files))

    for file in all_files:
        if file.suffix.lower() in EXTENSIONS:
            process_image(file)

if __name__ == "__main__":
    main()
