$(document).ready(function() {
    $("#startPop").on('click', function(){
        $("#startPop").text("yay!")
        $.ajax({
            type: "POST",
            url: "apps/py/grooveshark.py",
            data: {}
            }).done(function( o ) {
                alert("Playing")
            });
    });
});
