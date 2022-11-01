$(document).on('submit', '#register-form', function (e) {
	e.preventDefault();

	var register_form_id = $('#register-form')

	$.ajax({
		type: 'POST',
		url: "./",
		data: register_form_id.serialize(),
		dataType: "json",
		header: { 'X-CSRFToken': window.CSRF_TOKEN },
		success: function (response) {
			var success = response['success']
			if (success) {
				window.location = "../login?status=registered"
			}
			else {
				alert("Pendaftaran akun gagal! Harap periksa input Anda.");
				for (var msg in response['error']) {
					var txt = JSON.stringify(response['error'][msg]);
					document.getElementById("error").innerHTML = txt.replace(/[&\/\\#,\]+()$~%['":*?<>{}]/g, '');
				}
			}
		},
	});
});