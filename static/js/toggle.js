var toggle = document.getElementById('checkbox');
var toggleNumber;
if(!toggle){
    toggleNumber = true;
}
toggleNumber= toggle.getAttribute('value');
toggle.addEventListener('click', function() {
    toggleNumber = !toggleNumber;
    toggle.value = toggleNumber;
    console.log(toggleNumber)
    ajax_getTable();
});
