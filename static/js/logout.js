document.addEventListener('DOMContentLoaded', function() {
    var logoutLink = document.getElementById('logout');
    if (logoutLink) {
        logoutLink.addEventListener('click', function(e) {
            e.preventDefault();
            var confirmed = confirm('Tem certeza de que deseja sair?');
            if (confirmed) {
                window.location.href = "/accounts/logout";
            }
        });
    }
});