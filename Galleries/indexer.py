import os
from PIL import Image
import time
import random

grid = []
grid_sized = 300
pixel_factor_for_grid = 500
grid_width = 11
grid_maximum_size = 3
n_grid_y_init = 5

def get_largest_free_block(filling, start_x, start_y, grid_width, grid_height):
    if filling[start_y][start_x]:  # já está ocupado
        return 0, 0

    max_width = 0
    max_height = 0

    # Limite máximo de altura a partir do ponto
    for y in range(start_y, grid_height):
        if filling[y][start_x]:
            break
        max_height += 1

    max_width = grid_width - start_x
    # Limite máximo de largura dentro da altura válida
    for dy in range(max_height):
        row_width = 0
        for x in range(start_x, grid_width):
            if filling[start_y + dy][x]:
                break
            row_width += 1
        max_width = min(max_width, row_width)

    return max_width, max_height


def fill_remaining_space(filling, images_folder, layout_data):
    grid_width = len(filling[0])
    grid_height = len(filling)
    
    images = [f for f in os.listdir(images_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    random.shuffle(images)  # Embaralha para evitar repetição previsível

    # Pré-carrega proporções das imagens
    image_ratios = []
    for image_name in images:
        image_path = os.path.join(images_folder, image_name)
        try:
            with Image.open(image_path) as img:
                w, h = img.size
                ratio = round(w / h, 2) if h != 0 else 1
                image_ratios.append((image_name, ratio))
        except:
            continue

    for y in range(grid_height):
        for x in range(grid_width):
            if not filling[y][x]:
                w_max, h_max = get_largest_free_block(filling, x, y, grid_width, grid_height)
                if w_max == 0 or h_max == 0:
                    continue

                block_ratio = round(w_max / h_max, 2) if h_max != 0 else 1

                # Busca imagens com proporção parecida
                matching_images = [name for name, r in image_ratios if abs(r - block_ratio) < 0.2]

                if not matching_images:
                    matching_images = [name for name, r in image_ratios]  # Usa qualquer imagem

                image_name = random.choice(matching_images)
                x1, y1 = w_max, h_max

                # Marca espaço
                for dy in range(y1):
                    for dx in range(x1):
                        filling[y + dy][x + dx] = True

                layout_data.append(f"{x}|{y}|{x1}|{y1}|{image_name}")


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
    filling = [[False for _ in range(grid_width)] for _ in range(n_grid_y_init)]
    
    images = [f for f in os.listdir(images_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    layout_data = []

    y = 0  # Começa na primeira linha
    random.shuffle(images)
    for image_name in images:
        image_path = os.path.join(images_folder, image_name)
        with Image.open(image_path) as img:
            width, height = img.size
            x1 = round(width / pixel_factor_for_grid)
            y1 = round(height / pixel_factor_for_grid)

            # Redimensiona se exceder o tamanho máximo
            if x1 > grid_maximum_size and x1 >= y1:
                scale = grid_maximum_size / x1
                x1 = grid_maximum_size
                y1 = round(y1 * scale)
            elif y1 > grid_maximum_size and y1 > x1:
                scale = grid_maximum_size / y1
                y1 = grid_maximum_size
                x1 = round(x1 * scale)

            # Se for proporcional tipo 1x2, dobra as dimensões
            if y1 == x1 * 2 or y1 * 2 == x1:
                x1 *= 2
                y1 *= 2

            # Garante ao menos 1x1
            x1 = max(1, x1)
            y1 = max(1, y1)



            x = 0  # Sempre começa a busca do início da linha
            print(f"\n--- Posicionando imagem: {image_name} ---")
            print(f"Tamanho desejado na grade: {x1}x{y1}")
            print(f"Posição inicial tentativa: x={x}, y={y}")

            # Encontra a primeira posição livre suficiente
            while True:
                #print(f"[TRY] x={x}, y={y}, x+x1={x + x1} (limit={grid_width}), linhas={len(filling)}")
                if random.random() < 0.4:
                    x += 1
                if x + x1 > grid_width:
                    #print(f"    -> ULTRAPASSOU largura (x + x1 = {x + x1} > {grid_width}), pulando para próxima linha")
                    x = 0
                    y += 1
                    #print(f"    -> Novo y = {y}")
                    while y + y1 > len(filling):
                        filling.append([False for _ in range(grid_width)])
                        print(f"    -> Expandindo filling: agora tem {len(filling)} linhas")
                elif is_area_free(filling, x, y, x1, y1, grid_width):
                    #print(f"    -> ÁREA LIVRE em x={x}, y={y}, reservando espaço {x1}x{y1}")
                    break
                else:
                    #print(f"    -> Área OCUPADA em x={x}, y={y}, tentando próximo x")
                    x += 1
                #time.sleep(2)                





            print("outgrid", x, y)

            # Marca a área ocupada na matriz de preenchimento
            for dy in range(y1):
                for dx in range(x1):
                    filling[y + dy][x + dx] = True

            # Adiciona a entrada ao layout
            layout_data.append(f"{x}|{y}|{x1}|{y1}|{image_name}")

            # Atualiza x para a próxima imagem (não usado, mas mantido por clareza kkkkk)
            x += x1
    fill_remaining_space(filling, images_folder, layout_data)

    # Salva o layout no arquivo
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
