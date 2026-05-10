const summarizeBtn = document.getElementById("summarizeBtn");
const resultDiv = document.getElementById("result");
const loadingDiv = document.getElementById("loading");

summarizeBtn.addEventListener("click", async () => {

    loadingDiv.classList.remove("hidden");

    resultDiv.innerHTML = "";

    try {

        const [tab] = await chrome.tabs.query({
            active: true,
            currentWindow: true
        });

        const currentUrl = tab.url;

        const response = await fetch(
            `https://reddit-summarizer-zjaf.onrender.com/api/summarize?url=${encodeURIComponent(currentUrl)}`
        );

        const data = await response.json();

        resultDiv.innerHTML = `
            <h2>${data.title}</h2>
            <p>${data.summary}</p>
        `;

    } catch (error) {

        console.error(error);

        resultDiv.innerHTML =
            "Failed to summarize Reddit post.";

    }

    loadingDiv.classList.add("hidden");
});