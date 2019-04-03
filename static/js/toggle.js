var toggle = document.getElementById('checkbox');
var toggleNumber;
if(!toggle){
    toggleNumber = true;
}
var displayTable = function (){
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
toggleNumber= toggle.getAttribute('value');
displayTable();
console.log(toggleNumber)
toggle.addEventListener('click', function() {
    toggleNumber = !toggleNumber;
    toggle.value = toggleNumber;   
    displayTable();
    console.log(toggleNumber)
});
sortTable("queuetable2",1,0);