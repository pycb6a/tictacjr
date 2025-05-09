# TicTac Junior

**TicTac Junior** is a Python library for creating Scratch Junior-style projects using code.
It’s designed to help learners smoothly transition from Scratch Junior to text-based programming.

With TicTac Junior, you write familiar Scratch Junior-like logic using pure Python.
It’s great for children, educators, and anyone beginning their Python journey.

## 🎯 Core Idea

> Write a Python program - get a result that feels like Scratch Junior.

## 🧩 Example

```python
import tictacjr.en as tj


project = tj.Project()
project.title = "My TicTac Project"
project.set_grid()

page = tj.Page()
project.pages += page
page.background = tj.Background.PARK

label = tj.Label()
page.labels += label
label.text = "My TicTac Text"
label.color = tj.Color.WHITE
label.size = tj.TextSize.AA
label.x = 20
label.y = 25

tic = tj.Character()
page.characters += tic
tic.costume = tj.Costume.TIC
tic.size = tj.Size.M
tic.x = 20
tic.y = 15

script = tj.Script()
tic.scripts += script

(
    script.start_on_green_flag()
    .say("Hello World!")
    .move_right(5)
    .move_left(5)
    .turn_left(3)
    .turn_right(6)
    .turn_left(3)
    .hop()
    .say("Bye!")
    .go_home()
)

project.start()
```

## 🧱 Available Blocks

See the full list of available blocks in [`tictacjr/core/block.py`](https://github.com/pycb6a/tictacjr/blob/main/tictacjr/core/block.py).

These define the core actions (move, turn, say, wait, repeat, etc.) that mimic Scratch Junior's behavior in Python code.

## 💡 Inspiration

TicTac Junior draws inspiration from:
- [Scratch](https://scratch.mit.edu)
- [Scratch Junior](https://www.scratchjr.org/)
- [Scratch Junior Desktop](https://github.com/jfo8000/ScratchJr-Desktop)
- [PyStage](https://github.com/pystage/pystage)
- [Pygame projects](https://www.pygame.org/news)

## 🚧 TODO

- Add Event.START_ON_MESSAGE / _ControlAction.send_message
- Add support for multiple Pages on Stage
- Add _ControlAction.go_to_page
- Add Ukrainian localization
- Add documentation
- Add _ControlAction.stop
- Add _ControlAction.speed
- Add Event.START_ON_BUMP
- Add _SoundAction.pop
- Add support for custom characters/backgrounds
