$(document).ready(function () {
    setInterval(function () {
        $.ajax({
            type: 'GET',
            url: "/profile/reviewer_notifications/",
            success: function (response) {
                console.log(response)
                $('#reviewer_uncheck_notifications').empty();
                $('#reviewer_checked_notifications').empty();

                if (response.uncheck_notifications.length > 0) {
                    for (let item of response.uncheck_notifications) {

                        let time = new Date(item.created_at);
                        let time_string = time.toLocaleString();

                        let uncheck = `<tr>` +
                            `<td>` + item.id + `</td>` +
                            `<td><b>` + item.from_user__email + `</b><br>` +
                            item.message + `</td>` +
                            `<td>` + time_string + `</td>` +
                            `<td id="view_notif_id${item.id}"></td>` +
                            `<td><button type="button" data-id="${item.id}" class="btn btn-primary btn-sm article_view_reviewer" style="float: right"><i class="fas fa-fw m-r-5 fa-pen"></i>View
                                </button></td>`
                            + `</tr>`;

                        $('#reviewer_uncheck_notifications').append(uncheck);

                        if (item.notification_status__id == 1) {
                            $('#view_notif_id' + item.id).html("<span class='badge badge-danger'>" + item.notification_status__name + "</span>");
                        }
                        if (item.notification_status__id == 2) {
                            $('#view_notif_id' + item.id).html("<span class='badge badge-warning'>" + item.notification_status__name + "</span>");
                        }
                        if (item.notification_status__id == 3) {
                            $('#view_notif_id' + item.id).html("<span class='badge badge-success'>" + item.notification_status__name + "</span>");
                        }

                    }
                } else {
                    let tr = `<tr>` +
                        `<td><h3 class="text-center" style="color: green;">NO DATA</h3></td>`
                        + `</tr>`;
                    $('#reviewer_uncheck_notifications').append(tr);
                }

                if (response.check_notifications.length > 0) {
                    for (let item of response.check_notifications) {

                        let time = new Date(item.created_at);
                        let time_string = time.toLocaleString();

                        let checked = `<tr>` +
                            `<td>` + item.id + `</td>` +
                            `<td><b>` + item.from_user__email + `</b><br>` +
                            item.message + `</td>` +
                            `<td>` + time_string + `</td>` +
                            `<td id="view_notif_checked_id${item.id}"></td>` +
                            `<td><button type="button" data-id="${item.id}" class="btn btn-primary btn-sm article_view_reviewer" style="float: right"><i class="fas fa-fw m-r-5 fa-pen"></i>View
                                </button></td>`
                            + `</tr>`;

                        $('#reviewer_checked_notifications').append(checked);

                        if (item.notification_status__id == 3) {
                            $('#view_notif_checked_id' + item.id).html("<span class='badge badge-success'>" + item.notification_status__name + "</span>");
                        }

                    }
                } else {
                    let tr = `<tr>` + `<td><h3 class="text-center" style="color: green;">NO DATA</h3></td>` + `</tr>`;
                    $('#reviewer_checked_notifications').append(tr);
                }

            },
            error: function (response) {
                console.log(response);
            }
        });
    }, 2000);
});

$('body').on('click', '.article_view_reviewer', function (e) {
    e.preventDefault();

    let id = $(this).data('id');

    $.ajax({
        type: "GET",
        url: "/profile/reviewer_check_article/" + id + "/",
        success: function (response) {
            $('.dashboard_reviewer').empty();
            $('.dashboard_reviewer').html(response);
        },
        error: function (response) {
        }
    });
});


$('body').on('click', '#resubmit_reviewer_btn', function (e) {
    e.preventDefault();
    const $myForm = $('.sending_editor_form');
    const $formData = $myForm.serialize();

    let comment = $('#id_comment').val();

    $.ajax({
        type: "POST",
        url: "/profile/reviewer_resubmit/",
        data: $formData,
        success: function (response) {
            console.log(response.message);
            window.location.reload();
        },
        error: function (error) {
            console.log("Error");
        }
    });
});


$('body').on('click', '#reject_reviewer_btn', function (e) {
    e.preventDefault();
    const $myForm = $('.sending_editor_form');
    const $formData = $myForm.serialize();

    let comment = $('#id_comment').val();

    $.ajax({
        type: "POST",
        url: "/profile/reviewer_rejected/",
        data: $formData,
        success: function (response) {
            console.log(response.message);
            window.location.reload();
        },
        error: function (error) {
            console.log("Error");
        }
    });
});


$('body').on('click', '#confirm_reviewer_btn', function (e) {
    e.preventDefault();
    const $myForm = $('.sending_editor_form');
    const $formData = $myForm.serialize();

    let comment = $('#id_comment').val();

    $.ajax({
        type: "POST",
        url: "/profile/reviewer_confirmed/",
        data: $formData,
        success: function (response) {
            console.log(response.message);
            window.location.reload();
        },
        error: function (error) {
            console.log("Error");
        }
    });
});


$('body').on('click', '#view-article-messages-by-reviewer', function (e) {
    e.preventDefault();

    let id = $(this).data('id');

    $.ajax({
        type: "GET",
        url: "/profile/article_notification/view/" + id + "/",
        success: function (response) {
            console.log(response);
            $('#MessageBoxReviewer').css('display', 'block');
            $('#reviewer_chat_body').empty();

            for (let item of response.notifications) {

                let time_tz = new Date(item.created_at);
                let time_string = time_tz.toLocaleString();
                console.log(time_string);

                if (response.current_user_id === item.from_user__id) {

                    let temp1 = `<div class="widget-chat-item right"><div class="widget-chat-info"><div class="widget-chat-info-container"><div class="widget-chat-name text-indigo">`
                        + item.from_user__email +
                        `</div><div class="widget-chat-message">`
                        + item.message +
                        `</div><div class="widget-chat-time">` + `</div></div></div></div>`;

                    $('#reviewer_chat_body').append(temp1);
                }

                if (response.current_user_id === item.to_user__id) {

                    let temp2 = `<div class="widget-chat-item left">
                                        <div class="widget-chat-info">
                                            <div class="widget-chat-info-container">
                                                <div class="widget-chat-name text-indigo">`
                        + item.from_user__email +
                        `</div><div class="widget-chat-message">`
                        + item.message +
                        `</div><div class="widget-chat-time">` + `</div>
                                                         <br><div class="widget-chat-ansewer">
                                                            <button type="button" data-id="${id},${item.from_user__id}" class="btn btn-white btn-sm reviewerWrite-message-btn">Ansewer</button>
                                                        </div>
                                                        </div></div></div>`;
                    $('#reviewer_chat_body').append(temp2);
                }
            }

        },
        error: function (response) {
            console.log(response);
        }
    });

});


$('body').on('click', '.reviewerWrite-message-btn', function (e) {
    e.preventDefault();

    const data = $(this).data('id');
    const array = data.split(',');
    const id = array[0];
    const user_id = parseInt(array[1]);

    $.ajax({
        type: 'GET',
        url: "/send_message/" + id + "/" + user_id,
        success: function (response) {
            $('#writereviewer_message_div').html(response);
            $('#send-message-modal').modal('show');
        },
        error: function (error) {
            console.log("Xatolik");
            console.log(error);
        }
    });
});