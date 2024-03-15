// /*
// * Webserial basic demo
// */
'use strict';

// Global variables
let port 
let outputDone
let outputStream 
let reader 
let inputDone 
let inputStream

// check if broswer supports webserial
function check_compatability() {
  if ('serial' in navigator) {
    console.log('webserial supported');
    return true
  } else {
    console.log('webserial not supported');
    return false
    }
}



// Disconnect serial connection
async function disconnect() {
  if (reader) { //close input stream
    await reader.cancel();
    await inputDone.catch(() => {});
    reader = null;
    inputDone = null;
  }
  if (outputStream) { //close output stream
    await outputStream.getWriter().close();
    await outputDone;
    outputStream = null;
    outputDone = null;
  }

  if (port) {
    await port.close();
    port = null;
    console.log('port closed');
  };
  // console.log('made it here');
  return true;
};


// Connect serial port
async function connect() {
    try {
        port = await navigator.serial.requestPort();    
        await port.open({ 'baudRate': 9600 });
    } catch (err) {
        console.log(err);
        return false;
    }
    
    const encoder = new TextEncoderStream();
    outputDone = encoder.readable.pipeTo(port.writable);
    outputStream = encoder.writable;
    
    let decoder = new TextDecoderStream();
    inputDone = port.readable.pipeTo(decoder.writable);
    inputStream = decoder.readable;      
    reader = inputStream.getReader();      
    
    return true;      
}

// Write a character to the stream (and the port)
function writeStream(sendString) {
  const writer = outputStream.getWriter();
  console.log('[SENDING]', sendString);
  writer.write(sendString + '\n');
  writer.releaseLock();
}

// Monitor the port for incoming data. Fire off a custom event
// every time a temperature reading is successfully decoded.
async function readLoop() {
  let fullStr = '';
  while (true) {
    const { value, done } = await reader.read();
    if (value) {
      fullStr += value;
      // Could proably just check the last character instead...
      const res = fullStr.match(/(.*)\r\n/);
      if (res) {
        fullStr = ''; 
        emitEvent('readevent', res[1]);
      }
    }
    if (done) {
      console.log('[readLoop] DONE', done);
      reader.releaseLock();
      break;
    }
  }
  return false;
}
  




