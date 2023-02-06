Yes and no! Yes, it's possible to implement serial communication with a Micropython-based microprocessor; but no, it's not as simple as `import serial`.

Why isn't it that simple? The `pyserial` package, for example, or the `UART` class in Micropython, have to make certain assumptions about the underlying operating system that allows serial functionality to work. Those assumptions don't hold up inside a browser window/WASM environment. Even some packages that are pure Python with no C extensions, and so *should* run within the context of a Python interpreter, don't, because of [the limitations of the environment](https://pyodide.org/en/stable/usage/wasm-constraints.html).

But just as the Browser taketh away, the Browser also giveth. The [WebSerial API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Serial_API) provides access to native serial devices from within the Browser... sometimes. As that page notes, this is an experimental feature of *some* browsers, and only works in secure contexts (https).

But where it works, it works! There's some adaptation to be done to make things interface nicely with Python, but here's a quick demo I whipped up, helped quite a bit by [this Codelabs tutorial](https://codelabs.developers.google.com/codelabs/web-serial#3) and [this example on GitHub](https://github.com/UnJavaScripter/web-serial-example/blob/master/src/serial-handler.ts).

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>WebSerial Demo</title>
    <script defer src="https://pyscript.net/releases/2022.12.1/pyscript.js"></script>
    <link rel="stylesheet" href="https://pyscript.net/releases/2022.12.1/pyscript.css">
</head>
<body>
    <py-script src="webserialdemo.py"></py-script>

    <button py-click="sm.askForSerial()" id="open">Open a Serial Port</button>

    <br><input type="text" id="text">
    <button py-click ="sendValueFromInputBox(sm)" id="write">Write to the serial port</button>
</body>
</html>
```


```python
# webserialdemo.py
from js import navigator
from pyodide.ffi import to_js
from pyodide.ffi.wrappers import add_event_listener

#Utility function for converting py dicts to JS objects
def j(obj):
    return to_js(obj, dict_converter=js.Object.fromEntries)

class SerialManager():
    '''
    Class for managing reads and writes to/from a serial port
    Not very clean! No error handling, no way to stop listening etc.
    '''

    async def askForSerial(self):
        '''
        Request that the user select a serial port, and initialize
        the reader/writer streams with it
        '''
        self.port = await navigator.serial.requestPort()
        await self.port.open(j({"baudRate": 9600}))
        js.console.log("OPENED PORT")

        # Set up encoder to write to port
        self.encoder = js.TextEncoderStream.new()
        outputDone = self.encoder.readable.pipeTo(self.port.writable)

        # Set up listening for incoming bytes
        self.decoder = js.TextDecoderStream.new()
        inputDone = self.port.readable.pipeTo(self.decoder.writable)
        inputStream = self.decoder.readable

        self.reader = inputStream.getReader();
        await self.listenAndEcho()

    async def writeToSerial(self, data):
        '''Write to the serial port'''
        outputWriter = self.encoder.writable.getWriter()
        outputWriter.write(data + '\n')
        outputWriter.releaseLock()
        js.console.log(f"Wrote to stream: {data}")

    async def listenAndEcho(self):
        '''Loop forever, echoing values received on the serial port to the JS console'''
        receivedValues = []
        while (True):
            response = await self.reader.read()
            value, done = response.value, response.done
            if ('\r' in value or '\n' in value):
                #Output whole line and clear buffer when a newline is received
                print(f"Received from Serial: {''.join(receivedValues)}")
                receivedValues = []
            elif (value):
                #Output individual characters as they come in
                print(f"Char: {value}")
                receivedValues.append(value)

#Create an instance of the SerialManager class when this script runs
sm = SerialManager()

#A helper function - to point the py-click attribute of one of our buttons to
async def sendValueFromInputBox(sm: SerialManager):
    '''
    Get the value of the input box and write it to serial
    Also clears the input box
    '''
    textInput = js.document.getElementById("text")
    value = textInput.value
    textInput.value = ''

    await sm.writeToSerial(value)
```

If you want to see it in action with real hardware, I tested this with the following snippet of code on an Arduino Uno I had at hand:

```c++
// serialEcho.ino - to run on an Arduino Uno
// Echos back whatever is written to the serial port, with a small delay
void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0){
    int incomingByte = Serial.read();
    delay(100);
    Serial.print(char(incomingByte));
  }
}
```
