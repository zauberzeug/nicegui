let intervalId = null;

self.onmessage = function (e) {
  if (e.data.type === "start") {
    const { url, clientId, interval } = e.data;
    if (intervalId) clearInterval(intervalId);
    intervalId = setInterval(() => {
      fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ client_id: clientId }),
      }).catch(() => {});
    }, interval);
  } else if (e.data.type === "stop") {
    if (intervalId) clearInterval(intervalId);
    intervalId = null;
  }
};
