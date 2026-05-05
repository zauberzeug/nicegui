let timeoutId = null;

function scheduleNext(url, clientId, interval) {
  // jitter ±25% so synchronously-loaded clients don't stampede the server
  const jittered = interval * (0.75 + Math.random() * 0.5);
  timeoutId = setTimeout(() => {
    fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ client_id: clientId }),
    })
      .catch((err) => console.debug("heartbeat failed:", err))
      .finally(() => {
        if (timeoutId !== null) scheduleNext(url, clientId, interval);
      });
  }, jittered);
}

self.onmessage = function (e) {
  if (e.data.type === "start") {
    const { url, clientId, interval } = e.data;
    if (timeoutId !== null) clearTimeout(timeoutId);
    scheduleNext(url, clientId, interval);
  } else if (e.data.type === "stop") {
    if (timeoutId !== null) clearTimeout(timeoutId);
    timeoutId = null;
  }
};
