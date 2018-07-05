
from expyriment import design, control, stimuli, io, misc


# Create and initialize an Experiment
exp = design.Experiment("Simon Task")
control.initialize(exp)

# Define and preload standard stimuli
fixcross = stimuli.FixCross()
fixcross.preload()

# Create IO
#response_device = io.EventButtonBox(io.SerialPort("/dev/ttyS1"))
response_device = exp.keyboard

# Create design
for task in ["left key for green", "left key for red"]:
    b = design.Block()
    b.set_factor("Response", task)
    for where in [["left", -300], ["right", 300]]:
        for what in [["red", misc.constants.C_RED],
                     ["green", misc.constants.C_GREEN]]:
            t = design.Trial()
            t.set_factor("Position", where[0])
            t.set_factor("Colour", what[0])
            s = stimuli.Rectangle([50, 50], position=[where[1], 0],
                                  colour=what[1])
            t.add_stimulus(s)
            b.add_trial(t, copies=20)
    b.shuffle_trials()
    exp.add_block(b)
exp.add_bws_factor("ResponseMapping", [1, 2])
exp.data_variable_names = ["Position", "Button", "RT"]

# Start Experiment
control.start()
exp.permute_blocks(misc.constants.P_BALANCED_LATIN_SQUARE)
for block in exp.blocks:
    stimuli.TextScreen("Instructions", block.get_factor("Response")).present()
    response_device.wait()
    for trial in block.trials:
        fixcross.present()
        exp.clock.wait(1000 - trial.stimuli[0].preload())
        trial.stimuli[0].present()
        button, rt = response_device.wait()
        exp.data.add([trial.get_factor("Position"), button, rt])

# End Experiment
control.end()
 SNARC-experiment.py
#!/usr/bin/env python

"""
A parity judgment task to assess the SNARC effect.
See e.g.:
Gevers, W., Reynvoet, B., & Fias, W. (2003). The mental representation of
ordinal sequences is spatially organized. Cognition, 87(3), B87-95.
"""

__author__ = 'Florian Krause <siebenhundertzehn@gmail.com>, \
Oliver Lindemann <lindemann09@gmail.com>'
__version__ = '04-12-2012'


from expyriment import design, control, stimuli
from expyriment.misc import constants


control.set_develop_mode(False)

########### DESIGN ####################
exp = design.Experiment(name="SNARC")

# Design: 2 response mappings x 8 stimuli x 10 repetitions
for response_mapping in ["left_odd", "right_odd"]:
    block = design.Block()
    block.set_factor("mapping", response_mapping)
    #add trials to block
    for digit in [1, 2, 3, 4, 6, 7, 8, 9]:
        trial = design.Trial()
        trial.set_factor("digit", digit)
        block.add_trial(trial, copies=10)
    block.shuffle_trials()
    exp.add_block(block)

exp.add_experiment_info("This a just a SNARC experiment.")
#add between subject factors
exp.add_bws_factor('mapping_order', ['left_odd_first', 'right_odd_first'])
#prepare data output
exp.data_variable_names = ["block", "mapping", "trial", "digit", "ISI",
                           "btn", "RT", "error"]

#set further variables
t_fixcross = 500
min_max_ISI = [200, 750] # [min, max] inter_stimulus interval
ITI = 1000
t_error_screen = 1000
no_training_trials = 10

######### INITIALIZE ##############
control.initialize(exp)

# Prepare and preload some stimuli
blankscreen = stimuli.BlankScreen()
blankscreen.preload()
fixcross = stimuli.FixCross()
fixcross.preload()
error_beep = stimuli.Tone(duration=200, frequency=2000)
error_beep.preload()

#define a trial
def run_trial(cnt, trial):
    # present Fixation cross and prepare trial in the meantime
    fixcross.present()
    exp.clock.reset_stopwatch()
    ISI = design.randomize.rand_int(min_max_ISI[0], min_max_ISI[1])
    digit = trial.get_factor("digit")
    target = stimuli.TextLine(text=str(digit), text_size=60)
    target.preload()
    exp.clock.wait(t_fixcross - exp.clock.stopwatch_time)
    #presesnt blankscreen for a random interval
    blankscreen.present()
    exp.clock.wait(ISI)
    # Present target & record button response
    target.present()
    btn, rt = exp.keyboard.wait([constants.K_LEFT, constants.K_RIGHT])
    #Error feedback if required
    if block.get_factor("mapping") == "left_odd":
        error = (digit % 2 == 0 and btn == constants.K_LEFT) or \
                (digit % 2 == 1 and btn == constants.K_RIGHT)
    else:
        error = (digit % 2 == 1 and btn == constants.K_LEFT) or \
                (digit % 2 == 0 and btn == constants.K_RIGHT)
    if error:
        error_beep.present()
    #write data and clean up while inter-trial-interval
    blankscreen.present()
    exp.clock.reset_stopwatch()
    exp.data.add([block.id, block.get_factor("mapping"),
                  cnt, target.text, ISI,
                  btn, rt, int(error)])
    exp.data.save()
    target.unload()
    exp.clock.wait(ITI - exp.clock.stopwatch_time)


######### START ##############
control.start(exp)

# permute block order across subjects
if exp.get_permuted_bws_factor_condition('mapping_order') == "right_odd_first":
    exp.swap_blocks(0, 1)

# Run the actual experiment
for block in exp.blocks:
    # Show instruction screen
    if block.get_factor("mapping") == "left_odd":
        instruction = "Press LEFT arrow key for ODD\n" + \
                            "and RIGHT arrow key for EVEN numbers."
    else:
        instruction = "Press RIGHT arrow key for ODD\n" + \
                            "and LEFT arrow key for EVEN numbers."
    stimuli.TextScreen("Indicate the parity of the numbers", instruction +
                       "\n\nPress space bar to start training.").present()
    exp.keyboard.wait(constants.K_SPACE)
    #training trials
    for cnt in range(0, no_training_trials):
        trial = block.get_random_trial()
        run_trial(-1 * cnt, trial)#training trails has negative trial numbers
    # Show instruction screen
    stimuli.TextScreen("Attention!", instruction +
                       "\n\nThe experimental block starts now.").present()
    exp.keyboard.wait(constants.K_SPACE)
    # experimental trials
    for cnt, trial in enumerate(block.trials):
        run_trial(cnt, trial)


####### END EXPERIMENT ########
control.end(goodbye_text="Thank you very much for participating in our experiment",
             goodbye_delay=5000)