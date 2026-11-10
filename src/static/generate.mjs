const onSubmit = async (event) => {
	event.preventDefault()
	const form = event.currentTarget

	const response = await fetch(
		form.action,
		{method: "POST"},
	)

	const data = await response.json()
	if (!response.ok) throw new Error(
		data.error ?? "Request failed."
	)

	const params = new URLSearchParams({
		phrase: data.phrase,
		tweet_id: data.tweet_id,
	})

	window.location.assign(`/tweet-generator?${params}`)
}

document
.querySelector("#generate-form")
.addEventListener("submit", onSubmit)
