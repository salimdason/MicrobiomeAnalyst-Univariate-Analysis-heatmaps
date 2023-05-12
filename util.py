import subprocess
from time import sleep


class ColorCoder:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def progressBar(message, delay):
    for i in range(4):
        print(
            f"\r{ColorCoder.GREEN}{message}{'.' * i}{ColorCoder.ENDC}",
            end="",
        )
        sleep(delay)


class HeatMapGenerator:
    def __init__(self, command: list):
        self.command = command

    def generateHeatmap(self):
        try:
            progressBar(f"{ColorCoder.BLUE}Generating heatmap{ColorCoder.ENDC}", 0.5)
            subprocess.check_call(self.command)
            print(f"{ColorCoder.GREEN}Heatmap generation successful!{ColorCoder.ENDC}")
        except subprocess.CalledProcessError as error:
            print(
                f"{ColorCoder.FAIL}Heatmap generation failed!{ColorCoder.ENDC}", error
            )
