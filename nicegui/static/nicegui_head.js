function createRandomUUID() {
  try {
    return crypto.randomUUID();
  } catch (e) {
    // https://stackoverflow.com/a/2117523/3419103
    return "10000000-1000-4000-8000-100000000000".replace(/[018]/g, (c) =>
      (+c ^ (crypto.getRandomValues(new Uint8Array(1))[0] & (15 >> (+c / 4)))).toString(16)
    );
  }
}
const OLD_TAB_ID = sessionStorage.__nicegui_tab_closed === "false" ? sessionStorage.__nicegui_tab_id : null;
const TAB_ID =
  !sessionStorage.__nicegui_tab_id || sessionStorage.__nicegui_tab_closed === "false"
    ? (sessionStorage.__nicegui_tab_id = createRandomUUID())
    : sessionStorage.__nicegui_tab_id;
sessionStorage.__nicegui_tab_closed = "false";
window.onbeforeunload = function () {
  sessionStorage.__nicegui_tab_closed = "true";
};
function initSocketIO(options) {
  // Initialize window variables needed for socket communication
  window.documentId = createRandomUUID();
  window.clientId = options.query.client_id;
  window.path_prefix = options.prefix;
  window.nextMessageId = options.query.next_message_id;
  window.ackedMessageId = -1;
  // Initialize Socket.IO early
  const url = window.location.protocol === "https:" ? "wss://" : "ws://" + window.location.host;
  window.socket = io(url, {
    path: `${options.prefix}/_nicegui_ws/socket.io`,
    query: options.query,
    extraHeaders: options.extraHeaders,
    transports: options.transports,
  });
  window.did_handshake = false;
  // Queue for messages received before the app is mounted
  window.premountMessageQueue = [];
  window.catchAllHandler = (event, ...args) => {
    if (args.length > 0 && args[0]._id !== undefined) {
      const message_id = args[0]._id;
      if (message_id < window.nextMessageId) return;
      window.nextMessageId = message_id + 1;
      delete args[0]._id;
    }
    premountMessageQueue.push({ event, args });
  };
  window.socket.onAny(window.catchAllHandler); // onAny does not cover "connect", though
  window.socket.on("connect", handleConnect);
}
function handleConnect() {
  if (window.documentId === undefined) { throw new Error("documentId is undefined. You're calling this too early!"); }
  const args = {
    client_id: window.clientId,
    document_id: window.documentId,
    tab_id: TAB_ID,
    old_tab_id: OLD_TAB_ID,
    next_message_id: window.nextMessageId,
  };
  window.socket.emit("handshake", args, (ok) => {
    if (!ok) {
      console.log("reloading because handshake failed for clientId " + window.clientId);
      window.location.reload();
    }
    const popup = document.getElementById("popup");
    if (popup) {
      popup.ariaHidden = true;
    }
  });
  window.did_handshake = true;
}
