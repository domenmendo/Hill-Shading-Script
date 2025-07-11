import numpy as np
from PIL import Image
import math

def hill_shading(height_map, zenith_deg, azimuth_deg):
    """
    Implementacija hill-shading algoritma.
    
    Args:
        height_map: 2D numpy array z višinami
        zenith_deg: Zenit v stopinjah
        azimuth_deg: Azimut v stopinjah
    
    Returns:
        2D numpy array z vrednostmi osenčenosti
    """
    
    # Pretvorba stopinj v radiane
    zenith_rad = math.radians(zenith_deg)
    azimuth_rad = math.radians(azimuth_deg)
    
    height, width = height_map.shape
    
    # Inicializacija rezultatnih matrik
    slope_map = np.zeros((height, width))
    aspect_map = np.zeros((height, width))
    shading_map = np.zeros((height, width))
    
    # Iteracija čez vse piksle (razen robnih)
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            # Definiranje pikslov v 3x3 okolici (E je trenutni piksel)
            # A D G
            # B E H  
            # C F I
            A = height_map[y-1, x-1]
            D = height_map[y-1, x]
            G = height_map[y-1, x+1]
            B = height_map[y, x-1]
            E = height_map[y, x]
            H = height_map[y, x+1]
            C = height_map[y+1, x-1]
            F = height_map[y+1, x]
            I = height_map[y+1, x+1]
            
            # Izračun gradientov
            dzdx = ((C + 2*F + I) - (A + 2*D + G)) / 8.0
            dzdy = ((G + 2*H + I) - (A + 2*B + C)) / 8.0
            
            # Izračun slope (naklon)
            slope = max(math.atan(math.sqrt(dzdx**2 + dzdy**2)), 0)
            slope_map[y, x] = slope
            
            # Izračun aspect (usmerjenost)
            aspect = 0
            if slope > 0:
                aspect = (math.atan2(dzdy, -dzdx) + 2*math.pi) % (2*math.pi)
            else:
                if dzdy > 0:
                    aspect = math.pi/2
                elif dzdy < 0:
                    aspect = 3*math.pi/2
            
            aspect_map[y, x] = aspect
            
            # Izračun osenčenosti
            shading = (math.cos(-zenith_rad) * math.cos(slope) + 
                      math.cos(azimuth_rad - aspect) * math.sin(-zenith_rad) * math.sin(slope))
            
            shading_map[y, x] = shading
    
    return shading_map

def normalize_shading(shading_map):
    """
    Normalizacija vrednosti osenčenosti na interval [0, 255] za prikaz.
    """
    # Normalizacija na interval [0, 1]
    min_val = np.min(shading_map)
    max_val = np.max(shading_map)
    
    if max_val - min_val > 0:
        normalized = (shading_map - min_val) / (max_val - min_val)
    else:
        normalized = np.zeros_like(shading_map)
    
    # Pretvorba na 8-bitne vrednosti
    return (normalized * 255).astype(np.uint8)

def load_tiff_image(filepath):
    """
    Naloži 32-bitno Grayscale TIFF sliko.
    """
    try:
        with Image.open(filepath) as img:
            # Pretvorba v numpy array
            height_map = np.array(img, dtype=np.float32)
            return height_map
    except Exception as e:
        print(f"Napaka pri nalaganju slike: {e}")
        return None

def save_result_image(shading_map, filepath):
    try:
        # Normalizacija za prikaz
        normalized = normalize_shading(shading_map)
        
        # Shranjevanje kot slika
        img = Image.fromarray(normalized, mode='L')
        img.save(filepath)
        print(f"Slika shranjena: {filepath}")
    except Exception as e:
        print(f"Napaka pri shranjevanju slike: {e}")

def main():
    # Pot do vhodne datoteke
    input_filepath = "mb-center_vhod.tif"  # Prilagodite poti
    
    # Naložimo višinsko karto
    height_map = load_tiff_image(input_filepath)
    
    if height_map is None:
        print("Ni mogoče naložiti vhodne datoteke. Ustvarjam testne podatke...")
        # Ustvarimo testne podatke (hrib)
        height_map = create_test_height_map()
    
    print(f"Velikost višinske karte: {height_map.shape}")
    print(f"Min višina: {np.min(height_map):.2f}, Max višina: {np.max(height_map):.2f}")
    
    # Parametri za 4 slike
    parameters = [
        (38, 230),    # 1. slika
        (230, 38),    # 2. slika  
        (45, 315),    # 3. slika (poljubno)
        (60, 135)     # 4. slika (poljubno)
    ]
    
    # Generiranje slik
    for i, (zenith, azimuth) in enumerate(parameters, 1):
        print(f"\nObdelava slike {i}: zenit={zenith}°, azimut={azimuth}°")
        
        # Izračun hill-shading
        shading_result = hill_shading(height_map, zenith, azimuth)
        
        # Shranjevanje rezultata  
        output_filename = f"zenit{zenith}_azimut{azimuth}.jpg"
        save_result_image(shading_result, output_filename)

def create_test_height_map():
    """
    Funkcija za ustvarjanje testne višinske karte z dvema hriboma.
    """
    size = 200
    height_map = np.zeros((size, size))
    
    # Ustvarimo nekaj hribov
    center_x, center_y = size // 2, size // 2
    
    for y in range(size):
        for x in range(size):
            # Glavni hrib v sredini
            dist1 = math.sqrt((x - center_x)**2 + (y - center_y)**2)
            height1 = max(0, 100 - dist1 * 0.8)
            
            # Manjši hrib
            dist2 = math.sqrt((x - center_x + 60)**2 + (y - center_y - 40)**2)
            height2 = max(0, 50 - dist2 * 1.2)
            
            height_map[y, x] = height1 + height2
    
    return height_map

if __name__ == "__main__":
    main()