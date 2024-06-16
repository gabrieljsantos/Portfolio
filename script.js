// script.js
document.addEventListener('DOMContentLoaded', (event) => {
    const ball = document.querySelector('.ball');
    const ballSize = 20; // Tamanho da bolinha
    let x = 100; // Posição inicial x
    let y = 100; // Posição inicial y
    let dx = 2; // Velocidade x
    let dy = 2; // Velocidade y

    function moveBall() {
        const windowWidth = window.innerWidth;
        const windowHeight = window.innerHeight;

        // Atualiza a posição da bolinha
        x += dx;
        y += dy;

        // Detecta colisão com as bordas e inverte a direção
        if (x <= 0 || x + ballSize >= windowWidth) {
            dx = -dx;
        }
        if (y <= 0 || y + ballSize >= windowHeight) {
            dy = -dy;
        }

        // Aplica a nova posição à bolinha
        ball.style.transform = `translate(${x}px, ${y}px)`;

        // Chama a função novamente no próximo frame
        requestAnimationFrame(moveBall);
    }

    // Inicia o movimento da bolinha
    moveBall();
});
