$(".thumbsUp").on('click', function () {
	var dataPK = $(this).attr('data-pk');
	$.ajax({
		headers: { 'X-CSRFToken': window.CSRF_TOKEN },
		type: 'POST',
		url: window.THUMBS_UP_ENDPOINT,
		data: {
			pk: dataPK
		},
		success: function () {
			console.log('Success')
			location.reload(true)
		}
	})
})
