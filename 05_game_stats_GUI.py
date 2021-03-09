from tkinter import *
from functools import partial   # To prevent unwanted windows

import random


class Game:
    def __init__(self):

        # Formatting variables...
        self.game_stats_list = [50, 6]

        self.round_stats_list = []

        self.game_frame = Frame()
        self.game_frame.grid()

        # Heading Row
        self.heading_label = Label(self.game_frame, text="Play...", font="Arial 24 bold",
                                   padx=10, pady=10)
        self.heading_label.grid()

        # History Button (row 1)
        self.stats_button = Button(self.game_frame, text="Game Stats",
                                   font="Arial 14", padx=10, pady=10,
                                   command=lambda: self.to_stats(self.round_stats_list, self.game_stats_list))
        self.stats_button.grid(row=1)

    def to_stats(self, game_history, game_stats):
        GameStats(self, game_history, game_stats)


class GameStats:
    def __init__(self, partner, game_history, game_stats):

        print(game_history)

        # disable stats button
        partner.stats_button.config(state=DISABLED)

        heading = "Arial 12 bold"
        content = "Arial 12"

        # Sets up child windows (ie: help box)
        self.stats_box = Toplevel()

        # If users press cross at top, closes help and 'releases' button

        self.stats_box.protocol('WM_DELETE_WINDOW', partial(self.close_stats, partner))

        # Set up GUI Frame
        self.stats_frame = Frame(self.stats_box)
        self.stats_frame.grid()

        # Set up a Help heading (row 0)
        self.stats_heading_label = Label(self.stats_frame, text="Game Stats",
                                         font="arial 19 bold")
        self.stats_heading_label.grid(row=0)

        # To export <instructions> (row 1)
        self.export_instructions = Label(self.stats_frame,
                                         text="Here are your Game Stats."
                                              "Please use the Export Button to"
                                              "access the results of each round"
                                              "that you played.", font="arial 10 italic",
                                         justify=LEFT, fg="green", padx=10, pady=10)
        self.export_instructions.grid(row=1)

        # Starting Balance (row 2)
        self.details_frame = Frame(self.stats_frame)
        self.details_frame.grid(row=2)

        # Starting balance (row 2.0)

        self.start_balance_label = Label(self.details_frame, text="Starting Balance",
                                         font=heading, anchor="e")
        self.start_balance_label.grid(row=0, column=0, padx=0)

        self.start_balance_value_label = Label(self.details_frame, font=content,
                                               text="${}".format(game_stats[0]),
                                               anchor="w")
        self.start_balance_value_label.grid(row=0, column=1, padx=0)

        # Current Balance (row 2.2)
        self.current_balance_label = Label(self.details_frame, text="Current Balance: ",
                                           font=heading, anchor="e")
        self.current_balance_label.grid(row=1, column=0, padx=0)

        self.current_balance_value_label = Label(self.details_frame, font=content,
                                                 text="${}".format(game_stats[1]))
        self.current_balance_value_label.grid(row=1, column=1, padx=0)

        if game_stats[1] > game_stats[0]:
            win_loss = "Amount Won:"
            amount = game_stats[1] - game_stats[0]
            win_loss_fg = "green"
        else:
            win_loss = "Amount Lost:"
            amount = game_stats[0] - game_stats[1]
            win_loss_fg = "#660000"

        # Amount won/lost (row 2.3)
        self.win_loss_label = Label(self.details_frame, text=win_loss,
                                    font=heading, anchor="e")
        self.win_loss_label.grid(row=2, column=0, padx=0)

        self.win_loss_value_label = Label(self.details_frame, font=content,
                                          text="${}".format(amount), fg=win_loss_fg,
                                          anchor="w")
        self.win_loss_value_label.grid(row=2, column=1, padx=0)

        # Rounds Played (row 2.4)
        self.games_played_label = Label(self.details_frame, text="Rounds Played:",
                                        font=heading, anchor="e")
        self.games_played_label.grid(row=4, column=0, padx=0)

        self.games_played_value_label = Label(self.details_frame, font=content,
                                              text=len(game_history), anchor="w")
        self.games_played_value_label.grid(row=4, column=1, padx=0)

        # Export Button
        self.export_button = Button(self.details_frame, text="Export", font="Arial 15 bold",
                                  bg="#808080", fg="white", command=self.export)
        self.export_button.grid(row=6, padx=2)

        # Dismiss Button (row 3)
        self.dismiss_button = Button(self.details_frame, text="Quit", fg="white", bg="#660000", font="Arial 15 bold",
                                  width=20, command=self.close_stats, padx=10, pady=10)
        self.dismiss_button.grid(row=6, pady=10)

    def export(self):
        get_export = Export(self, self.games_played_label, self.current_balance_label)

    def close_stats(self, partner):
        # Put stats button back to normal...
        partner.stats_button.config(state=NORMAL)
        self.stats_box.destroy()


# Export section
class Export:
    def __init__(self, partner, game_history, all_game_stats):

        print(game_history)

        # Disable export button
        partner.export_button.config(state=DISABLED)

        # Sets up child window (ie: export box)
        self.export_box = Toplevel()

        # If users press cross at top, closes export and 'releases' export button
        self.export_box.protocol('WM_DELETE_WINDOW', partial(self.close_export, partner))

        # Set up GUI frame
        self.export_frame = Frame(self.export_box, width=300)
        self.export_frame.grid()

        # Set up export heading (row 0)
        self.how_heading = Label(self.export_frame, text="Export / Instructions", font="arial 14 bold")
        self.how_heading.grid(row=0)

        # Export Instructions (label, row 1)
        self.export_text = Label(self.export_frame, text="Enter a filename in the box below and press the "
                                                         "Save button to save your calculation history to "
                                                         "text file.", justify=LEFT, width=40, wrap=250)
        self.export_text.grid(row=1)

        # Warning text (label, row 2)
        self.export_text = Label(self.export_frame, text="If the filename you enter below already exists, "
                                                         "its contents will be replaced with your calculation "
                                                         "history", justify=LEFT, bg="#ffafaf", fg="maroon",
                                 font="Arial 10 italic", wrap=225, padx=10, pady=10)
        self.export_text.grid(row=2, pady=10)

        # Filename Entry Box (row 3)
        self.filename_entry = Entry(self.export_frame, width=20, font="Arial 14 bold", justify=CENTER)
        self.filename_entry.grid(row=3, pady=10)

        # Error Message Labels (initially blank, row 4)
        self.save_error_label = Label(self.export_frame, text="", fg="maroon")
        self.save_error_label.grid(row=4)

        # Save / Cancel Frame (row 5)
        self.save_cancel_frame = Frame(self.export_box)
        self.save_cancel_frame.grid(row=5, pady=10)

        # Save and Cancel Buttons (row 0 of save_cancel_frame)
        self.save_button = Button(self.save_cancel_frame, text="Save", font="Arial 15 bold", bg="#003366",
                                  fg="white", command=partial(lambda: self.save_history(partner, game_history, all_game_stats)))
        self.save_button.grid(row=0, column=1)

    def close_export(self, partner):
        # Put stats button back to normal...
        partner.stats_button.config(state=NORMAL)
        self.export_box.destroy()

    def save_history(self, partner, game_history, game_stats):

        # Regular expression to check filename is valid
        valid_char = "[A-Za-z0-9_]"
        has_error = "no"

        filename = self.filename_entry.get()
        print(filename)

        for letter in filename:
            if re.match(valid_char, letter):
                continue
            elif letter == " ":
                problem = "(no spaces allowed)"

            else:
                problem = ("(no {}'s allowed)".format(letter))
            has_error = "yes"
            break

        if filename == "":
            problem = "can't be blank"
            has_error = "yes"

        if has_error == "yes":
            self.filename_entry.config(bg="#ffafaf")
            print()

        else:
            # If there are no errors, generate text filename and then close dialogue
            # add .txt suffix
            filename = filename + ".txt"

            # Create file to hold data
            f = open(filename, "w+")

            # Heading for stats
            f.write("Game Statistics\n\n")

            # Game stats
            for round in game_stats:
                f.write("\nRound Details\n\n")

            # Add new line at end of each item
            for item in game_history:
                f.write(item + "\n")

            # close file
            f.close()

# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Mystery Box Game")
    something = Game()
    root.mainloop()
