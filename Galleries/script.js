

const sizeGrid = 100; // Grid size in pixels
const spacing = 0; // Spacing between grid cells in pixels
const folder = './3D_imgs/'; // Path to the folder containing images

async function fetchLayoutData(filePath) {
    try {
        const response = await fetch(filePath);
        const text = await response.text();
        return text.split('\n').filter(line => line.trim()).map(line => {
            const [x, y, x1, y1, path] = line.split('|');
            return {
                x: parseInt(x, 10),
                y: parseInt(y, 10),
                width: parseInt(x1, 10) * sizeGrid,
                height: parseInt(y1, 10) * sizeGrid,
                path: path.trim()
            };
        });
    } catch (error) {
        console.error('Error fetching layout data:', error);
        return [];
    }
}

function renderImages(layoutData) {
    const container = document.getElementById('container');
    const overlay = document.getElementById('overlay');
    const popupImage = document.getElementById('popupImage');
    const closeButton = document.getElementById('closeButton');

    // Show image in popup
    function showPopup(src) {
        popupImage.src = src;
        overlay.classList.remove('hidden');
    }

    // Hide popup
    function hidePopup() {
        overlay.classList.add('hidden');
        popupImage.src = '';
    }

    layoutData.forEach(({ x, y, width, height, path }) => {
        const imgDiv = document.createElement('div');
        imgDiv.className = 'image';
        imgDiv.style.left = `${(x * (sizeGrid+ spacing)) + spacing}px`; // Position on X-axis
        imgDiv.style.top = `${(y * (sizeGrid+ spacing)) + spacing}px`;  // Position on Y-axis
        imgDiv.style.width = `${width}px`;      // Set width
        imgDiv.style.height = `${height}px`;    // Set height

        const img = document.createElement('img');
        img.src = folder + path;
        img.alt = `Image: ${path}`;

        // Add click event to show the popup
        img.addEventListener('click', () => showPopup(img.src));

        imgDiv.appendChild(img);
        container.appendChild(imgDiv);
    });

    // Attach event to close button
    closeButton.addEventListener('click', hidePopup);

    // Close the popup when clicking outside the image
    overlay.addEventListener('click', (event) => {
        if (event.target === overlay) hidePopup();
    });
}

async function init() {
    const layoutData = await fetchLayoutData('layout.inf');
    renderImages(layoutData);
}

window.onload = init;
