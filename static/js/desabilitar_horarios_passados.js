var agora = new Date();
var hora = agora.getHours();
var minutos = agora.getMinutes();

// Verificar qual é o horário atual
var horarioAtual = null;
if (hora >= 7 && hora < 8) {
    if (hora == 7 && minutos >= 35) {
        horarioAtual = 1;
    } else {
        horarioAtual = 0;
    }
} else if (hora >= 8 && hora < 9) {
    if (hora == 8 && minutos < 25) {
        horarioAtual = 1;
    } else {
        horarioAtual = 2;
    }
} else if (hora >= 9 && hora < 10) {
    if (hora == 9 && minutos < 10) {
        horarioAtual = 2;
    } else {
        horarioAtual = 3;
    }
} else if (hora >= 10 && hora < 11) {
    if (hora == 10 && minutos < 20) {
        horarioAtual = 3;
    } else {
        horarioAtual = 4;
    }
} else if (hora >= 11 && hora < 13) {
    if (hora == 11 && minutos < 10) {
        horarioAtual = 4;
    } else {
        horarioAtual = 5;
    }
} else if (hora >= 13 && hora < 14) {
    if (hora == 13 && minutos < 30) {
        horarioAtual = 5;
    } else {
        horarioAtual = 6;
    }
} else if (hora >= 14 && hora < 15) {
    if (hora == 14 && minutos < 20) {
        horarioAtual = 6;
    } else {
        horarioAtual = 7;
    }
} else if (hora >= 15 && hora < 16) {
    if (hora == 15 && minutos < 5) {
        horarioAtual = 7;
    } else {
        horarioAtual = 8;
    }
} else if (hora >= 16 && hora < 10) {
    if (hora == 16 && minutos < 10) {
        horarioAtual = 8;
    } else {
        horarioAtual = 9;
    }
}


// Desabilitar as opções de horário anteriores ao horário atual
if (horarioAtual != null) {
    var checkboxes = document.querySelectorAll('[id^="id_horario_"]');
    for (var i = 0; i < horarioAtual; i++) {
        var checkbox = document.querySelector('#id_horario_' + i);
        if (checkbox) {
            checkbox.disabled = true;
        }
    }
} else {
    // Se for antes do primeiro horário ou depois do último horário, desabilitar todos os horários
    var checkboxes = document.querySelectorAll('[id^="id_horario_"]');
    for (var i = 0; i < checkboxes.length; i++) {
        checkboxes[i].disabled = true;
    }
}