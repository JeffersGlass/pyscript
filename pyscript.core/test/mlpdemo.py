import time
time.time = lambda : 0

from microMLP import MicroMLP
from binascii import unhexlify

from pyscript import window

colors = []

for line in data.split("\n"):
    if not line: continue
    _, name, _, r, g, b = line.split(",")
    colors.append([name, r, g, b])

print("loaded colors")

num_colors = len(colors)
for i, color in enumerate(colors):
  color.append(i / num_colors)



mlp = MicroMLP.Create( neuronsByLayers           = [3, 50, 50, 50, 50, len(colors)],
                      activationFuncName        = MicroMLP.ACTFUNC_TANH,
                      layersAutoConnectFunction = MicroMLP.LayersFullConnect )

print("constructed")

for color in colors:
  if not line: continue
  print("Processing ", line)
  _, r, g, b, index = color
  mlp.AddExample( [r, g, b], [index] )

learnCount = mlp.LearnExamples()

print("learned!")

last_guess = ""

# Construct Chart

window.console.log(window.c)
window.c.config._config.data.labels[0] = "FOOO"
window.c.update() ### TODO Use this strategy to set data on the JS side, using a JS function that gets passed ints or similar

def guess_color(event):
  value = elem.value
  print(f"The color changed to: {value}")

  r, g, b = int("0x" + value[1:3]), int("0x" + value[3:5]), int("0x" + value[5:7])
  print(r, g, b)

  data = [MicroMLP.NNValue.FromAnalogSignal(val) for val in (r, g, b)]
  float_predictions = [val.AsFloat for val in mlp.Predict(data)]
  closest_index = float_predictions.index(max(float_predictions))
  closest_color = colors[closest_index][0]

  global last_guess

  if True: #closest_color != last_guess:
    print(f"This color is closest to {closest_color}")
    last_guess = closest_color

from js import document
elem = document.getElementById("main-color")
elem.oninput = guess_color