import serial
from js import navigator
from pyodide.ffi import to_js
from pyodide.ffi.wrappers import add_event_listener


# Utility function for converting py dicts to JS objects
def j(obj):
    return to_js(obj, dict_converter=js.Object.fromEntries)


class SerialManager:
    async def askForSerial(self):
        self.port = await navigator.serial.requestPort()
        await self.port.open(j({"baudRate": 9600}))
        js.console.log("OPENED PORT")

        self.encoder = js.TextEncoderStream.new()
        outputDone = self.encoder.readable.pipeTo(self.port.writable)

        # Set up listening for incoming bytes
        self.decoder = js.TextDecoderStream.new()
        inputDone = self.port.readable.pipeTo(self.decoder.writable)
        inputStream = self.decoder.readable

        self.reader = inputStream.getReader()
        await self.listenAndEcho()

    async def writeToSerial(self, data):
        outputWriter = self.encoder.writable.getWriter()
        outputWriter.write(data + "\n")
        outputWriter.releaseLock()
        js.console.log(f"Wrote to stream: {data}")

    async def listenAndEcho(self):
        """Loop forever, echoing values received on the serial port to the JS console"""
        receivedValues = []
        while True:
            response = await self.reader.read()
            value, done = response.value, response.done
            if (
                "\r" in value or "\n" in value
            ):  # Output whole line and clear buffer when a newline is received
                print(f"Received from Serial: {''.join(receivedValues)}")
                receivedValues = []
            elif value:  # Output individual characters as they come in
                print(f"Char: {value}")
                receivedValues.append(value)


sm = SerialManager()


async def sendValueFromInputBox(sm: SerialManager):
    """Get the value"""
    textInput = js.document.getElementById("text")
    value = textInput.value
    textInput.value = ""

    await sm.writeToSerial(value)
