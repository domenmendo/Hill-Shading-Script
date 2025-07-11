# Hill Shading Script

This Python script implements a **hill-shading algorithm** to visualize terrain data from a height map. It takes a 32-bit grayscale TIFF image as input, calculates shading based on a customizable light source (zenith and azimuth angles), and outputs shaded JPEG images.

If no input file is found, the script automatically generates a synthetic test height map with two hills.

---

## ✨ Features

- **Hill Shading Algorithm**: Calculates illumination of terrain from a simulated light source.
- **Input Flexibility**: Supports 32-bit TIFF input or generates test data if input is missing.
- **Custom Light Source**: Adjustable **zenith** and **azimuth** angles for shading direction.
- **Image Output**: Saves shaded images as `.jpg` files based on the light parameters.

---

## 🧰 Prerequisites

Install the required Python libraries:

```bash
pip install numpy Pillow
```

---

## 🗂️ How to Use

### 1. Prepare the Input File (Optional)
Place your **32-bit grayscale TIFF height map** in the same directory as `main.py` and name it:

```
mb-center_vhod.tif
```

> If this file is **not found**, the script will automatically generate a test height map.

### 2. Run the Script

```bash
python main.py
```

### 3. Output
- Shaded images will be saved in the same directory.
- Filenames will include the **zenith** and **azimuth** angles used:
  ```
  zenit38_azimut230.jpg
  zenit230_azimut38.jpg
  zenit45_azimut315.jpg
  zenit60_azimut135.jpg
  ```

---

## 🧠 Script Details

### `hill_shading(height_map, zenith_deg, azimuth_deg)`
- Core function that computes terrain shading.
- Uses slope/aspect and light angles to calculate pixel shading.

### `normalize_shading(shading_map)`
- Normalizes shading to an 8-bit range (0–255) for image output.

### `load_tiff_image(filepath)`
- Loads a 32-bit grayscale TIFF file into a NumPy array.

### `save_result_image(shading_map, filepath)`
- Saves the shaded image as a JPEG.

### `create_test_height_map()`
- Generates a 200x200 test height map with two hills for synthetic shading.

### `main()`
- Loads the TIFF or generates test data.
- Logs shape and height statistics.
- Applies `hill_shading()` for four predefined light source settings.
- Saves each result using `save_result_image()`.

---

## 🖼️ Example Output

After execution, you will find images such as:

- `zenit38_azimut230.jpg`
- `zenit230_azimut38.jpg`
- `zenit45_azimut315.jpg`
- `zenit60_azimut135.jpg`

Each image visualizes terrain shading from a different light direction.
