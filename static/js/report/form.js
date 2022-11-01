function clear() {
	var form = document.getElementById("form_post");
	form.reset();
}

// Melakukan GET POST ketika submit form
$(document).on('submit', '#form_post', function (e) {
	e.preventDefault();
	var form = document.getElementById("form_post");
	var formData = new FormData(form);
	$.ajax({
		type: "POST",
		processData: false,
		contentType: false,
		url: window.ADD_ENDPOINT,
		data: formData,
		success: function (response) {
			clear();
			console.log("hai");
		},
	})
});
