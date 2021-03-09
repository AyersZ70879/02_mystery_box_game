from tkinter import *
from functools import partial   # To prevent unwanted windows
import random


# Start Section
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


    # check funds function
    def check_funds(self):
        starting_balance = self.start_amount_entry.get()

        # Set error background and colours (and assume no errors at the start
        error_back = "#ffafaf"
        has_errors = "no"

        # Change background to white
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


# Game Section
class Game:
    def __init__(self, partner, stakes, starting_balance):

        # initialise variables
        self.balance = IntVar()

        # Set starting balance to amount entered by the user at the start if the game
        self.balance.set(starting_balance)

        # Get value of stakes (use it as a multiplier when calculator winnings
        self.multiplier = IntVar()
        self.multiplier.set(stakes)

        # List for holding stats
        self.round_stats_list = []
        self.game_stats_list = []

        # Stats list
        self.game_stats_list.append(starting_balance)
        self.game_stats_list.append(0)

        # GUI Setup
        self.game_box = Toplevel()
        self.game_frame = Frame(self.game_box, bg="#DDF0FF")
        self.game_frame.grid()

        # If user press cross at top, game quits
        self.game_box.protocol('WM_DELETE_WINDOW', self.to_quit)

        self.game_frame = Frame(self.game_box, bg="#DDF0FF")
        self.game_frame.grid()

        # Heading Row
        self.heading_label = Label(self.game_frame, text="Play...", font="Arial 24 bold",
                                   padx=10, pady=10, bg="#DDF0FF")
        self.heading_label.grid(row=0)

        # Instructions Label
        self.instructions_label = Label(self.game_frame, wrap=300, justify=LEFT, bg="#DDF0FF", text="Press 'Open "
                                                                                      "Boxes' button or press <enter> "
                                                                                                    "to reveal the"
                                                                                      " contents of the mystery boxes.")
        self.instructions_label.grid(row=1)

        # Boxes go here (row 2)

        self.box_frame = Frame(self.game_frame, bg="#DDF0FF")
        self.box_frame.grid(row=2, pady=10)

        photo = PhotoImage(file="question.gif")

        self.prize1_label = Label(self.box_frame, image=photo,
                                  padx=10, pady=10)
        self.prize1_label.photo = photo
        self.prize1_label.grid(row=0, column=0)

        self.prize2_label = Label(self.box_frame, image=photo,
                                   padx=10, pady=10)
        self.prize2_label.photo = photo
        self.prize2_label.grid(row=0, column=1, padx=10)

        self.prize3_label = Label(self.box_frame, image=photo,
                                  padx=10, pady=10)
        self.prize3_label.photo = photo
        self.prize3_label.grid(row=0, column=2)

        # Play button goes here (row 3)
        self.play_button = Button(self.game_frame, text="Open Boxes", bg="#FDEA9B", font="Arial 15 bold",
                                  width=20, padx=10, pady=10, command=self.reveal_boxes)

        # bind button to <enter> (users can push to reveal the boxes)
        self.play_button.focus()
        self.play_button.bind('<Return>', lambda e: self.reveal_boxes())
        self.play_button.grid(row=3)

        # Balance label (row 4)

        start_text = "Game Cost: ${} \n"" \nHow much will you win".format(stakes*5)

        self.balance_label = Label(self.game_frame, font="Arial 12 bold", fg="green",
                                   text=start_text, wrap=300, justify=LEFT, bg="#DDF0FF")
        self.balance_label.grid(row=4, pady=10)

        # Help and Game stats button (row 5)
        self.help_export_frame = Frame(self.game_frame, bg="#DDF0FF")
        self.help_export_frame.grid(row=5, pady=10)

        self.help_button = Button(self.help_export_frame, text="Help / Rules", font="Arial 15 bold",
                                  bg="#808080", fg="white", command=self.help)
        self.help_button.grid(row=0, column=0, padx=2)

        self.stats_button = Button(self.help_export_frame, text="Game Stats", font="Arial 15 bold",
                                   bg="#003366", fg="white", command=lambda: self.to_stats(self.round_stats_list,
                                                                                   self.game_stats_list))
        self.stats_button.grid(row=0, column=1, padx=2)

        # Quit Button
        self.quit_button = Button(self.game_frame, text="Quit", fg="white", bg="#660000", font="Arial 15 bold",
                                  width=20, command=self.to_quit, padx=10, pady=10)
        self.quit_button.grid(row=6, pady=10)

    # Help section
    def help(self):
        get_help = Help(self)
        get_help.help_text.configure(text="Enter the funds you want to play with and choose your stakes. \n"
                                          "Press <enter> or 'Open Boxes' to see what is hidden in the mystery box! \n "
                                          "However, you only have a certain amount of funds so play wisely!")

    def to_stats(self, game_history, game_stats):
        GameStats(self, game_history, game_stats)

    def reveal_boxes(self):
        # retrieve of the balance from the initial function..
        current_balance = self.balance.get()
        stakes_multiplier = self.multiplier.get()

        round_winnings = 0
        prizes = []
        stats_prizes = []

        # Photo can be changed depending on stakes
        copper = ["copper_low.gif", "copper_med.gif", "copper_high.gif"]
        silver = ["silver_low.gif", "silver_med.gif", "silver_high.gif"]
        gold = ["gold_low.gif", "gold_med.gif", "gold_high.gif"]

        for item in range(0, 3):
            prize_num = random.randint(1, 100)

            if 0 < prize_num <= 5:
                prize = PhotoImage(file=gold[stakes_multiplier-1])
                prize_list = "gold (${})".format(5 * stakes_multiplier)
                round_winnings += 5 * stakes_multiplier
            elif 5 < prize_num <= 25:
                prize = PhotoImage(file=silver[stakes_multiplier-1])
                prize_list = "silver (${})".format(2 * stakes_multiplier)
                round_winnings += 2 * stakes_multiplier
            elif 25 < prize_num <= 65:
                prize = PhotoImage(file=copper[stakes_multiplier-1])
                prize_list = "copper (${})".format(1 * stakes_multiplier)
                round_winnings += stakes_multiplier
            else:
                prize = PhotoImage(file="lead.gif")
                prize_list = "lead ($0)"

            prizes.append(prize)
            stats_prizes.append(prize_list)

        photo1 = prizes[0]
        photo2 = prizes[1]
        photo3 = prizes[2]

        # Display prizes
        self.prize1_label.config(image=photo1)
        self.prize1_label.photo = photo1
        self.prize2_label.config(image=photo2)
        self.prize2_label.photo = photo2
        self.prize3_label.config(image=photo3)
        self.prize3_label.photo = photo3

        # Deduct cost of game
        current_balance -= 5 * stakes_multiplier

        # Add Winnings
        current_balance += round_winnings

        # Set balance to new balance
        self.balance.set(current_balance)

        # update game_stats_list with current balance (replace item in position 1 with current balance)
        self.game_stats_list[1] = current_balance

        balance_statement = "Game Cost: ${}\nPayback: ${} \nCurrent Balance: ${}".format(5 * stakes_multiplier,
                                                                                         round_winnings,
                                                                                         current_balance)

        # Add round results to stats list
        round_summary = "{} | {} | {} - Cost: ${} | " \
                        "Payback: ${} | Current Balance: " \
                        "${}".format(stats_prizes[0], stats_prizes[1],
                                     stats_prizes[2], 5 * stakes_multiplier, round_winnings,
                                     current_balance)
        self.round_stats_list.append(round_summary)
        print(self.round_stats_list)

        # Edit label so user can see their balance
        self.balance_label.configure(text=balance_statement)

        if current_balance < 5 * stakes_multiplier:
            self.play_button.config(state=DISABLED)
            self.game_box.focus()
            self.play_button.config(text="Game Over")

            balance_statement = "Current Balance: ${}\nYour balance is too low. You can only " \
                                "quit or view your stats. Sorry about that.".format(current_balance)
            self.balance_label.config(fg="#660000", font="Arial 10 bold", text=balance_statement)

    def to_quit(self):
        root.destroy()


# Game Stats
class GameStats:
    def __init__(self, partner, game_history, game_stats):

        print(game_stats)

        all_game_stats = [
            "Starting Balance: ${}".format(game_stats[0]),
            "Current Balance: ${}".format(game_stats[1])
        ]

        # disable stats button
        partner.stats_button.config(state=DISABLED)

        heading = "Arial 12 bold"
        content = "Arial 12"

        # Sets up child windows (ie: help box)
        self.stats_box = Toplevel()

        # If users press cross at top, closes help and 'releases' button

        self.stats_box.protocol('WM_DELETE_WINDOW', partial(self.close_stats, partner))

        # Set up GUI Frame
        self.stats_frame = Frame(self.stats_box, bg="#DDF0FF")
        self.stats_frame.grid()

        # Set up a Help heading (row 0)
        self.stats_heading_label = Label(self.stats_frame, text="Game Stats",
                                         font="arial 19 bold", bg="#DDF0FF")
        self.stats_heading_label.grid(row=0)

        # To export <instructions> (row 1)
        self.export_instructions = Label(self.stats_frame,
                                         text="Here are your Game Stats. "
                                              "Please use the Export Button to "
                                              "access the results of each round "
                                              "that you played.", wrap=250, font="arial 10 italic",
                                         justify=LEFT, fg="green", padx=10, pady=10, bg="#DDF0FF")
        self.export_instructions.grid(row=1)

        # Starting Balance (row 2)
        self.details_frame = Frame(self.stats_frame, bg="#DDF0FF")
        self.details_frame.grid(row=2)

        # Starting balance (row 2.0)

        self.start_balance_label = Label(self.details_frame, text="Starting Balance",
                                         font=heading, anchor="e", bg="#DDF0FF")
        self.start_balance_label.grid(row=0, column=0, padx=0)

        self.start_balance_value_label = Label(self.details_frame, font=content,
                                               text="${}".format(game_stats[0]),
                                               anchor="w", bg="#DDF0FF")
        self.start_balance_value_label.grid(row=0, column=1, padx=0)

        # Current Balance (row 2.2)
        self.current_balance_label = Label(self.details_frame, text="Current Balance: ",
                                           font=heading, anchor="e", bg="#DDF0FF")
        self.current_balance_label.grid(row=1, column=0, padx=0)

        self.current_balance_value_label = Label(self.details_frame, font=content,
                                                 text="${}".format(game_stats[1]), bg="#DDF0FF")
        self.current_balance_value_label.grid(row=1, column=1, padx=0)

        if game_stats[1] > game_stats[0]:
            win_loss = "Amount Won:"
            amount = game_stats[1] - game_stats[0]
            win_loss_fg = "green"
        else:
            win_loss = "Amount Lost:"
            amount = game_stats[0] - game_stats[1]
            win_loss_fg = "#660000"

        # Add amount won / lost to all_game_stats list for export
        all_game_stats.append("{} {}".format(win_loss, amount))
        all_game_stats.append("Rounds Played: {}".format(len(game_history)))

        # Amount won/lost (row 2.3)
        self.win_loss_label = Label(self.details_frame, text=win_loss,
                                    font=heading, anchor="e", bg="#DDF0FF")
        self.win_loss_label.grid(row=2, column=0, padx=0)

        self.win_loss_value_label = Label(self.details_frame, font=content,
                                          text="${}".format(amount), fg=win_loss_fg,
                                          anchor="w", bg="#DDF0FF")
        self.win_loss_value_label.grid(row=2, column=1, padx=0)

        # Rounds Played (row 2.4)
        self.games_played_label = Label(self.details_frame, text="Rounds Played:",
                                        font=heading, anchor="e", bg="#DDF0FF")
        self.games_played_label.grid(row=4, column=0, padx=0)

        self.games_played_value_label = Label(self.details_frame, font=content,
                                              text=len(game_history), anchor="w", bg="#DDF0FF")
        self.games_played_value_label.grid(row=4, column=1, padx=0)

        # Export Button
        self.export_button = Button(self.details_frame, text="Export", font="Arial 10 bold",
                                    bg="orange", command=lambda: self.export(game_history, all_game_stats))
        self.export_button.grid(row=5, column=0, padx=2)

        # Dismiss button (row 3)
        self.dismiss_btn = Button(self.details_frame, text="Dismiss", width=10, bg="orange",
                                  font="arial 10 bold", command=partial(self.close_stats, partner))
        self.dismiss_btn.grid(row=5, column=1, pady=10)

    def export(self, game_history, all_game_stats):
        Export(self, game_history, all_game_stats)

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
        self.save_frame = Frame(self.export_box)
        self.save_frame.grid(row=5, pady=10)

        # Save and Cancel Buttons (row 0 of save_cancel_frame)
        self.save_button = Button(self.save_frame, text="Save", font="Arial 15 bold", bg="#003366",
                                  fg="white",
                                  command=partial(lambda: self.save_history(partner, game_history, all_game_stats)))
        self.save_button.grid(row=0, column=1)

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
                problem = "(No spaces allowed)"

            else:
                problem = ("(No {}'s allowed)".format(letter))
            has_error = "yes"
            break

        if filename == "":
            problem = "File name can't be blank"
            has_error = "yes"

        if has_error == "yes":
            self.filename_entry.config(bg="#ffafaf")
            self.save_error_label.config(text="Invalid Name: {}".format(problem))
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
                f.write(round + "\n")

            # Heading for Rounds
            f.write("\nRound Details\n\n")

            # Add new line at end of each item
            for item in game_history:
                f.write(item + "\n")

            # close file
            f.close()

            # close dialogue
            self.close_export(partner)

    def close_export(self, partner):
        # Put export button back to normal...
        partner.export_button.config(state=NORMAL)
        self.export_box.destroy()


# Help GUI
class Help:
    def __init__(self, partner):
        background = "#f4a261"

        # disable help button
        partner.help_button.config(state=DISABLED)

        # Sets up child window (ie: help box)
        self.help_box = Toplevel()

        # If users press the cross at top, closes help and 'releases' help button
        self.help_box.protocol('WM_DELETE_WINDOW', partial(self.close_help, partner))

        # Set up GUI Frame

        self.help_frame = Frame(self.help_box, bg=background)
        self.help_frame.grid()

        # Set up Help Heading (row 0)
        self.how_heading = Label(self.help_frame, text="Help / Instructions", font="arial 14 bold",
                                 bg=background)
        self.how_heading.grid(row=0)

        # Help text (label, row 1)
        self.help_text = Label(self.help_frame, text="", justify=LEFT, width=40, bg=background,
                               wrap=250)
        self.help_text.grid(column=0, row=1)

        # Dismiss button (row 2)
        self.dismiss_btn = Button(self.help_frame, text="Dismiss", width=10, bg="orange",
                                  font="arial 10 bold", command=partial(self.close_help, partner))
        self.dismiss_btn.grid(row=2, pady=10)

    def close_help(self, partner):
        # Put help button back to normal...
        partner.help_button.config(state=NORMAL)
        self.help_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Mystery Box Game")
    something = Start(root)
    root.mainloop()
