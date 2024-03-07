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


// $('#add-post-form').on( 'submit', function(e) {
//     e.preventDefault();
//     const form = $(this);
//     ajaxFormSubmit(form)
// } )

$(document).ready( function () {
    // $('#myTable').DataTable();
} );