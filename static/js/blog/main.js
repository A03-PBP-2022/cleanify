console.log(123)
console.log(document.querySelectorAll('textarea.expand'))

;[...document.querySelectorAll('textarea.expand')].forEach(el => {
	const offsetHeight = el.offsetHeight
	el.addEventListener('input', () => {
		el.style.height = ""
		el.style.height = Math.max(offsetHeight, el.scrollHeight + 2) + 'px'
	});
	el.style.height = Math.max(offsetHeight, el.scrollHeight + 2) + 'px'
})