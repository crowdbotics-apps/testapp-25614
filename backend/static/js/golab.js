// $(document).on('click', '#filter-form .btn-reset', function (event) {
//     event.preventDefault();
// });
$(document).on('click', '.btn-schedule-view', function (event) {
    event.preventDefault();
    let url = $(this).data('url');
    let type = $(this).data('type');
    console.log(url);
    let title = $('#name-' + type).html();
    $('#scheduleModalView .modal-title').html(title);
    // $('#scheduleModalView .modal-body iframe').attr('src', url);
    let modalObject = $('#scheduleModalView');
    modalObject.modal('show');
    modalObject.on('shown.bs.modal', function () {
        modalObject.find('.modal-body iframe').attr('src', url);
        modalObject.find('.modal-body iframe').removeClass('d-none');
        modalObject.find('.modal-body iframe').load(function () {
            $('.loading').hide();

        });
    });


});
$('#scheduleModalView').on('hidden.bs.modal', function () {
    let modalObject = $('#scheduleModalView');
    modalObject.find('.modal-body iframe').attr('src', '');
    modalObject.find('.modal-body iframe').addClass('d-none');
});

$(document).on('click', '.filter-card .btn-toggle-filter-box', function (event) {
    event.preventDefault();
    $('.filter-card .card-body').toggleClass('d-none');
});
