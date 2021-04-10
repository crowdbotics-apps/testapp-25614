
(function($) {
  "use strict"; // Start of use strict
  $(function(){
   $(document).ready(function() {
     var form = $("#changelist-search");
     $('<input>').attr({
        type: 'hidden',
        id: 'foo',
        name: 'bar'
     }).appendTo(form);

  })

  })(jQuery); // End of use strict
