$(document).ready(function () {
  function atualizarTurmasPorCurso() {
      var cursoId = $('#id_curso').val();

      if (cursoId) {
          var url = `/reservas/get_turmas/${cursoId}/`;
          $.ajax({
              url: url,
              dataType: 'json',
              success: function (data) {
                  var turmaCheckboxContainer = $('#id_turmas_container');
                  turmaCheckboxContainer.empty();  // Limpar checkboxes existentes

                  data.forEach(function (turma) {
                      var label = $('<label>');
                      var checkbox = $('<input>').attr({
                          type: 'checkbox',
                          name: 'turmas',
                          value: turma.id
                      });
                      label.append(checkbox, ' ' + turma.turma);
                      turmaCheckboxContainer.append(label);
                  });
              }
          });
      }
  }

  $('#id_curso').change(function () {
      atualizarTurmasPorCurso();
  });

  atualizarTurmasPorCurso();
});
