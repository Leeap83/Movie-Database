  $(document).ready(function(){
    $(".sidenav").sidenav({edge: "right"});
    $('.datepicker').datepicker({
        format: "dd mmmm, yyyy",
        yearRange: [1950,2025],
        showClearBtn: true,
        i18n: {
            done: "Select"
        }
    })
  });

  
