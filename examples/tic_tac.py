import tictacjr.en as tj

# Create a new project and configure the window, title, and grid
project = tj.Project()
project.title = "My TicTac Project"
project.window = 40, 30
project.set_grid()

# Create a page and add it to the project
page = tj.Page()
project.pages += page
page.background = tj.Background.PARK

# Add a label to the page and set its properties
label = tj.Label()
page.labels += label
label.text = "My TicTac Text"
label.color = tj.Color.WHITE
label.size = tj.TextSize.AA
label.x = 20
label.y = 25

# Add the first character (tic) to the page and configure
tic = tj.Character()
page.characters += tic
tic.costume = tj.Costume.TIC
tic.size = tj.Size.M
tic.x = 15
tic.y = 15

# Add a script to tic
script = tj.Script()
tic.scripts += script

(
    script.start_on_tap()
    .say("Hello World!")
    .move_right(5)
    .move_left(5)
    .turn_left(3)
    .turn_right(6)
    .turn_left(3)
    .wait(2)
    .say("Bye!")
)

# Add the second character (tac) and configure
tac = tj.Character()
page.characters += tac
tac.costume = tj.Costume.TAC
tac.size = tj.Size.XS
tac.x = 5
tac.y = 5

# Add a script to tac
script = tj.Script()
tac.scripts += script
my_block = (
    script.make_block()
    .move_up(2)
    .move_down(2)
    .hide()
    .wait(2)
    .show()
)
(
    script.start_on_green_flag()
    .do_block(my_block)
    .start_repeat()
    .hop()
    .repeat(3)
)

# Add the third character (toc) and configure
toc = tj.Character()
page.characters += toc
toc.costume = tj.Costume.TOC
toc.size = tj.Size.L
toc.x = 30
toc.y = 20

# Add a script to toc
script = tj.Script()
toc.scripts += script
(
    script.start_on_tap()
    .grow(2)
    .shrink(3)
    .turn_left(5)
    .go_home()
    .reset_size()
)

# Start the project
project.start()
