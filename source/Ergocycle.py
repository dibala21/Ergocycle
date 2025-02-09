# Main class

# Imports
# from Crankset import Crankset
# from Menu import Menu
# from Motor import Motor
from Screen import Screen as Screen
# from StimulationSignal import StimulationSignal
from Stimulator import Stimulator as Stimulator

import threading

class Ergocycle:

    # Constuctor
    def __init__(self):

        # Dictionary that matches buttons text to functions to be called
        function_dictionary = {
            "Tester événements" : self.test_event,
            "Commander amplitude" : self.command_stimulator
        }

        self.assistance_screen = Screen(function_dictionary)
        # self.crankset = Crankset()
        # self.crankset_measures = {}
        # self.motor = Motor()
        # For now, we will only use one screen to make the implementation easier
        # self.stimulation_screen = Screen()
        self.stimulator = Stimulator("a channel", "a freq", "a ts1", "a ts2", "a mode", "a pulse_width", "an amplitude", "a port_path")

        self.assistance_screen.start_application()
        #self.test_timer()


    def test_event(self):
        print("(Ergocycle) Testing an event")

    def command_stimulator(self):#(self, command)
        self.stimulator.throw_command("Set frequency to " + self.assistance_screen.get_amplitude() + " volts")

    def test_timer(self):
        print("TEST TIMER")
        # threading.Timer(1, test_timer).start()

    def command_assistance_screen(self, command, parameters):
        print("TODO")

    def command_motor(self, commanded_parameter, value):
        print("TODO")

    def command_stimulation_screen(self, command, parameters):
        print("TODO")

    def read_crankset(self):
        print("TODO")
