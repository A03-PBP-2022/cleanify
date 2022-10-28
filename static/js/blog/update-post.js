const form = document.querySelector("#add-form")

form.addEventListener("submit", event => {
	event.preventDefault()
	const formData = new FormData(event.target)
	const formProps = Object.fromEntries(formData)
	const actionUrl = event.target.getAttribute('action')
	const redirectUrl = event.target.dataset.redirect || window.location.href
	fetch(actionUrl, {
		method: 'POST',
		body: JSON.stringify(formProps),
		headers: {
			'X-CSRFToken': window.CSRF_TOKEN
		}
	})
		.then(response => {
			if (response.status === 200 || response.status === 201) {
				window.location = redirectUrl
			}
		})
})