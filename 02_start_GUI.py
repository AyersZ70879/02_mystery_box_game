from tkinter import *
from functools import partial   # To prevent unwanted windows
import random


class Start:
    def __init__(self, parent):

        # GUI to get starting balances and stakes
        self.start_frame = Frame(padx=10, pady=10, bg="#DDF0FF")
        self.start_frame.grid()

        # Set initial balance to zero
        self.starting_funds = IntVar()
        self.starting_funds.set(0)

        # Mystery Heading (row 0)
        self.mystery_box_label = Label(self.start_frame, text="Mystery Box Game", font="Arial 19 bold", bg="#DDF0FF")
        self.mystery_box_label.grid(row=0)

        # Mystery Box Description (row 1)
        self.mystery_instructions = Label(self.start_frame, text="Please enter a dollar amount "
                                                              "(between $5 and $50) in the box "
                                                              "below. The higher the stakes, the more "
                                                              "you can win!", font="Arial 10 italic", wrap=275,
                                          justify=LEFT, padx=10, pady=10, bg="#DDF0FF")
        self.mystery_instructions.grid(row=1)

        # Entry box and error frame (row 2)
        self.entry_error_frame = Frame(self.start_frame, width=200, bg="#DDF0FF")
        self.entry_error_frame.grid(row=2)

        self.start_amount_entry = Entry(self.entry_error_frame, font="Arial 16 bold")
        self.start_amount_entry.grid(row=0, column=0)

        self.add_funds_button = Button(self.entry_error_frame, font="Arial 14 bold", text="Add Funds",
                                       command=self.check_funds)
        self.add_funds_button.grid(row=0, column=1)

        self.amount_error_label = Label(self.entry_error_frame, fg="maroon", text="", font="Arial 10 bold",
                                        wrap=275, justify=LEFT, bg="#DDF0FF")
        self.amount_error_label.grid(row=1, columnspan=2, pady=5)

        # Button frame (row 3)
        self.stakes_frame = Frame(self.start_frame, bg="#DDF0FF")
        self.stakes_frame.grid(row=3)

        # Buttons go here..
        button_font = "Arial 12 bold"
        # Orange low stakes button...
        self.low_stakes_button = Button(self.stakes_frame, text="Low ($5)", command=lambda: self.to_game(1),
                                       font=button_font, bg="#ED6A5A")
        self.low_stakes_button.grid(row=0, column=0, pady=10)

        # Yellow medium stakes button...
        self.medium_stakes_button = Button(self.stakes_frame, text="Medium ($10)",
                                       command=lambda: self.to_game(2),
                                       font=button_font, bg="#E8E288")
        self.medium_stakes_button.grid(row=0, column=1, padx=5, pady=10)

        # Green high stakes button...
        self.high_stakes_button = Button(self.stakes_frame, text="High ($15)", command=lambda: self.to_game(3),
                                       font=button_font, bg="#8AA894")
        self.high_stakes_button.grid(row=0, column=2, pady=10)

        # Disable all stakes buttons at start
        self.low_stakes_button.config(state=DISABLED)
        self.medium_stakes_button.config(state=DISABLED)
        self.high_stakes_button.config(state=DISABLED)

        # Help Button
        self.help_button = Button(self.start_frame, text="How to Play", bg="#808080", fg="white",
                                  font=button_font)
        self.help_button.grid(row=4, pady=10)

    # check funds function
    def check_funds(self):
        starting_balance = self.start_amount_entry.get()


        # Set error background and colours (and assume no errors at the start
        error_back = "#ffafaf"
        has_errors = "no"

        # Change background to white (fr testing purposes)
        self.start_amount_entry.config(bg="white")
        self.amount_error_label.config(text="")

        # Disable all stakes buttons in case user changes mind and decreases amount entered
        self.low_stakes_button.config(state=DISABLED)
        self.medium_stakes_button.config(state=DISABLED)
        self.high_stakes_button.config(state=DISABLED)

        try:
            starting_balance = int(starting_balance)

            if starting_balance < 5:
                has_errors = "yes"
                error_feedback = "Sorry, the least you can play with is $5"
            elif starting_balance > 50:
                has_errors = "yes"
                error_feedback = "Too high! The most you can risk in this game is $50"

            elif starting_balance >= 15:
                # enable all buttons
                self.low_stakes_button.config(state=NORMAL)
                self.medium_stakes_button.config(state=NORMAL)
                self.high_stakes_button.config(state=NORMAL)

            elif starting_balance >= 10:
                # enable low medium stakes buttons
                self.low_stakes_button.config(state=NORMAL)
                self.medium_stakes_button.config(state=NORMAL)

            else:
                self.low_stakes_button.config(state=NORMAL)

        except ValueError:
            has_errors = "yes"
            error_feedback = "Please enter a dollar amount (not text or decimals)"

        if has_errors == "yes":
            self.start_amount_entry.config(bg=error_back)
            self.amount_error_label.config(text=error_feedback)

        else:
            # set starting balance to amount entered by user
            self.starting_funds.set(starting_balance)

    # to_game function
    def to_game(self, stakes):

        starting_balance = self.starting_funds.get()

        Game(self, stakes, starting_balance)

        # hide start up window
        root.withdraw()


class Game:
    def __init__(self, partner, stakes, starting_balance):
        print(stakes)
        print(starting_balance)


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Mystery Box Game")
    something = Start(root)
    root.mainloop()
