async function previewReel() {
  const url = document.getElementById("reelUrl").value.trim();
  const adsSection = document.getElementById("adsSection");
  const videoPreview = document.getElementById("videoPreview");
  const downloadSection = document.getElementById("downloadSection");
  const downloadBtn = document.getElementById("downloadBtn");

  // Reset UI
  adsSection.classList.add("hidden");
  videoPreview.classList.add("hidden");
  downloadSection.classList.add("hidden");
  videoPreview.innerHTML = "";

  if (!url || !url.startsWith("https://www.instagram.com/reel/")) {
    videoPreview.classList.remove("hidden");
    videoPreview.innerHTML = `<p style="color:red;">⚠️ Please enter a valid Instagram Reel URL.</p>`;
    return;
  }

  try {
    videoPreview.classList.remove("hidden");
    videoPreview.innerHTML = `<p style="color:#555;">⏳ Fetching reel... Please wait.</p>`;

    const res = await fetch("/get_reel", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ url }),
    });

    const data = await res.json();

    if (data.video_url) {
      adsSection.classList.remove("hidden");
      downloadSection.classList.remove("hidden");

      const videoSrc = data.video_url;

      videoPreview.innerHTML = `
        <h3>Reel Preview:</h3>
        <video controls autoplay muted>
          <source src="${videoSrc}" type="video/mp4">
          Your browser does not support HTML5 video.
        </video>
      `;

      downloadBtn.href = videoSrc;
    } else {
      videoPreview.innerHTML = `<p style="color:red;">❌ Could not extract reel. Please make sure it is a <strong>public reel</strong>.</p>`;
    }
  } catch (err) {
    console.error(err);
    videoPreview.innerHTML = `<p style="color:red;">⚠️ An error occurred. Please try again later.</p>`;
  }
}
