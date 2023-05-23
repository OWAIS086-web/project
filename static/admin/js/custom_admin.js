// CSRF Token ERROR
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');


// $(document).ready(function () {
//     $(document).on('click', '.admin_list_driver_and_head_update_button', function (e) {
//         e.preventDefault();
//         let instance_id = $(this)
//         console.log(instance_id)
//         // let driver_head_icon = $(`#driver_and_head_input_${instance_id}`).val();
//         // console.log(driver_head_icon)
//     })
//
// })

(function ($) {
    $(document).on('click', '.admin_list_driver_and_head_update_button', function (e) {
        e.preventDefault();
        let _this = $(this);
        let instance_id = $(this).attr('data-instance')
        let msg_element = $(`#driver_and_head_message_${instance_id}`)
        // let driver_head_icon = $(`#driver_and_head_input_${instance_id}`).val();
        let driver_head_icon_input = $(`#driver_and_head_input_${instance_id}`);
        let driver_head_icon = driver_head_icon_input.prop('files')[0];
        console.log(driver_head_icon)
        let url = `/implant-types/admin/implant-types/${instance_id}/driver-head-icon/`;
        let form_data = new FormData();
        form_data.append('csrfmiddlewaretoken', csrftoken);
        form_data.append('driver_and_head', driver_head_icon);
        console.log(form_data)
        $.ajax({
            type: "POST",
            enctype: 'multipart/form-data',
            data: form_data,
            url: url,
            processData: false,
            contentType: false,
            cache: false,
            timeout: 800000,
            beforeSend: function () {
                _this.text('Uploading')
            },
            success: function (data) {
                console.log(data);
                msg_element.text('Uploaded')
                _this.text('Submit');
                driver_head_icon_input.val('');
                let html = `<img src="${data.driver_and_head}" style="max-width: 70px; height: auto">`
                $(`#driver_and_head_${instance_id}`).html(html);

            },
            error: function (request, status, error) {
                console.log(error);
                msg_element.text('Failed')
                _this.text('Submit')
            }

        })
    })
})(jQuery)
