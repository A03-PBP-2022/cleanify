counter = 0
function updateCards() {
	var tempCounter = counter;
	// AJAX GET melakukan append data
	$.get(window.JSON_URL, function (data) {
		var card = document.getElementById("card-deck");
		card.innerHTMLL = ""
		let string = ``
		data.forEach(report => {
			string += `
			<div class="card-group" >
				<div class = "card mb-2 bg-light">
					<div class="card-header">
						<small class = "card-date">${report.fields.date}</small>
					</div>
					<div class="card-body">
						<small class="card-title">Urgency level: ${report.fields.urgency}</small>
						<div>
							<small class="card-description">Description: ${report.fields.description}</small>
						</div>
					</div>
					<div class="card-footer">
						<small class="card-description">${report.fields.location}</small>
					</div>
				</div>
			</div>`
			tempCounter++;
			
		})
		card.innerHTML = string
		counter = tempCounter;
	});
}

$(document).ready(function () {
	updateCards();
})