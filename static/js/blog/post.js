const commentsListEl = document.querySelector('#comments-list')
const commentTemplate = document.querySelector('#template-comment').content
const commentEditTemplate = document.querySelector('#template-comment-edit').content
const noCommentsPlaceholderEl = document.querySelector("#comments-no-comment")
let loadedComments = []
let hasDeletedComment = false
let currentPage = 1
let isLastPage = false
let isLoadingComments = false
let userId = -1;
const permissions = {
	addComment: 0,
	changeComment: 0,
	viewComment: 0,
	deleteComment: 0
}

const createCommentEl = comment => {
	const commentEl = commentTemplate.cloneNode(true).firstElementChild
	commentEl.dataset.id = comment.pk
	commentEl.querySelector(".comment-author").textContent = comment.author.username
	commentEl.querySelector(".comment-content").innerHTML = marked.parse(comment.content)
	commentEl.querySelector(".comment-timestamp").textContent = new Date(comment.created_timestamp).toLocaleDateString('en-uk', { year: "numeric", month: "long", day: "numeric", timeZone: "UTC" })

	if (permissions.changeComment === 2 || (permissions.changeComment === 1 && comment.author.pk == userId)) {
		commentEl.querySelector(".comment-edit").addEventListener('click', event => {
			event.preventDefault()
			const commentContentEl = commentEl.querySelector('article')
			const commentEditEl = commentEditTemplate.cloneNode(true).firstElementChild
			commentEl.removeChild(commentContentEl)
			commentEl.appendChild(commentEditEl)

			const commentEditSubmitEl = commentEditEl.querySelector(".comment-edit-submit")
			const commentEditInputEl = commentEditEl.querySelector(".comment-edit-input")
			commentEditInputEl.innerHTML = comment.content
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
	} else {
		commentEl.querySelector(".comment-edit-part").remove()
	}

	if (permissions.deleteComment === 2 || (permissions.deleteComment === 1 && comment.author.pk == userId)) {
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
						// loadedComments = loadedComments.filter(id => id !== comment.pk)
						currentPage = Math.max(Math.ceil(loadedComments.length / 10), 1)
						updateNoCommentsPlaceholder()
					}
				})
		})
	} else {
		commentEl.querySelector(".comment-delete-part").remove()
	}

	return commentEl
	
}

const loadComments = async (page = currentPage) => {

	isLoadingComments = true

	try {
		const request = await fetch(commentsListEl.dataset.action + "?page=" + page)
		const comments = await request.json()
		// commentsListEl.style.minHeight = commentsListEl.offsetHeight + "px"
		isLastPage = comments.length !== 10
		comments.results.forEach(comment => {
			if (loadedComments.includes(comment.pk)) return
			const commentEl = createCommentEl(comment)
			commentsListEl.appendChild(commentEl)
			loadedComments.push(comment.pk)
		})
		// commentsListEl.style.minHeight = 0
		isLoadingComments = false
		updateNoCommentsPlaceholder()
		
	} catch {
		isLoadingComments = false
	}
}

const emptyCommentList = () => {
	loadedComments.length = 0
	hasDeletedComment = false
	currentPage = 1
	commentsListEl.innerHTML = ""
	isLastPage = false
	updateNoCommentsPlaceholder()
}

const updateNoCommentsPlaceholder = () => {
	if (loadedComments.length) noCommentsPlaceholderEl.classList.add('d-none')
	else noCommentsPlaceholderEl.classList.remove('d-none')
}

(async () => {
	const userInfoRequest = await fetch('/auth/api/info')
	const userInfo = await userInfoRequest.json()
	const userPermissions = userInfo.permissions
	if (userPermissions.includes('add_comment')) permissions.addComment += 1
	if (userPermissions.includes('change_self_comment')) permissions.changeComment += 1
	if (userPermissions.includes('change_other_comment')) permissions.changeComment += 1
	if (userPermissions.includes('delete_self_comment')) permissions.deleteComment += 1
	if (userPermissions.includes('delete_other_comment')) permissions.deleteComment += 1
	userId = userInfo.pk
	await loadComments(1)

	document.addEventListener('scroll', event => {
		if (document.body.scrollHeight - window.innerHeight/2 > window.pageYOffset + window.innerHeight) return
		if (isLoadingComments || isLastPage) return
		currentPage += 1
		loadComments(currentPage)
	})	
})()


const newCommentForm = document.querySelector("#comment-new-form")

if (newCommentForm) newCommentForm.addEventListener("submit", async event => {
	event.preventDefault()
	const formData = new FormData(event.target)
	const formProps = Object.fromEntries(formData)
	const actionUrl = event.target.getAttribute('action')
	const response = await fetch(actionUrl, {
		method: 'POST',
		body: JSON.stringify(formProps),
		headers: {
			'X-CSRFToken': window.CSRF_TOKEN
		}
	})
	if (response.status === 200 || response.status === 201) {
		commentId = (await response.json()).pk
		console.log(commentId)

		const newResponse = await fetch(commentsListEl.dataset.action + commentId)
		const newComment = await newResponse.json()
		const commentEl = createCommentEl(newComment)
		commentsListEl.prepend(commentEl)
		loadedComments.push(newComment.pk)
		// currentPage = Math.max(Math.ceil(loadedComments.length / 10), 1)
		// // if (isLastPage) loadComments()
		// loadComments()
	}
})

const deletePostButton = document.querySelector(".post-delete")

if (deletePostButton) deletePostButton.addEventListener('click', event => {
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