function validateEmail(email) {
    var regex = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    return regex.test(email);
}

function formValidate(array) {

    let is_validRForm = true;

    $('.text-danger').hide();

    for (let index = 0; index < array.length; index++) {
        let key = array[index].key;
        let value = array[index].value;
        let message = array[index].message;


        if (key == 'email') {
            if (value == "") {
                $('.' + key).after('<span class="text-danger"> Please enter your email </span>');
                is_validRForm = false;
            } else if (!validateEmail(value)) {
                $('.' + key).after('<span class="text-danger"> Please enter a valid email address</span>');
                is_validRForm = false;
            }
        }

        if (value == "") {
            $('.' + key).after('<span class="text-danger text-small"> Please enter your ' + message + '</span>');
            is_validRForm = false;
        }

    }

    return is_validRForm
}


$('body').on('click', '.registerBtn', function (e) {
    e.preventDefault();

    let lname = $('.last_name').val();
    let fname = $('.first_name').val();
    let mname = $('.middle_name').val();
    let username = $('.username').val();
    let email = $('.email').val();
    let password = $('.password1').val();
    let confirmPassword = $('.password2').val();

    let data = [{key: 'last_name', value: lname, message: "surname"},
        {key: 'first_name', value: fname, message: "name"},
        {key: 'middle_name', value: mname, message: "middle name"},
        {key: 'username', value: username, message: "username"},
        {key: 'password1', value: password, message: "password"},
        {key: 'password2', value: confirmPassword, message: "confirmpassword"},
        {key: 'email', value: email, message: ""}];

    let is_valid_registerForm = formValidate(data);

    if (is_valid_registerForm) {
        $.ajax({
            method: "POST",
            url: '/profile/register/',
            data: $('.registerForm').serialize(),
            success: function (response) {
                if (response.message) {
                    $('#registerFormError').html("<span class='text-danger text-center'>" + response.message + "</span>");
                } else {
                    window.location.reload();
                }
            },
        });
    }
});

$('body').on('click', '.loginBtn', function (e) {
    e.preventDefault();

    let is_valid_form = formValidateLogin();
    if (is_valid_form) {
        $.ajax({
            method: "POST",
            url: '/profile/login/',
            data: $('.loginForm').serialize(),
            success: function (response) {
                if (response.message) {
                    $('#loginFormError').html("<span class='text-danger text-center'>" + response.message + "</span>");
                } else {
                    window.location.reload();
                }
            },
        });
    }

    function formValidateLogin() {

        let username = $('.usernameLogin').val();
        let password = $('.passwordLogin').val();

        let inputValue = new Array(username, password);

        let inputMessage = new Array("Username", "Password");

        let is_valid = true;

        $('.text-danger').hide();

        if (inputValue[0] == "") {
            $('.usernameLogin').after('<span class="text-danger"> Please enter your ' + inputMessage[0] + '</span>');
            is_valid = false;
        }

        if (inputValue[1] == "") {
            $('.passwordLogin').after('<span class="text-danger"> Please enter your ' + inputMessage[1] + '</span>');
            is_valid = false
        }

        return is_valid;
    }
});


$('body').on('submit', '.editProfileForm', function (e) {
    e.preventDefault();

    let last_name = $('.last_name').val();
    let first_name = $('.first_name').val();
    let middle_name = $('.middle_name').val();
    let username = $('.username').val();
    let email = $('.email').val();
    let birthday = $('.birthday').val();
    let region = $('.region').val();
    let gender = $('.gender').val();
    let phone = $('.phone').val();
    let pser = $('.pser').val();
    let pnum = $('.pnum').val();
    let work = $('.work').val();
    // let roles = $("#roles :selected").map((_, e) => e.value).get();

    let dataEdit = [{key: 'last_name', value: last_name, message: "surname"},
        {key: 'first_name', value: first_name, message: "name"},
        {key: 'middle_name', value: middle_name, message: "middle name"},
        {key: 'username', value: username, message: "username"},
        {key: 'email', value: email, message: ""},
        {key: 'birthday', value: birthday, message: "birthday"},
        {key: 'region', value: region, message: "region"},
        {key: 'gender', value: gender, message: "gender"},
        {key: 'phone', value: phone, message: "phone"},
        {key: 'pser', value: pser, message: "pser"},
        {key: 'pnum', value: pnum, message: "pnum"},
        {key: 'work', value: work, message: "work"}];


    let is_valid_form = formValidate(dataEdit);

    let formData = new FormData(this);

    if (is_valid_form) {
        $.ajax({
            method: "POST",
            url: '/profile/edit_profile/',
            data: formData,
            contentType: false,
            processData: false,
            success: function (response) {
                swal({
                    title: response.message,
                    timer: 1500,
                });
                if (response.status) {
                    window.location.reload();
                }
            },
        });
    }
});