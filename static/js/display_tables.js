$(document).ready(function () {
    const $myForm = $('.create_author_form'); // select form class
    $myForm.submit(function (event) {
        event.preventDefault();

        const $formData = $myForm.serialize(); // get all data from form which will be submitted to database
        const $thisURL = $myForm.attr('data-url') || window.location.href; // data-url is attribute in form
        $.ajax({
            type: 'POST',
            url: $thisURL,
            data: $formData,
            success: handleSuccess,
            error: handleError,
        });

        function handleSuccess(data) {
            $myForm[0].reset();
            $('#add_author_modal').click();
            $('#add-author-notif').click();
        }

        function handleError(ThrowError) {
            console.log('error');
            console.log(ThrowError);
        }
    });
});