// USER DASHBOARD

$('body').on('click', '.create_articleFileBtn', function (e) {
    e.preventDefault();

    let url = $(this).data('url');

    $.ajax({
        type: 'GET',
        url: url,
        success: function (response) {
            $('#edit_author_div').html(response);
            $('#create_articleFile_modal').modal('show');
        },
        error: function (error) {
            console.log(error);
        }
    });

});


$('body').on('click', '.edit-author', function (e) {
    e.preventDefault();

    let url = $(this).data('url');

    $.ajax({
        type: 'GET',
        url: url,
        success: function (response) {
            $('#edit_author_div').html(response);
            $('#edit-author-modal').modal('show');
        },
        error: function (error) {
            console.log(error);
        }
    });

});

$('body').on('click', '.remove-author', function (e) {
    e.preventDefault();

    let url = $(this).data('url');

    $.ajax({
        type: 'GET',
        url: url,
        success: function (response) {
            $('#edit_author_div').html(response);
            $('#removeAuthor').modal('show');
        },
        error: function (error) {
            console.log(error);
        }
    });

});

$('body').on('submit', '.edit-author-form', function (e) {
    e.preventDefault();
    const $myForm = $('.edit-author-form');

    const $formData = $myForm.serialize();
    const $thisURL = $myForm.attr('data-url')

    $.ajax({
        type: 'POST',
        url: $thisURL,
        data: $formData,
        success: function (response) {
            console.log(response);
            if (response.result) {
                swal({
                    title: response.message,
                    timer: 2000,
                });
            } else {
                alert(response.message);
            }
            $('#edit-author-modal').modal('hide');
        },
        error: function (error) {
            console.log(error);
        }
    });

    return false;
});
$('body').on('click', '.create_article_btn', function (e) {
    e.preventDefault();

    let url = $('.create_article_btn').data('url');

    $.ajax({
        type: 'GET',
        url: url,
        success: function (response) {
            $('#create_article_div').html(response);
            $('#create_article_modal').modal('show');
        },
        error: function (error) {
            console.log("Xatolik");
            console.log(error);
        }
    });
});

$('body').on('click', '.authorWrite-message-btn', function (e) {
    e.preventDefault();
    const url = $(this).data('url');

    $.ajax({
        type: 'GET',
        url: url,
        success: function (response) {
            $('#write_message_div_form').html(response);
            $('#send-message-modal').modal('show');

        },
        error: function (error) {
            console.log("Xatolik");
            console.log(error);
        }
    });

    return false;
});

$('body').on('click', '.view_message_btn', function (e) {
    e.preventDefault();
    let id = $(this).data('id');
    let url = $('#view-article-messages-by-author_' + id).data('url');

    $.ajax({
        type: "GET",
        url: url,
        success: function (response) {
            if (response.is_visible_comment) {
                $('#MessageBoxAuthor').css("display", "block");

                $('#article_title').text(response.article_title);
                $('#user_chat_body').empty();

                for (let item of response.notifications) {

                    let time_tz = new Date(item.created_at);
                    let time_string = time_tz.toLocaleString();

                    if (response.current_user_id === item.from_user__id) {

                        let temp1 = `<div class="widget-chat-item right">
                                                        <div class="widget-chat-info">
                                                            <div class="widget-chat-info-container">
                                                                <div class="widget-chat-name text-indigo">`
                            + item.from_user__email +
                            `</div>
                                                                <div class="widget-chat-message">` + `<i style="color: #0a6aa1">(${item.to_user__email}).</i>`
                            + item.message +
                            `</div>
                                                                <div class="widget-chat-time">` + time_string + `</div>
                                                                 <br><br><div class="widget-chat-ansewer"></div>
                                                            </div>
                                                        </div>
                                                    </div>`;

                        $('#user_chat_body').append(temp1);
                    }

                    if (response.current_user_id === item.to_user__id) {

                        let temp2 = `<div class="widget-chat-item left">
                                                        <div class="widget-chat-info">
                                                            <div class="widget-chat-info-container">
                                                                <div class="widget-chat-name text-indigo">`
                            + item.from_user__email +
                            `</div>
                                                                <div class="widget-chat-message">` + `<i style="color: #0a6aa1">(${item.to_user__email}).</i>`
                            + item.message +
                            `</div>
                                                                <div class="widget-chat-time">` + time_string + `</div>
                                                                <br><div class="widget-chat-ansewer">
                                                                    <button type="button" data-url="${response.url}${id}/${item.from_user__id}/" class="btn btn-white btn-sm authorWrite-message-btn">Ansewer</button>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </div>`;

                        $('#user_chat_body').append(temp2);
                    }
                }

            } else {
                swal({
                    title: response.message,
                    timer: 3000,
                });
            }

        },
        error: function (response) {
            console.log(response);
        }
    });

    return false;
});

$('body').on('click', '.edit_article_btn', function (e) {
    e.preventDefault();

    let url = $(this).data('url');

    $.ajax({
        type: 'GET',
        url: url,
        success: function () {
            window.location.href = url;
        },
        error: function (error) {
            console.log("Xatolik");
            console.log(error);
        }
    });
});

$('body').on('click', '.remove_article_btn', function (e) {
    e.preventDefault();

    let url = $(this).data('url');

    $.ajax({
        type: 'GET',
        url: url,
        success: function (response) {
            $('#create_article_div').html(response);
            $('#delete_article_modal').modal('show');

        },
        error: function (error) {
            console.log("Xatolik");
            console.log(error);
        }
    });
});

$('body').on('submit', '.update_article_form', function (e) {
    e.preventDefault();
    const $myForm = $('.update_article_form')
    const $formData = $myForm.serialize();
    const $thisURL = $myForm.attr('data-url')

    let title = $('.title').val();
    let title_en = $('.title_en').val();


    let data = [
        {key: 'title', value: title, message: "title"},
    ];

    let is_valid_editArticleForm = formValidate(data);

    if (is_valid_editArticleForm) {

        $.ajax({
            type: "POST",
            url: $thisURL,
            data: $formData,
            success: function (response) {
                $('#edit_article_form_error').empty();
                if (response.result) {
                    $('#edit_article_form_error').html(`<div class="alert alert-success forshadow" style="text-align: center">${response.message}</div>`);
                } else {
                    $('#edit_article_form_error').html(`<div class="alert alert-danger forshadow" style="text-align: center">${response.message}</div>`);
                }
            },
            error: function (error) {
                console.log(error);
            }
        });

    } else {
        swal({
            title: "Iltimos formani toliq to'ldiring!",
            timer: 3000
        });
    }
});

$('body').on('click', '.view_user_btn', function (e) {
    e.preventDefault();

    let url = $(this).data('url');

    $.ajax({
        type: 'GET',
        url: url,
        success: function (response) {
            $('#show_res').html(response);
            $('#view_user_modal').modal('show');
        },
        error: function (error) {
            console.log(error);
        }
    });
});


$('body').on('click', '.edit_user_btn', function (e) {
    e.preventDefault();

    let url = $(this).data('url');

    $.ajax({
        type: 'GET',
        url: url,
        success: function (response) {
            $('#show_res').html(response);
            $('#edit_user_modal').modal('show');
        },
        error: function (error) {
            console.log(error);
        }
    });
});

$('body').on('click', '.edit_user_btn_save', function (e) {
    e.preventDefault();

    let csrftoken = getCookie('csrftoken');
    let url = $('#choose_role_form').data('url');

    let selected = [];
    $('#widget-todolist-body-role input[type=checkbox]').each(function () {
        if ($(this).is(":checked")) {
            selected.push($(this).val());
        }
    });
    let n = selected.length;

    if (n === 0) {
        alert("Rol tanlanishi kerak!");
    }
    if (n >= 1) {
        $.ajax({
            type: "POST",
            url: url,
            data: {
                roles: selected,
                csrfmiddlewaretoken: csrftoken,
            },
            success: function (response) {
                swal({
                    title: response.message,
                    timer: 1500,
                });
            },
            error: function (error) {
                console.log(error);
            }
        });
    }
});

$('body').on('click', '.delete_user_btn', function (e) {
    e.preventDefault();

    let url = $(this).data('url');

    $.ajax({
        type: 'GET',
        url: url,
        success: function (response) {
            $('#show_res').html(response);
            $('#delete_user_modal').modal('show');
        },
        error: function (error) {
            console.log(error);
        }
    });
});

$('body').on('click', '.confirm_role_editor_btn', function (e) {
    e.preventDefault();

    alert("salom");

    let url = $(this).data('url');

    $.ajax({
        type: 'GET',
        url: url,
        success: function (response) {
             swal({
                    title: response.message,
                    timer: 1500,
                });
             window.location.reload();
        },
        error: function (error) {
            console.log(error);
        }
    });
});


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}