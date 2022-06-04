from ui import UserInterface


def main() -> None:
    ui = UserInterface()
    ui.run_game_loop()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
