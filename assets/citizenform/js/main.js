
(function ($) {
    "use strict";


    /*==================================================================
    [ Focus Contact2 ]*/
    $('.input100').each(function(){
        $(this).on('blur', function(){
            if($(this).val().trim() != "") {
                $(this).addClass('has-val');
            }
            else {
                $(this).removeClass('has-val');
            }
        })    
    })
  
  
    /*==================================================================
    [ Validate ]*/
    var name = $('.validate-input input[name="name"]');
    var adhar = $('.validate-input input[name="Aadhar No"]');
    var message = $('.validate-input textarea[name="from"]');
   
    var adharcard = /^\d{12}$/;
    var adharsixteendigit = /^\d{16}$/;
    var gender = $('.validate-input option[name="gender"]');
    var migrate = $('.validate-input option[name="migrated"]');
 
 

    $('.validate-form').on('submit',function(){
        var check = true;

        if($(name).val().trim() == ''){
            showValidate(name);
            check=false;
        }


        if($(adhar).val() == ''){
            showValidate(adhar);
            check=false
        }
        if($(gender).val()=='')
            {
                showValidate(gender);
                check=false;
            }
        if($(migrate)=='Choose migrated')
            {
                showValidate(migrate);
                check=false;
            }
        if($(message).val().trim() == ''){
            showValidate(message);
            
            check=false;
        }

        return check;
    });


    $('.validate-form .input100').each(function(){
        $(this).focus(function(){
           hideValidate(this);
       });
    });

    function showValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).addClass('alert-validate');
    }

    function hideValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).removeClass('alert-validate');
    }
    
    

})(jQuery);
