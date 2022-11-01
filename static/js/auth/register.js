$(document).on('submit', '#register-form', function (e) {
	e.preventDefault();

	var registrationForm = $('#register-form')

	$.ajax({
		type: 'POST',
		url: "./",
		data: registrationForm.serialize(),
		dataType: "json",
		header: { 'X-CSRFToken': window.CSRF_TOKEN },
		success: function (response) {
			var success = response['success']
			if (success) {
				window.location = "../login?status=registered"
			}
			else {
				alert("Registration failed! Please check your inputs.");
				for (var msg in response['error']) {
					var txt = JSON.stringify(response['error'][msg]);
					document.getElementById("error").innerHTML = txt.replace(/[&\/\\#,\]+()$~%['":*?<>{}]/g, '');
				}
			}
		},
	});
});