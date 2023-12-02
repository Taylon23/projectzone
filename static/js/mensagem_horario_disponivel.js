$(document).ready(function () {
    // Define a hora desejada (no formato de 24 horas)
    var horaDesejada = 16;  // Exemplo: 16 representa as 4:00 PM

    // Obtem a hora atual
    var agora = new Date();
    var horaAtual = agora.getHours();

    // Obtem o elemento de mensagem pelo ID
    var mensagemElemento = $('#mensagem-horario');

    // Verifica se a hora atual é maior que a hora desejada
    if (horaAtual > horaDesejada || horaAtual < 7) {
        // A hora atual é maior que a hora desejada
        // Atualiza a mensagem personalizada
        mensagemElemento.text('Desculpe, não há mais  horários disponíveis');
    }
});