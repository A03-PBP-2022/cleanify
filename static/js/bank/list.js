$(document).ready(() => {
	getBanks();
})

function getBanks() {
	console.log("in getTasks")
	$.ajax({
		type: "GET",
		url: "/banksampah/json/",
	}).done((data) => {
		console.log("about to showTasks")
		showBanks(data)
	});
}

function showBanks(data) {
	console.log("in showTasks");
	const cards = $('.cards');
	cards.empty();
	data.forEach(bank => {
		console.log('test');
		const card = `
		<div class="col-12 col-md-6 col-xl-4">
			<div class="card">
				<div>
					<h4><label for="jenis">Type</label></h4>
					<p id="jenis">${bank.fields.jenis}</p>
					<h4><label for="alamat">Address</label></h4>
					<p id="alamat"><span style="font-weight:normal">${bank.fields.alamat}</p>
					<h4><label for="tanggal">Date</label></h4>
					<p id="tanggal">${bank.fields.tanggal}</p>
				</div>
				<div class="card-link-wrapper">
					<button class="btn btn-danger" type="submit" value="Delete" onclick=deleteTask(${bank.pk})><i class="btn-danger"></i>Delete</button>
				</div>
			</div>
		</div>`;
		cards.append(card);
	})
}

function deleteTask(id) {
	$.ajax({
		type: "GET",
		url: "/banksampah/delete/" + id,
		data: { csrfmiddlewaretoken: window.CSRF_TOKEN, pk: id }
	}).done((data) => {
		getBanks();
	})
}
