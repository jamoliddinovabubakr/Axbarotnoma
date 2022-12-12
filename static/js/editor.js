// EDITOR DASHBOARD

$('body').on('click', '.resultBtnUnReview', function (e) {
    e.preventDefault();
    let data = $(this).data('id');
    let article_id = parseInt(data.split(',')[0]);
    let notif_id = parseInt(data.split(',')[1]);
    let btn_number = parseInt(data.split(',')[2]);
    let token = $(this).data('action');
    let text = $('#resubmit_or_reject_text').val();


    if (text.length > 0) {
        $.ajax({
            type: "POST",
            url: "/profile/editor_submit_result/",
            data: {
                article_id: article_id,
                notif_id: notif_id,
                text: text,
                btn_number: btn_number,
                csrfmiddlewaretoken: token,
            },
            success: function (response) {
                window.location.reload();
            },
            error: function (error) {
                console.log(error);
            }
        });

    } else {
        alert("Izohni kiriting!");
    }

});

$('body').on('click', '.resubmit_to_reviewer_btn', function (e) {
    e.preventDefault();

    let id = $(this).data('id');
    let token = $(this).data('action');

    $.ajax({
        type: "POST",
        url: "/profile/editor_resubmit_to_reviewer/",
        data: {
            review_id: id,
            csrfmiddlewaretoken: token,
        },
        success: function (response) {
            $('#resubmit_to_reviewer_btn_' + id).prop("disabled", true);
            swal({
                title: response.message,
                timer: 1500,
            });

        },
        error: function (error) {
            console.log(error);
        }
    });

});

$('body').on('click', '.resultBtn', function (e) {
    e.preventDefault();
    let data = $(this).data('id');
    let article_id = parseInt(data.split(',')[0]);
    let notif_id = parseInt(data.split(',')[1]);
    let btn_number = parseInt(data.split(',')[2]);
    let token = $(this).data('action');

    if (btn_number === 2) {
        let text = $('#resubmit_text').val();
        if (text.length > 0) {
            $.ajax({
                type: "POST",
                url: "/profile/approve_publish/",
                data: {
                    article_id: article_id,
                    notif_id: notif_id,
                    text: text,
                    btn_number: btn_number,
                    csrfmiddlewaretoken: token,
                },
                success: function (response) {
                    $('#approveForPublicationBtn').prop("disabled", true);

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

        } else {
            alert("Izohni kiriting!");
        }
    }

    if (btn_number === 0 || btn_number === 1 || btn_number === 3) {
        $.ajax({
            type: "POST",
            url: "/profile/approve_publish/",
            data: {
                article_id: article_id,
                notif_id: notif_id,
                btn_number: btn_number,
                csrfmiddlewaretoken: token,
            },
            success: function (response) {
                $('#approveForPublicationBtn').prop("disabled", true);

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
    }

});

$('body').on('click', '#random_send_reviewer_btn', function (e) {
    e.preventDefault();

    let id = $(this).data('id');
    let token = $(this).data('action');

    let value = $('#reviewer_number').val();

    if (value > 0) {
        $.ajax({
            type: "POST",
            url: "/profile/random_sending_reviewer/",
            data: {
                value: value,
                article_id: id,
                csrfmiddlewaretoken: token,
            },
            success: function (response) {
                if (response.is_valid) {
                    $('#send_btn_to_reviewer').prop("disabled", true);
                    $('#random_send_reviewer_btn').prop("disabled", true);
                    swal({
                        title: response.message,
                        timer: 1500,
                    });
                    window.location.reload();
                } else {
                    alert(response.message);
                }
            },
            error: function (error) {
                console.log(error);
            }
        });
    } else {
        alert("Taqrizchilar sonini kiriting!")
    }
});

$('body').on('click', '#send_btn_to_reviewer', function (e) {
    e.preventDefault();

    let article_id = $(this).data('id');
    let token = $(this).data('action');

    let selected = [];
    $('#widget-todolist-body input[type=checkbox]').each(function () {
        if ($(this).is(":checked")) {
            selected.push($(this).val());
        }
    });

    let n = selected.length;

    if (n === 0) {
        alert("Taqrizchi tanlamadiz!");
    }

    if (n > 5) {
        alert("5 tadan kop Taqrizchi tanladiz");
    }

    if (n >= 1 && n <= 5) {
        $.ajax({
            type: "POST",
            url: "/profile/sending_reviewer/",
            data: {
                reviewers: selected,
                csrfmiddlewaretoken: token,
                article_id: article_id
            },
            success: function (response) {
                if (response.is_valid) {
                    $('#send_btn_to_reviewer').prop("disabled", true);
                    $('#random_btn').prop("disabled", true);

                    swal({
                        title: response.message,
                        timer: 1500,
                    });
                    window.location.reload();
                } else {
                    alert(response.message);
                }
            },
            error: function (error) {
                console.log(error);
            }

        });
    }

});


$('body').on('click', '#view-article-messages-by-editor', function (e) {
    e.preventDefault();

    let id = $(this).data('id');

    $.ajax({
        type: "GET",
        url: "/profile/article_notification/view/" + id + "/",
        success: function (response) {
            console.log(response);
            $('#MessageBoxEditor').css('display', 'block');
            $('#editor_chat_body').empty();

            for (let item of response.notifications) {

                let time_tz = new Date(item.created_at);
                let time_string = time_tz.toLocaleString();
                console.log(time_string);

                if (response.current_user_id === item.from_user__id) {

                    let temp1 = `<div class="widget-chat-item right"><div class="widget-chat-info"><div class="widget-chat-info-container">
                                        <div class="widget-chat-name text-indigo">`
                        + item.from_user__email +
                        `</div><div class="widget-chat-message">`
                        + item.message +
                        `</div><div class="widget-chat-time">`
                        + `</div></div></div></div>`;

                    $('#editor_chat_body').append(temp1);
                }

                if (response.current_user_id === item.to_user__id) {
                    console.log("menga");

                    let temp2 = `<div class="widget-chat-item left">
                                        <div class="widget-chat-info">
                                            <div class="widget-chat-info-container">
                                        <div class="widget-chat-name text-indigo">`
                        + item.from_user__email +
                        `</div><div class="widget-chat-message">` + item.message + `</div>
                                             <div class="widget-chat-time">` + `</div>
                                             <br><div class="widget-chat-ansewer">
                                                <button type="button" data-id="${id},${item.from_user__id}" class="btn btn-white btn-sm editorWrite-message-btn">Ansewer</button>
                                            </div>
                                            </div></div></div>`;
                    $('#editor_chat_body').append(temp2);
                }
            }

        },
        error: function (response) {
            console.log(response);
        }
    });

});

$('body').on('click', '.editorWrite-message-btn', function (e) {
    e.preventDefault();

    const data = $(this).data('id');
    const array = data.split(',');
    const id = array[0];
    const user_id = parseInt(array[1]);
    $.ajax({
        type: 'GET',
        url: "/send_message/" + id + "/" + user_id,
        success: function (response) {
            $('#writeeditor_message_div').html(response);
            $('#send-message-modal').modal('show');
        },
        error: function (error) {
            console.log("Xatolik");
            console.log(error);
        }
    });
});

$(document).ready(function () {
    setInterval(function () {
        $.ajax({
            type: 'GET',
            url: "/profile/editor_notifications/",
            success: function (response) {
                $('#editor_uncheck_notifications').empty();
                $('#editor_checked_notifications').empty();

                if (response.uncheck_notifications.length > 0) {
                    for (let item of response.uncheck_notifications) {

                        let time = new Date(item.created_at);
                        let time_string = time.toLocaleString();

                        let uncheck = `<tr>` +
                            `<td>` + item.id + `</td>` +
                            `<td><b>` + item.article__author__email + `</b><br>` +
                            item.article__title.toString().slice(0, 100) + `</td>` +
                            `<td>` + time_string + `</td>` +
                            `<td id="view_notif_id${item.id}"></td>` +
                            `<td><button type="button" data-id="${item.id}" class="btn btn-primary btn-sm article_view_editor" style="float: right"><i class="fas fa-fw m-r-5 fa-pen"></i>View
                                </button></td>`
                            + `</tr>`;

                        $('#editor_uncheck_notifications').append(uncheck);


                        if (item.notification_status__id === 1) {
                            $('#view_notif_id' + item.id).html("<span class='badge badge-danger'>" + item.notification_status__name + "</span>");
                        }
                        if (item.notification_status__id === 2) {
                            $('#view_notif_id' + item.id).html("<span class='badge badge-warning'>" + item.notification_status__name + "</span>");
                        }

                    }
                } else {
                    let tr = `<tr>` +
                        `<td><h3 class="text-center" style="color: green;">NO DATA</h3></td>`
                        + `</tr>`;
                    $('#editor_uncheck_notifications').append(tr);
                }

                if (response.check_notifications.length > 0) {
                    for (let item of response.check_notifications) {

                        let time = new Date(item.created_at);
                        let time_string = time.toLocaleString();

                        let checked = `<tr>` +
                            `<td>` + item.id + `</td>` +
                            `<td><b>` + item.article__author__email + `</b><br>` +
                            item.article__title.toString().slice(0, 100) + `</td>` +
                            `<td>` + time_string + `</td>` +
                            `<td id="view_notif_checked_id${item.id}"></td>` +
                            `<td><button type="button" data-id="${item.id}" class="btn btn-primary btn-sm article_view_editor" style="float: right"><i class="fas fa-fw m-r-5 fa-pen"></i>View
                                </button></td>`
                            + `</tr>`;

                        $('#editor_checked_notifications').append(checked);

                        if (item.notification_status__id == 3) {
                            $('#view_notif_checked_id' + item.id).html("<span class='badge badge-success'>" + item.notification_status__name + "</span>");
                        }

                    }
                } else {
                    let tr = `<tr>` + `<td><h3 class="text-center" style="color: green;">NO DATA</h3></td>` + `</tr>`;
                    $('#editor_checked_notifications').append(tr);
                }

            },
            error: function (response) {
                console.log(response);
            }
        });
    }, 2000);
});

$('body').on('click', '.article_view_editor', function (e) {
    e.preventDefault();

    let id = $(this).data('id');

    $.ajax({
        type: "GET",
        url: "/profile/editor_check_article/" + id + "/",
        success: function (response) {
            $('.editor_dashboard').empty();
            $('.editor_dashboard').html(response);
        },
        error: function (response) {
        }
    });
});

$('body').on('click', '.choose_type_sumit_btn', function (e) {
    e.preventDefault();

    let btn_id = $(this).data('id');

    if (btn_id == 1) {
        $('#list_reviewers').css("display", "block");
        $('#random_btn').css("display", "none");

        $.ajax({
            type: 'GET',
            url: "/profile/load_reviewers/",
            success: function (response) {
                $('#widget-todolist-body').empty();
                $('#count_reviewer').html("<span>" + response.reviewers.length + "</span><small>Count</small>");


                for (let item of response.reviewers) {
                    let widget_item = `<div class="widget-todolist-item">` +
                        `<div class="widget-todolist-input"><div class="checkbox checkbox-css pt-0">` +
                        `<input type="checkbox" id="widget_todolist_${item.id}" name="reviewer_checkbox" value="${item.id}"/><label for="widget_todolist_${item.id}" class="p-l-15">&nbsp;</label></div></div>` +
                        `<div class="widget-todolist-content"><h4 class="widget-todolist-title">` + item.user__last_name + " " + item.user__first_name + " " + item.user__middle_name +
                        `</h4><p class="widget-todolist-desc"><b>Email:</b>${item.user__email}</p></div><div class="widget-todolist-icon"><p class="widget-todolist-desc">${item.scientific_degree__name}</p></div><div class="widget-todolist-icon">
											<a href="#"><i class="fa fa-question-circle"></i></a></div>`
                        + `</div>`;

                    $('#widget-todolist-body').append(widget_item);
                }
            },
            error: function (error) {
                console.log("Xatolik");
                console.log(error);
            }
        });
    }

    if (btn_id == 2) {
        $('#list_reviewers').css("display", "none");
        $('#random_btn').css("display", "block");
    }

});