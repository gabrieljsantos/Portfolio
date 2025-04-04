import os
from PIL import Image

grid = []
grid_sized = 100
pixel_factor_for_grid = 500
grid_width = 12
grid_maximum_size = 3

def generate_layout_images(images_folder, layout_file_path):
    # Lista as imagens da pasta
    images = [f for f in os.listdir(images_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    layout_data = []
    # Variáveis para rastrear a posição
    x = 0
    y = 0
    y1 = 2 
    for image_name in images:
        image_path = os.path.join(images_folder, image_name)
        # Abrindo a imagem e calculando a proporção
        with Image.open(image_path) as img:
            width, height = img.size
            x1 = round(width / pixel_factor_for_grid)
            y1 = round(height / pixel_factor_for_grid)

            if x1 > grid_maximum_size and x1 >= y1:
                scale = grid_maximum_size / x1
                x1 = grid_maximum_size
                y1 = int(y1 * scale)

            elif y1 > grid_maximum_size and y1 > x1:
                scale = grid_maximum_size / y1
                y1 = grid_maximum_size
                x1 = int(x1 * scale)
                
            if x1 < 1 :
                x1 = 1
            if y1 < 1 :
                y1 = 1


            # Adiciona a linha no formato desejado
            layout_data.append(f"{x}|{y}|{x1}|{y1}|{image_name}")
            
        x += x1
        if x > grid_width :
            x = 0
            y += y1
    
    # Salvando o layout no arquivo
    with open(layout_file_path, 'w') as layout_file:
        layout_file.write("\n".join(layout_data))

# Defina os caminhos das pastas
images_folder = 'Galleries/3D/3D_imgs'  # Substitua pelo caminho real da pasta de imagens
layout_file_path = 'Galleries/3D/layout.inf'  # Substitua pelo caminho real do arquivo layout.inf

generate_layout_images(images_folder, layout_file_path)


images_folder = 'Galleries/Personalizados/Personalizados_imgs'  # Substitua pelo caminho real da pasta de imagens
layout_file_path = 'Galleries/Personalizados/layout.inf'  # Substitua pelo caminho real do arquivo layout.inf

generate_layout_images(images_folder, layout_file_path)

print("Layout gerado com sucesso!")
