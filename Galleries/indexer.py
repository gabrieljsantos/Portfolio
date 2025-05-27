import os
from PIL import Image

grid = []
grid_sized = 100
pixel_factor_for_grid = 500
grid_width = 9
grid_maximum_size = 3

def is_area_free(filling, x, y, x1, y1, grid_width):
    if x + x1 > grid_width:
        return False
    if y + y1 > len(filling):
        return False
    for dy in range(y1):
        for dx in range(x1):
            if y + dy >= len(filling) or filling[y + dy][x + dx]:
                return False
    return True


def generate_layout_images(images_folder, layout_file_path):
    filling = [[False for _ in range(grid_width)]]
    
    images = [f for f in os.listdir(images_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    layout_data = []

    x = 0
    y = 0

    for image_name in images:
        image_path = os.path.join(images_folder, image_name)
        with Image.open(image_path) as img:
            width, height = img.size
            x1 = round(width / pixel_factor_for_grid)
            y1 = round(height / pixel_factor_for_grid)

            if x1 > grid_maximum_size and x1 >= y1:
                scale = grid_maximum_size / x1
                x1 = grid_maximum_size
                y1 = round(y1 * scale)

            elif y1 > grid_maximum_size and y1 > x1:
                scale = grid_maximum_size / y1
                y1 = grid_maximum_size
                x1 = round(x1 * scale)

            if y1 == x1 * 2 or y1 * 2 == x1:
                x1 *= 2
                y1 *= 2

            x1 = max(1, x1)
            y1 = max(1, y1)

            print("##",x,y)
            x = 0  # <- Resetar x no início da tentativa de posicionar nova imagem
            # Garante que a área esteja livre
            while not is_area_free(filling, x, y, x1, y1, grid_width):
                x += 1
                if x + x1 > grid_width:
                    x = 0
                    y += 1
                    # Garante que tenha linhas o suficiente
                    while y + y1 > len(filling):
                        filling.append([False for _ in range(grid_width)])
            print("@@",x,y)

            # Garante que há linhas suficientes na matriz 'filling'
            while y + y1 > len(filling):
                filling.append([False for _ in range(grid_width)])

            # Marca área ocupada como True
            for dy in range(y1):
                for dx in range(x1):
                    filling[y + dy][x + dx] = True

            # Adiciona entrada ao layout
            layout_data.append(f"{x}|{y}|{x1}|{y1}|{image_name}")

            # Atualiza posição x
            x += x1

    # Salvando o layout
    with open(layout_file_path, 'w') as layout_file:
        layout_file.write("\n".join(layout_data))

# Defina os caminhos das pastas
images_folder = 'Galleries/3D/3D_imgs'  # Substitua pelo caminho real da pasta de imagens
layout_file_path = 'Galleries/3D/layout.inf'  # Substitua pelo caminho real do arquivo layout.inf

generate_layout_images(images_folder, layout_file_path)

images_folder = 'Galleries/Keychain/Keychain_imgs'  # Substitua pelo caminho real da pasta de imagens
layout_file_path = 'Galleries/Keychain/layout.inf'  # Substitua pelo caminho real do arquivo layout.inf

generate_layout_images(images_folder, layout_file_path)





images_folder = 'Galleries/Personalizados/Personalizados_imgs'  # Substitua pelo caminho real da pasta de imagens
layout_file_path = 'Galleries/Personalizados/layout.inf'  # Substitua pelo caminho real do arquivo layout.inf

generate_layout_images(images_folder, layout_file_path)



print("Layout gerado com sucesso!")
