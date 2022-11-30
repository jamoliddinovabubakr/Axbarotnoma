function validateEmail(email) {
    var regex = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    return regex.test(email);
}

$('body').on('click', '.registerBtn', function (e) {
    e.preventDefault();

        $.ajax({
            method: "POST",
            url: '/profile/register/',
            data: $('.registerForm').serialize(),
            success: function (response) {
                if(response.message){
                    $('#registerFormError').html("<span class='text-danger text-center'>" + response.message +"</span>");
                } else {
                    window.location.href="/";
                } 
            },
        });


    function formValidate() {

        let lname = $('.last_name').val();
        let fname = $('.first_name').val();
        let mname = $('.middle_name').val();
        let username = $('.username').val();
        let email = $('.email').val();
        let password = $('.password1').val();
        let confirmPassword = $('.password2').val();



        var inputValue = new Array(lname, fname, mname, email, username, password, confirmPassword);

        var inputMessage = new Array("Surname", "Name", "Family Name", "Email", "Username", "Password", "ConfirmPassword");

        $('.text-danger').hide();

        if (inputValue[0] == "") {
            $('.last_name').after('<span class="text-danger"> Please enter your ' + inputMessage[0] + '</span>');
        }

        if (inputValue[1] == "") {
            $('.first_name').after('<span class="text-danger"> Please enter your ' + inputMessage[1] + '</span>');
        }

        if (inputValue[2] == "") {
            $('.middle_name').after('<span class="text-danger"> Please enter your ' + inputMessage[2] + '</span>');
        }

        if (inputValue[4] == "") {
            $('.username').after('<span class="text-danger"> Please enter your ' + inputMessage[4] + '</span>');
        }

        if (inputValue[3] == "") {
            $('.email').after('<span class="text-danger"> Please enter your ' + inputMessage[3] + '</span>');
        }
        else if (!validateEmail.test(email)) {
            $('.email').after('<span class="text-danger"> Please enter a valid email address</span>');
        }

        if (inputValue[5] == "") {
            $('.password1').after('<span class="text-danger"> Please enter your ' + inputMessage[5] + '</span>');
        }

        if (inputValue[6] == "") {
            $('.password2').after('<span class="text-danger"> Please enter your ' + inputMessage[6] + '</span>');
        }
    }
});


