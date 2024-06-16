document.getElementById('hover-link').addEventListener('mouseover', function() {
    document.body.classList.add('background-hover');
});
document.getElementById('hover-link').addEventListener('mouseout', function() {
    document.body.classList.remove('background-hover');
});
