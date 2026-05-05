let intervalId = null;
let inFlight = false;

self.onmessage = function (e) {
  if (e.data.type === "start") {
    const { url, clientId, interval } = e.data;
    if (intervalId) clearInterval(intervalId);
    intervalId = setInterval(() => {
      if (inFlight) return; // skip while a previous heartbeat is still pending
      inFlight = true;
      fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ client_id: clientId }),
      })
        .catch((err) => console.debug("heartbeat failed:", err))
        .finally(() => {
          inFlight = false;
        });
    }, interval);
  } else if (e.data.type === "stop") {
    if (intervalId) clearInterval(intervalId);
    intervalId = null;
    inFlight = false;
  }
};
