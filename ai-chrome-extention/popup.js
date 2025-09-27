document.getElementById("askBtn").addEventListener("click", async () => {
  // Get active tab URL dynamically
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const url = tab.url;
  const query = document.getElementById("query").value;

  // Call your backend
  const response = await fetch("http://localhost:8000/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url, query })
  });

  const data = await response.json();
  document.getElementById("answer").innerText = data.answer;
});
