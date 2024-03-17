let port;
let outputDone;
let outputStream;
let inputDone;
let inputStream;
let reader;

async function connect() {
  try {
    port = await navigator.serial.requestPort();
    await port.open({ baudRate: 115200 });
  } catch (err) {
    console.log(err);
    return false;
  }

  const encoder = new TextEncoderStream();
  outputDone = encoder.readable.pipeTo(port.writable);
  outputStream = encoder.writable;

  const decoder = new TextDecoderStream();
  inputDone = port.readable.pipeTo(decoder.writable);
  inputStream = decoder.readable;
  reader = inputStream.getReader();

  return true;
}

async function disconnect() {
  if (reader) {
    await reader.cancel();
    await inputDone.catch(() => {});
    reader = null;
    inputDone = null;
  }
  if (outputStream) {
    await outputStream.getWriter().close();
    await outputDone;
    outputStream = null;
    outputDone = null;
  }
  if (port) {
    await port.close();
    port = null;
  }
}

function send(message) {
  const writer = outputStream.getWriter();
  writer.write(message + "\n");
  writer.releaseLock();
}

async function readLoop() {
  let fullStr = "";
  while (true) {
    const { value, done } = await reader.read();
    if (value) {
      fullStr += value;
      const res = fullStr.match(/(.*)\r\n/);
      if (res) {
        fullStr = "";
        emitEvent("read", res[1]);
      }
    }
    if (done) {
      reader.releaseLock();
      break;
    }
  }
}
