(function($) {
  "use strict"; // Start of use strict
  $(function(){
   $(document).ready(function() {
    $('#id_result').bind('change', type_change);
   })
  })

  function type_change() {
   var result =  $('#id_result').val();

   if (result === 'not_detected') {
      $('#id_iterpretation').val('SARS-CoV-2 was not detected in your sample.')
   } else if (result === 'detected') {
      $('#id_iterpretation').val('SARS-CoV-2 was detected in your sample.')
   } else {
      $('#id_iterpretation').val('')
   }
  }
  })(jQuery); // End of use strict
