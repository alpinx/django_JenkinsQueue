
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
                  sortTable("queuetable1",1,0);
              }
          });
        }else{
            $(".tablerow").each(  function() {
                  $(this).removeClass("nodisplay");
                  sortTable("queuetable1",1,2);
              }
          );
        }
    }
    function sortTable(table,f,n){
		var rows = $('#'+table+' tbody  tr.tablerow').get();
	    rows.sort(function(a, b) {
		var A = getVal(a);
		var B = getVal(b);

		if(A < B) {
			return -1*f;
		}
		if(A > B) {
			return 1*f;
		}
		return 0;
	});

	function getVal(elm){
		var v = $(elm).children('td').eq(n).text().toUpperCase();
		if($.isNumeric(v)){
			v = parseInt(v,10);
		}
		return v;
	}

	$.each(rows, function(index, row) {
		$('#'+table+'').children('tbody').append(row);
	});
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
            findError();
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
    sortTable("queuetable2",1,0);

    var findError = (function() {
        var tableRows = $("#queuetable2 tbody tr.tablerow"); //find all the rows
        var tableRowsAR = $("#queuetable1 tbody tr.tablerow"); //find all the rows
        var AlreadyInQueue =  {};
        var Running =  {};
        var AlreadyRunning ={}

        var colorAQ = {};
        tableRows.each(function() {
            var rowValue = $(this).children(".srprofile").html(); if (rowValue!=""){
            if (AlreadyInQueue[rowValue]){
                colorAQ = AlreadyInQueue[rowValue];
              colorAQ.count++;
              colorAQ[colorAQ.count]=$(this).children(".srprofile");
            }else{
                 var colorAQ = {};
                colorAQ.count=1;
              colorAQ[colorAQ.count]=$(this).children(".srprofile");
              AlreadyInQueue[rowValue] = colorAQ;
            }}
        });
        var colorRT = {};
        tableRowsAR.each(function() {
            var rowValue = $(this).children(".srprofile").html(); if (rowValue!=""){
            if (Running[rowValue]){
                colorRT = Running[rowValue];
              colorRT.count++;
              colorRT[colorRT.count]=$(this).children(".srprofile");
            }else{
                 var color = {};
                color.count=1;
              color[color.count]=$(this).children(".srprofile");
              Running[rowValue] = color;
            }   }
        });

        tableRows.each(function() {
            var rowValue = $(this).children(".srprofile").html(); if (rowValue!=""){
            if (Running[rowValue]){
                var colorAR = {};
              colorAR.count=2;
              colorAR[colorAR.count]=$(this).children(".srprofile");
              AlreadyRunning[rowValue] = colorAR
            }else{
                 var color = {};
                color.count=1;
              color[color.count]=$(this).children(".srprofile");
              AlreadyRunning[rowValue] = color;
            }   }
        });
        console.log(AlreadyInQueue)
         console.log(Running)
          console.log(AlreadyRunning)
        Object.keys(AlreadyInQueue).forEach(function(key){
                if(AlreadyInQueue[key].count>1){
            for (var k in AlreadyInQueue[key]){
              if (AlreadyInQueue[key].hasOwnProperty(k)&&k!='count') {
                  AlreadyInQueue[key][k].append('      <-- already in queue!!!');
              }
            }
          }
        })
        Object.keys(Running).forEach(function(key){
                if(Running[key].count>1){
            for (var k in Running[key]){
              if (Running[key].hasOwnProperty(k)&&k!='count') {
                 Running[key][k].append('      <-- running twice!!!');
              }
            }
          }
        })
        Object.keys(AlreadyRunning).forEach(function(key){
                if(AlreadyRunning[key].count>1){
            for (var k in AlreadyRunning[key]){
              if (AlreadyRunning[key].hasOwnProperty(k)&&k!='count') {
                 AlreadyRunning[key][k].append('      <-- already running!!!');
              }
            }
          }
        })
        tableRowsAR.each(function() {
            var rowValue = $(this).children(".srprofile").html();
            if (rowValue!=""){
                var rowTime = $(this).children(".time").html();
              if(rowTime/60>60){
                $(this).children(".srprofile").append('   <-- Duration is longer as 1 hour!!!')
              }
            }} )
    });

ajax_getTable();
ajax_getBuilds();
sortTable("queuetable2",1,0);

setInterval(ajax_getTable, 5000);
setInterval(ajax_getBuilds, 30000);
