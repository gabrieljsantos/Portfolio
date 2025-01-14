window.onload = function() {
    const container = document.getElementById("grid-container");

    // Simulando o carregamento das imagens (como se estivessem sendo lidas de uma pasta)
    const imageNames = [
        "1 (1).png", "1 (2).png", "1 (3).png", "004.jpeg", "005.jpeg", "006.jpeg"
    ];

    imageNames.forEach((imageName) => {
        const img = new Image();
        img.src = `./images/${imageName}`;  // Caminho para as imagens (ajuste conforme a localização real)

        img.onload = function() {
            const aspectRatio = img.width / img.height;
            const gridItem = document.createElement("div");
            gridItem.classList.add("grid-item");

            let gridRowSpan = 1;
            let gridColumnSpan = 1;

            // Ajustando a proporção para definir quantas regiões a imagem ocupa
            if (aspectRatio > 1) {
                // Imagem larga: ocupa duas regiões na vertical
                gridColumnSpan = 2;
            } else if (aspectRatio < 1) {
                // Imagem alta: ocupa duas regiões na horizontal
                gridRowSpan = 2;
            }

            gridItem.style.gridRowEnd = `span ${gridRowSpan}`;
            gridItem.style.gridColumnEnd = `span ${gridColumnSpan}`;

            const imageElement = document.createElement("img");
            imageElement.src = img.src;
            gridItem.appendChild(imageElement);

            container.appendChild(gridItem);
        };
    });
};
