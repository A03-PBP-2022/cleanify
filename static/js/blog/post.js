const commentsListEl = document.querySelector('#comments-list')
const commentTemplate = document.querySelector('#template-comment').content
const commentEditTemplate = document.querySelector('#template-comment-edit').content
let loadedComments = []
let hasDeletedComment = false
let currentPage = 1
let isLastPage = false
let isLoadingComments = false

const loadComments = (page = currentPage) => {

	isLoadingComments = true

	fetch(commentsListEl.dataset.action + "?page=" + page)
		.catch(response => isLoadingComments = false)
		.then(response => response.json())

		.then(comments => {
			// commentsListEl.style.minHeight = commentsListEl.offsetHeight + "px"
			isLastPage = comments.length !== 10
			comments.forEach(comment => {
				if (loadedComments.includes(comment.pk)) return

				const commentEl = commentTemplate.cloneNode(true).firstElementChild
				commentEl.dataset.id = comment.pk
				commentEl.querySelector(".comment-author").textContent = comment.fields.author.username
				commentEl.querySelector(".comment-content").innerHTML = marked.parse(comment.fields.content)
				commentEl.querySelector(".comment-timestamp").textContent = new Date(comment.fields.created_timestamp).toLocaleDateString('en-uk', { year: "numeric", month: "long", day: "numeric", timeZone: "UTC" })

				if (!comment.perms.edit) {
					commentEl.querySelector(".comment-edit-part").remove()
				}

				if (!comment.perms.delete) {
					commentEl.querySelector(".comment-delete-part").remove()
				}

				const deleteButton = commentEl.querySelector(".comment-delete")
				const deleteUrl = deleteButton.dataset.action.replace('0', comment.pk)
				delete deleteButton.dataset.action

				commentEl.querySelector(".comment-delete").addEventListener('click', event => {
					event.preventDefault()
					fetch(deleteUrl, {
						method: 'DELETE',
						headers: {
							'X-CSRFToken': window.CSRF_TOKEN
						}
					})
						.then(response => {
							if (response.status === 200 || response.status === 201) {
								// loadComments()
								commentEl.remove()
								hasDeletedComment = true
								isLastPage = false
								loadedComments = loadedComments.filter(id => id !== comment.pk)
								currentPage = Math.max(Math.ceil(loadedComments.length / 10), 1)
							}
						})
				})

				commentEl.querySelector(".comment-edit").addEventListener('click', event => {
					event.preventDefault()
					const commentContentEl = commentEl.querySelector('article')
					const commentEditEl = commentEditTemplate.cloneNode(true).firstElementChild
					commentEl.removeChild(commentContentEl)
					commentEl.appendChild(commentEditEl)

					const commentEditSubmitEl = commentEditEl.querySelector(".comment-edit-submit")
					const commentEditInputEl = commentEditEl.querySelector(".comment-edit-input")
					commentEditInputEl.innerHTML = comment.fields.content
					editUrl = commentEditSubmitEl.dataset.action.replace('0', comment.pk)

					commentEditSubmitEl.addEventListener('click', event => {
						event.preventDefault()
						fetch(editUrl, {
							method: 'POST',
							body: JSON.stringify({
								content: commentEditInputEl.value
							}),
							headers: {
								'X-CSRFToken': window.CSRF_TOKEN
							}
						})
							.then(response => {
								if (response.status === 200 || response.status === 201) {
									commentEl.removeChild(commentEditEl)
									commentEl.appendChild(commentContentEl)
									return response.json()
								}
								throw Error()
							})
							.then(newComment => {
								comment = newComment
								commentEl.querySelector(".comment-content").innerHTML = marked.parse(comment.fields.content)
							})
					
					})
				})

				commentsListEl.appendChild(commentEl)
				loadedComments.push(comment.pk)
			})
			// commentsListEl.style.minHeight = 0
			isLoadingComments = false
		})
}

const emptyCommentList = () => {
	loadedComments.length = 0
	hasDeletedComment = false
	currentPage = 1
	commentsListEl.innerHTML = ""
	isLastPage = false
}

loadComments(1)

document.addEventListener('scroll', event => {
	if (document.body.scrollHeight - window.innerHeight/2 > window.pageYOffset + window.innerHeight) return
	if (isLoadingComments || isLastPage) return
	currentPage += 1
	loadComments(currentPage)
})

const form = document.querySelector("#comment-new-form")

if (form) form.addEventListener("submit", event => {
	event.preventDefault()
	const formData = new FormData(event.target)
	const formProps = Object.fromEntries(formData)
	const actionUrl = event.target.getAttribute('action')
	fetch(actionUrl, {
		method: 'POST',
		body: JSON.stringify(formProps),
		headers: {
			'X-CSRFToken': window.CSRF_TOKEN
		}
	})
		.then(response => {
			if (response.status === 200 || response.status === 201) {
				currentPage = Math.max(Math.ceil(loadedComments.length / 10), 1)
				if (isLastPage) loadComments()
			}
		})
})

const deletePostButton = document.querySelector(".post-delete")

deletePostButton.addEventListener('click', event => {
	event.preventDefault()
	const actionUrl = event.target.dataset.action
	const redirectUrl = event.target.dataset.redirect
	fetch(actionUrl, {
		method: 'DELETE',
		headers: {
			'X-CSRFToken': window.CSRF_TOKEN
		}
	})
		.then(response => {
			if (response.status === 200 || response.status === 201) {
				if (redirectUrl) window.location = redirectUrl
				else window.location.reload()
			}
		})
})