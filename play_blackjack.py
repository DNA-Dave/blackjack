from Blackjack import Blackjack
import signal

# This short file simply is run to play blackjack. It creates a blackjack game instance and runs it

def signal_handling(signum,frame):
    # this is the signal handler that allows a control-C to be caught and allows the program to exit gracefully
    print("")
    print("Quitting, thanks for playing!")
    quit()

signal.signal(signal.SIGINT, signal_handling)
new_game = Blackjack()
new_game.start_game()