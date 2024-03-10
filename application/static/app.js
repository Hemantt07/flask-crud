const ajaxFormSubmit = (form) => {
    $('#loaderWrap').css({display: "flex"})
    $.ajax({
        url: form.attr('action'),
        method: form.attr('method'),
        data: form.serialize(),
        success: function(response) {
            $('#loaderWrap').css({display: "none"})
            console.log(response);
            form[0].reset()
        },
        error: function(xhr, status, error) {
            $('#loaderWrap').css({display: "none"})
            console.error(error);
        }
    });
}

$( '#openai-form' ).on( 'submit', function(e){
    e.preventDefault();
    $('#loaderWrap').css({display: "flex"})
    const action = $(this).attr('action')
    const prompt = $('#prompt').val()
    if ( prompt == '' ) {
        $('#prompt').addClass('is-invalid')
        return
    } else {
        $.ajax({
            url: action,
            method: 'post',
            data: {
                prompt: prompt
            },
            success:function(response){
                $('#loaderWrap').css({display: "none"})
                $('#openai-form').siblings('#output').html( '<p class="p-3 bg-light">'+ response.generated_text +'</p>' )
            },
            error: function(error){
                $('#loaderWrap').css({display: "none"})
                console.log(error)
            }
        })
    }
} )

if ( $('#openai-form').length == 0 ) {
 
    $('form button[type-submit]').on( 'click', function(e){
        const form = $(this).closest('form')
        e.preventDefault()
        $('#loaderWrap').css({display: "flex"})
        var formHasError = false;
        $(this).find('input').each(function(e){
            if ($(this).val() == '') {
                $(this).addClass( 'is-invalid' )
                console.log($(this))
                formHasError = true
            } else {        
                $(this).removeClass( 'is-invalid' )
            }    
        })
        var emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;

        $('input[type=email]').each( function(){
            if ( !emailPattern.test($(this).val())  ) {
                $(this).addClass('is-invalid')
                if ( $(this).siblings('p.text-danger').length == 0 ) {
                    $(this).parent().append('<p class="text-danger">This is not a valid email</p>')
                }
                formHasError = true
            }
        } )

        if ( $('#password').length != 0 && $('#confirmPassword').length != 0 ) {
            if ( $('#password').val() !== $('#confirmPassword').val() ) {
                $('#password').addClass('is-invalid')
                if ( $('#password').siblings('p.text-danger').length == 0 ) {
                    $('#password').parent().append('<p class="text-danger">Passwords do not match</p>')
                }
                if ( $('#confirmPassword').siblings('p.text-danger').length == 0 ) {
                    $('#confirmPassword').parent().append('<p class="text-danger">Passwords do not match</p>')
                }
                formHasError = true
            } else {
                $('#password').removeClass('is-invalid')
                $('#confirmPassword').removeClass('is-invalid')
            }
        }

        if (!formHasError) {
            $('#loaderWrap').css({display: "none"})
            form.submit()
        }
    } )
   
}