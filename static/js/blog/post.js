const newCommentForm = document.querySelector("#new-comment-form")

newCommentForm.addEventListener("submit", event => {
	event.preventDefault()
	console.log(event)
})