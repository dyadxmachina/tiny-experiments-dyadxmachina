#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A very short example experiment in 16 lines of pure code.
Participants have to indicate the parity of digits by pressing 
the left arrow key for odd and the right arrow key for even numbers.
"""

from expyriment import control, stimuli, design, misc

digit_list = [1, 2, 3, 4, 6, 7, 8, 9] * 12
design.randomize.shuffle_list(digit_list)

exp = control.initialize()
exp.data_variable_names = ["digit", "btn", "rt", "error"]

control.start(exp)

for digit in digit_list:
    target = stimuli.TextLine(text=str(digit), text_size=80)
    exp.clock.wait(500 - stimuli.FixCross().present() - target.preload())
    target.present()
    button, rt = exp.keyboard.wait([misc.constants.K_LEFT, misc.constants.K_RIGHT])
    error = (button == misc.constants.K_LEFT) == digit%2
    if error: stimuli.Tone(duration=200, frequency=2000).play()
    exp.data.add([digit, button, rt, int(error)])
    exp.clock.wait(1000 - stimuli.BlankScreen().present() - target.unload())


radius = 20
movement = [4, 8]
arena = (exp.screen.size[0] // 2 - radius, exp.screen.size[1] // 2 - radius)
dot = stimuli.Circle(radius=radius, colour=misc.constants.C_YELLOW)

stimuli.BlankScreen().present()

exp.clock.reset_stopwatch()
while exp.clock.stopwatch_time < 10000:
    erase = stimuli.Rectangle(size=dot.surface_size, position=dot.position,
                        colour = exp.background_colour)
    dot.move(movement)
    if dot.position[0] > arena[0] or dot.position[0] < -1*arena[0]:
        movement[0] = -1 * movement[0]
    if dot.position[1] > arena[1] or dot.position[1] < -1*arena[1]:
        movement[1] = -1 * movement[1]

    erase.present(clear=False, update=False) # present but do not refesh screen
    dot.present(clear=False, update=True)    # present but do not refesh screen
    exp.screen.update_stimuli([dot, erase])  # refesh screen
    exp.keyboard.check()    # ensure that keyboard input is proccesed
                            # to quit experiment with ESC
    exp.clock.wait(1)

while exp.clock.stopwatch_time < 10000:
    erase = stimuli.Rectangle(size=dot.surface_size, position=dot.position,
                        colour = exp.background_colour)
    dot.move(movement)
    if dot.position[0] > arena[0] or dot.position[0] < -1*arena[0]:
        movement[0] = -1 * movement[0]
    if dot.position[1] > arena[1] or dot.position[1] < -1*arena[1]:
        movement[1] = -1 * movement[1]

    erase.present(clear=False, update=False) # present but do not refesh screen
    dot.present(clear=False, update=True)    # present but do not refesh screen
    exp.screen.update_stimuli([dot, erase])  # refesh screen
    exp.keyboard.check()    # ensure that keyboard input is proccesed
                            # to quit experiment with ESC
    exp.clock.wait(1)

control.end(goodbye_text="Thank you very much...", goodbye_delay=2000)