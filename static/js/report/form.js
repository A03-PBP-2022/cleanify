function clear() {
	var form = document.getElementById("form_post");
	form.reset();
}

// Melakukan GET POST ketika submit form
$(document).on('submit', '#form_post', function (e) {
	e.preventDefault();
	var form = document.getElementById("form_post");
	var formData = new FormData(form);
	var img = $("#image")[0].files;
	formData.append("image", img[0]);
	$.ajax({
		type: "POST",
		processData: false,
		contentType: false,
		url: "{% url 'crewdashboard:addlocation' %}",
		data: formData,
		success: function (response) {
			clear();
			console.log("hai");
		},
	})
});
