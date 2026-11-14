const onSubmit = async (event) => {
	event.preventDefault()
	const form = event.currentTarget
	const button = form.querySelector('button[type="submit"]')
	const generateLabel = form.querySelector("#generate-label")
	const loadingStatus = form.querySelector("#loading-status")
	const generatedResult = document.querySelector("#generated-result")
	const errorSection = document.querySelector("#generation-error")
	const errorMessage = errorSection.querySelector(
		"#generation-error-message",
	)

	button.disabled = true
	form.setAttribute("aria-busy", "true")
	generateLabel.hidden = true
	loadingStatus.hidden = false
	generatedResult.hidden = true
	errorSection.hidden = true

	try {
		const response = await fetch(
			form.action,
			{method: "POST"},
		)

		if (!response.ok) throw new Error(
			`Request failed with status ${response.status}.`
		)

		const data = await response.json()
		if (data.error) throw new Error(
			data.error ?? "Request failed"
		)

		const params = new URLSearchParams({
			compressed_phrase: data.compressed_phrase,
			tweet_id: data.tweet_id,
		})

		window.location.assign(`/tweet-generator?${params}`)
	} catch (error) {
		button.disabled = false
		form.removeAttribute("aria-busy")
		generateLabel.hidden = false
		loadingStatus.hidden = true
		errorSection.hidden = false
		errorMessage.textContent = error instanceof Error
			? error.message
			: String(error)
	}
}

document
.querySelector("#generate-form")
.addEventListener("submit", onSubmit)
