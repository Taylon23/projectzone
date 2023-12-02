document.addEventListener('DOMContentLoaded', function () {
    const menuToggle = document.getElementById('menu-toggle');
    const menuTopo = document.getElementById('menu-topo');

    menuToggle.addEventListener('click', function (event) {
        event.stopPropagation(); // Evita que o evento de clique se propague para o documento
        menuTopo.classList.toggle('active');
    });

    document.addEventListener('click', function () {
        if (menuTopo.classList.contains('active')) {
            menuTopo.classList.remove('active');
        }
    });

    menuTopo.addEventListener('click', function (event) {
        event.stopPropagation(); // Evita que o evento de clique no menu se propague para o documento
    });
});