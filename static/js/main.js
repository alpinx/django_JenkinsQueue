
    var append_increment = 0;
    var toggle = document.getElementById('checkbox');
    var toggleNumber;
    if(!toggle){
        toggleNumber = true;
    }else{
        toggleNumber= toggle.getAttribute('value');
    }
    var displayTable = function (){
        var toggle = document.getElementById('checkbox');
        var toggleNumber = toggle.getAttribute('value');;
        if(toggleNumber){
          $(".tablerow").each(function() {
              var cell = $.trim($(this).find("td:eq(0)").text());
              if (cell.length == 0){
                  $(this).addClass("nodisplay");
              }
          });
        }else{
            $(".tablerow").each(  function() {
                  $(this).removeClass("nodisplay");
              }
          );
        }
    }
    console.log(toggleNumber)

    var ajax_getTable = function () {
        $.ajax({
            type: "GET",
            url: "get_more_tables/",  // URL to your view that serves new info
            data: {'append_increment': append_increment}
        })
        .done(function(response) {
             $('#_appendHere').html(response);
             displayTable();
            append_increment += 1;
            jQuery('td:contains("already running")').each(function() {
              if( $(this).hasClass("highlight") )
                  $(this).addClass('blink_me');});
            jQuery('td:contains("already in queue")').each(function() {
              if( $(this).hasClass("highlight") )
                  $(this).addClass('blink_me');});
            jQuery('td:contains("running twice")').each(function() {
              if( $(this).hasClass("highlight") )
                  $(this).addClass('blink_me');});
            jQuery('td:contains("Duration is longer as 1 hour")').each(function() {
              if( $(this).hasClass("highlight") )
                  $(this).addClass('blink_me');});
        });
    }
    var append_increment2 = 0;

    var ajax_getBuilds = function () {
        $.ajax({
            type: "GET",
            url: "get_finished_builds/",  // URL to your view that serves new info
            data: {'append_increment2': append_increment2}
        })
        .done(function(response) {
             $('#_appendBuilds').html(response);
            append_increment2 += 1;

            jQuery('td:contains("FAILURE")').each(function() {
              if( $(this).hasClass("highlight") )
                  $(this).addClass('failure');
                  });
            jQuery('td:contains("SUCCESS")').each(function() {
              if( $(this).hasClass("highlight") )
                  $(this).addClass('success');
                  });


        });
    }
ajax_getTable();
ajax_getBuilds();
setInterval(ajax_getTable, 5000);
setInterval(ajax_getBuilds, 30000);