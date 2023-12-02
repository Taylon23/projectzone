$(document).ready(function () {
    var horariosInicialmenteDesabilitados = [];

    // Preenche a lista com os horários inicialmente desabilitados
    $('input[name="horario"]:disabled').each(function() {
        horariosInicialmenteDesabilitados.push($(this).val());
    });
    
    function atualizarHorariosDisponiveis() {
        var projetorId = $('#id_projetor').val();
        var data = $('#id_data').val();

        if (projetorId && data) {
            var url = `/reservas/get_horarios_disponiveis/${projetorId}/${data}/`;
            $.ajax({
                url: url,
                dataType: 'json',
                success: function (data) {
                    var horariosDisponiveis = data.horarios;

                    // Desabilita todos os horários
                    $('input[name="horario"]').prop('disabled', true);

                    // Habilita os horários disponíveis
                    horariosDisponiveis.forEach(function (horario) {
                        $('input[name="horario"][value="' + horario[0] + '"]').prop('disabled', false);
                    });

                    // Desabilita os horários inicialmente desabilitados novamente
                    horariosInicialmenteDesabilitados.forEach(function (horario) {
                        $('input[name="horario"][value="' + horario + '"]').prop('disabled', true);
                    });
                }
            });
        }
    }

    $('#id_projetor').change(function () {
        atualizarHorariosDisponiveis();
    });

    $('#id_data').change(function () {
        atualizarHorariosDisponiveis();
    });

    // Chama a função inicialmente para configurar os horários disponíveis
    atualizarHorariosDisponiveis();
});
