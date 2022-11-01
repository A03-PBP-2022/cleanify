$(".thumbsUp").on('click', function () {
	var dataPK = $(this).attr('data-pk');
	$.ajax({
		headers: { 'X-CSRFToken': window.CSRF_TOKEN },
		type: 'POST',
		url: "{% url 'faq:update_thumbsUp' %}",
		data: {
			pk: dataPK
		},
		success: function () {
			console.log('Success')
			location.reload(true)
		}
	})
})
