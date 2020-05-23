$(document).ready(function(){
    
    $("#parishLabel").hide()
    $("#parishInput").hide()

    $('#prayerInput').click(function(){

        if($(this).prop("checked") == true){

            $("#parishLabel").show()
            $("#parishInput").show()

        }

        else if($(this).prop("checked") == false){

            $("#parishLabel").hide()
            $("#parishInput").hide()

        }

    });
    function submit(){
        $("#signupForm").submit()
    }
});