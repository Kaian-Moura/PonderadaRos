import cv2
import numpy as np
import json
import matplotlib.pyplot as plt
import os

def process_dog_pipeline(image_path, output_json, output_pipeline_plot):
    # 1. Original
    img = cv2.imread(image_path)
    if img is None:
        print(f"Erro ao carregar a imagem: {image_path}")
        return
    
    h, w = img.shape[:2]
    target_h = 720
    target_w = int(w * (target_h / h))
    img_resized = cv2.resize(img, (target_w, target_h))
    img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
    
    # 2. Escala de Cinza + Gaussiana
    gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # 3. Limiarização (Threshold)
    _, thresh = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # 4. Máscara (Operações Morfológicas)
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    # 5. Gradiente Sobel (ou Canny para representar bordas)
    sobelx = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)
    sobel_mag = np.sqrt(sobelx**2 + sobely**2)
    sobel_mag = np.uint8(sobel_mag / sobel_mag.max() * 255)
    
    # 6. Contorno Final (Canny + Aproximação)
    edges = cv2.Canny(blurred, 100, 200)
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    filtered_contours = []
    for c in contours:
        if cv2.arcLength(c, False) > 40:
            epsilon = 0.002 * cv2.arcLength(c, True)
            filtered_contours.append(cv2.approxPolyDP(c, epsilon, True))
            
    # Mapeamento para Turtlesim
    all_points = np.vstack(filtered_contours).reshape(-1, 2)
    min_x, min_y = all_points.min(axis=0)
    max_x, max_y = all_points.max(axis=0)
    range_x, range_y = max_x - min_x, max_y - min_y
    scale = 9.0 / max(range_x, range_y)
    offset_x = (11.0 - range_x * scale) / 2.0 - min_x * scale
    offset_y = (11.0 - range_y * scale) / 2.0 - min_y * scale
    
    paths = []
    for contour in filtered_contours:
        path = [(float(p[0][0] * scale + offset_x), float(11.0 - (p[0][1] * scale + offset_y))) for p in contour]
        paths.append(path)
    
    with open(output_json, 'w') as f:
        json.dump(paths, f)

    # GERAR IMAGEM COMPOSTA (PIPELINE)
    plt.figure(figsize=(15, 10))
    plt.gcf().set_facecolor('#0a0a0a')
    plt.suptitle('Pipeline de Visão Computacional - Dog Draw', color='white', fontsize=20, fontweight='bold')
    
    titles = ['Original', 'Escala de Cinza + Gaussiana', 'Limiarização', 'Máscara', 'Gradiente Sobel', 'Contorno Final']
    images = [img_rgb, blurred, thresh, mask, sobel_mag, edges]
    cmaps = [None, 'gray', 'gray', 'gray', 'hot', 'gray']
    
    for i in range(6):
        plt.subplot(2, 3, i+1)
        if cmaps[i]:
            plt.imshow(images[i], cmap=cmaps[i])
        else:
            plt.imshow(images[i])
        plt.title(titles[i], color='white', fontsize=14)
        plt.axis('off')
        
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(output_pipeline_plot, facecolor='#0a0a0a')
    print(f"Pipeline gerada com sucesso: {output_pipeline_plot}")

if __name__ == "__main__":
    img_path = "/home/ubuntu/upload/dog.png"
    if os.path.exists(img_path):
        process_dog_pipeline(img_path, "/home/ubuntu/Cachorroponderada/dog_paths_v2.json", "/home/ubuntu/Cachorroponderada/pipeline_visao.png")
    else:
        print("Imagem dog.png não encontrada!")
