const onSubmit = async (event) => {
	event.preventDefault()
	const form = event.currentTarget
	const button = form.querySelector('button[type="submit"]')
	const generateLabel = form.querySelector("#generate-label")
	const loadingStatus = form.querySelector("#loading-status")
	const generatedResult = document.querySelector("#generated-result")

	button.disabled = true
	form.setAttribute("aria-busy", "true")
	generateLabel.hidden = true
	loadingStatus.hidden = false
	generatedResult.hidden = true

	const response = await fetch(
		form.action,
		{method: "POST"},
	)

	const data = await response.json()
	if (!response.ok) throw new Error(
		data.error ?? "Request failed."
	)

	const params = new URLSearchParams({
		compressed_phrase: data.compressed_phrase,
		tweet_id: data.tweet_id,
	})

	window.location.assign(`/tweet-generator?${params}`)
}

document
.querySelector("#generate-form")
.addEventListener("submit", onSubmit)
