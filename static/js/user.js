// USER DASHBOARD

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

    const data = $(this).data('id');
    const array = data.split(',');
    const id = array[0];
    const user_id = parseInt(array[1]);

    $.ajax({
        type: 'GET',
        url: "/send_message/" + id + "/" + user_id,
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

function OnClickViewArticle(id) {
    $('#MessageBoxAuthor').css("display", "none");
    let url = $('#article_view_btn_' + id).data('url');

    $.ajax({
        type: "GET",
        url: url,
        success: function (response) {
            $("#articleView").css("display", "block");

            console.log(response);
            let fileID = response['file'];
            let FileArticle = "File Not Exists";
            if (fileID != "None") {
                FileArticle = `<a href='${response['file']}' download role='button'>` + `<span>Yuklab olish</span></a>`
            }
            let temp = "<tr><td>" +
                response['id'] + "</td><td>" + FileArticle
                + `</td><td>` +
                response['title'] + `</td><td>` +
                response['created_at'] + `</td><td>` +
                `<button type="button" data-url="${response['edit_url']}" class="btn btn-sm btn-outline-warning edit_article_btn" disabled><i class="fa fa-edit"></i></button>` + " " +
                `<button type="button" data-url="${response['delete_url']}" class="btn btn-sm btn-outline-danger remove_article_btn"><i class="fa fa-trash"></i></button>`
                + "</td></tr>";
            $("#articleDetail").html(temp);
            if (response.article_status_id === 6) {
                $('.edit_article_btn').prop('disabled', false);
            }
            if (response.article_status_id === 7) {
                $('.edit_article_btn').prop('disabled', false);
            }
            if (response.article_status_id === 8) {
                $('.edit_article_btn').prop('disabled', false);
            }

        },
        error: function (response) {
            console.log(response);
        }
    });
}

$('body').on('click', '.view_message_btn', function (e) {
    e.preventDefault();
    let id = $(this).data('id');
    let url = $('#view-article-messages-by-author_' + id).data('url');

    $.ajax({
        type: "GET",
        url: url,
        success: function (response) {
            console.log(response);
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
                                                                <div class="widget-chat-message">`
                            + item.message +
                            `</div>
                                                                <div class="widget-chat-time">` + `</div>
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
                                                                <div class="widget-chat-message">`
                            + item.message +
                            `</div>
                                                                <div class="widget-chat-time">` + `</div>
                                                                <br><div class="widget-chat-ansewer">
                                                                    <button type="button" data-id="${id},${item.from_user__id}" class="btn btn-white btn-sm authorWrite-message-btn">Ansewer</button>
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


function OnClickSubmissionTab() {
    $('#articleView').css("display", "none");
    $('#MessageBox').css("display", "none");
}