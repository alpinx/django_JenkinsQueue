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
          }
      });
    }else{
    	$(".tablerow").each(  function() {
              $(this).removeClass("nodisplay");
          }
      );
    }
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
