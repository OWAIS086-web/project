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
        let instance_id = $(this).attr('data-instance')
        console.log(instance_id)
        // let driver_head_icon = $(`#driver_and_head_input_${instance_id}`).val();
        let driver_head_icon = $(`#driver_and_head_input_${instance_id}`).prop('files')[0];
        console.log(driver_head_icon)
        let url = `/implant-types/admin/impant-types/${instance_id}/driver-head-icon/`;
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
            success: function (data) {
                console.log(data)
            },
            error: function (request, status, error) {
                console.log(error)
            }

        })
    })
})(jQuery)
