// script.js
// Função para carregar os dados de um arquivo de texto
async function loadData(filePath) {
    const response = await fetch(filePath);
    const data = await response.text();
    return data.split('\n').map(line => line.trim());
}

// Função para gerar a seção de redes sociais
async function generateNetworks() {
    const networks = await loadData('networks.txt');
    const networksContainer = document.getElementById('networks-images');

    networks.forEach(line => {
        const [name, link, image] = line.split('|');
        const anchor = document.createElement('a');
        anchor.href = link;
        anchor.target = '_blank';

        const img = document.createElement('img');
        img.src = image;
        img.alt = `${name} de Gabriel J Santos`;

        anchor.appendChild(img);
        networksContainer.appendChild(anchor);
    });
}

// Função para gerar a seção de habilidades
async function generateSkills() {
    const skills = await loadData('skills.txt');
    const skillsContainer = document.getElementById('skills-gallery');

    skills.forEach(line => {
        const [name, image, link] = line.split('|');
        const galleryItem = document.createElement('div');
        galleryItem.classList.add('gallery-item');

        const img = document.createElement('img');
        img.src = image;
        img.alt = name;

        const overlay = document.createElement('div');
        overlay.classList.add('overlay');
        overlay.textContent = name;

        galleryItem.appendChild(img);
        galleryItem.appendChild(overlay);

        if (link) {
            const anchor = document.createElement('a');
            anchor.href = link;
            anchor.target = '_blank';
            anchor.appendChild(galleryItem);
            skillsContainer.appendChild(anchor);
        } else {
            skillsContainer.appendChild(galleryItem);
        }
    });
}

// Carregar as redes sociais e as habilidades quando a página carregar
window.onload = async () => {
    await generateNetworks();
    await generateSkills();
};
