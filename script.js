const shareBtn = document.getElementById('shareBtn');
const nameInput = document.getElementById('nameInput');
const statusLine = document.getElementById('statusLine');
const radar = document.getElementById('radar');
const pinIcon = document.getElementById('pinIcon');
const resultBox = document.getElementById('resultBox');
const resultTitle = document.getElementById('resultTitle');
const resultBody = document.getElementById('resultBody');

shareBtn.onclick = () => {
  const name = nameInput.value.trim();
  if (!name) {
    nameInput.focus();
    nameInput.style.borderColor = 'var(--red)';
    statusLine.textContent = 'Pehle apna naam likhein';
    return;
  }
  nameInput.style.borderColor = '';

  if (!navigator.geolocation) {
    showResult(false, 'Supported nahi', 'Yeh browser location share nahi kar sakta.');
    return;
  }

  shareBtn.disabled = true;
  shareBtn.textContent = 'Permission ka intezaar...';
  radar.classList.add('animate');
  statusLine.textContent = 'Browser permission maang raha hai...';

  navigator.geolocation.getCurrentPosition(
    async (pos) => {
      radar.classList.remove('animate');
      pinIcon.classList.add('drop');
      statusLine.textContent = 'Location mil gayi';

      const { latitude, longitude, accuracy } = pos.coords;

      try {
        const res = await fetch('/checkin', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name, lat: latitude, lng: longitude, accuracy }),
        });
        const data = await res.json();

        if (data.ok) {
          showResult(
            true,
            '✓ Location Telegram par bhej di gayi',
            `${latitude.toFixed(5)}, ${longitude.toFixed(5)}\n±${Math.round(accuracy)}m accuracy`
          );
        } else {
          showResult(false, 'Bhej nahi payi', 'Server par kuch gadbad hui.');
        }
      } catch (e) {
        showResult(false, 'Bhej nahi payi', 'Server tak pahunch nahi paya.');
      }

      shareBtn.disabled = false;
      shareBtn.textContent = 'Meri Location Share Karein';
    },
    (err) => {
      radar.classList.remove('animate');
      shareBtn.disabled = false;
      shareBtn.textContent = 'Meri Location Share Karein';
      let msg = 'Location nahi mil payi.';
      if (err.code === err.PERMISSION_DENIED) msg = 'Permission deny ki gayi. Share karne ke liye allow karna zaroori hai.';
      else if (err.code === err.TIMEOUT) msg = 'Time out ho gaya, dobara try karein.';
      statusLine.textContent = 'Nahi mila';
      showResult(false, 'Nahi ho paya', msg);
    },
    { enableHighAccuracy: true, timeout: 12000, maximumAge: 0 }
  );
};

function showResult(ok, title, body) {
  resultBox.classList.add('show');
  resultBox.classList.toggle('error', !ok);
  resultTitle.textContent = title;
  resultBody.textContent = body;
}
