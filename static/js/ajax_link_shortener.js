$('button[type=submit]').click(function (e) {
    e.preventDefault();
    if ($(this).attr("id") === "copy") {
        var copyText = document.getElementById("url_input");
        copyText.select();
        copyText.setSelectionRange(0, 100);
        document.execCommand("copy");
        return false;
    }
    var $form = $(this).closest('form');

    $.ajax({
        type: $form.attr('method'),
        url: $form.attr('action'),
        data: $form.serialize()
    }).done(function (data) {
        if (data.error) {
            alert(data.error);
        } else if (data.message) {
            $('#url_input').val(data.message);
            $('button#submit').hide();
            $('button#copy').show();
        }
    });
});

$('#url_input').on("keypress, keyup, keydown", function () {
    $('button#submit').show();
    $('button#copy').hide();
});