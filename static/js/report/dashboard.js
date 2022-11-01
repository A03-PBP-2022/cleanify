counter = 0
function updateTable() {
	var tempCounter = counter;
	// AJAX GET melakukan append data
	$.get(window.JSON_URL, function (data) {
		var card = document.getElementById("card-deck");
		card.innerHTMLL = ""
		let string = ``
		for (var i = counter; i < data.length; i++) {
			string += `
<div class="card-group">
<div class = "card mb-2 bg-light">
	<div class="card-header">
		<small class = "card-date">${data[i].fields.date}</small>
	</div>
	<div class="card-body">
		<small class="card-title">Urgency level: ${data[i].fields.urgency}</small>
		<div>
			<small class="card-description">Description: ${data[i].fields.description}</small>
		</div>
	</div>
	<div class="card-footer">
		<small class="card-description">${data[i].fields.location}</small>
	</div>
</div>
</div>`
			tempCounter++;
		}
		card.innerHTML = string
		let str = document.getElementById("cardBody").innerHTML;
		let res = str.replace(/\\n/g, '<br> <br>');
		document.getElementById("cardBody").innerHTML = res;

		counter = tempCounter;
	});
}

// Melakukan refresh ketika button diklik
$(document).ready(function () {
	updateTable();
})