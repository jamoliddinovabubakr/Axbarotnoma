$(document).ready(function () {
    $('#add_author_btn').one('click', function (e) {
        e.preventDefault();
        let article_id = $('#id_article').val();
        let fname = $('#author_fname').val();
        let lname = $('#author_lname').val();
        let mname = $('#author_mname').val();
        let email = $('#author_email').val();
        let work = $('#author_work_place').val();
        let author_tr = $('#author_author_order').val();

        if (fname == "" || lname == "" || mname == "" || email == "" || work == "" || author_tr == 0){
            alert("Please complete fields !");
        } else {
            $.ajax({
                type: "POST",
                url: "author/"+ article_id,
                data: "POST",
                response: "POST",
                error: "POST",
            });
        }


    });
});


