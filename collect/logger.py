import time
from datetime import datetime


class RestaurantLogger:
    """Logging restaurant processing process"""
    def __init__(self):
        """Init timer variables and iterator"""
        self.before = None
        self.after = None
        self.iteration = 1
        self.f = open("logs.txt", "a")

    def start(self):
        """Start timer to calculate execution time"""
        self.before = time.time()
        self.f.write("\n\n\n")

    def log(self, current_url, menu_urls, used_urls, to_be_processed):
        """Log all necessary info about parsing process"""
        self.f.write("============================\n")
        self.f.write("{:14}\n".format(self.iteration))
        self.f.write("============================\n")
        now = datetime.now()
        self.f.write(" " + str(now) + "\n")
        self.f.write("============================\n")
        self.f.write("\n  {} {}\n\n".format("Parsing", current_url))

        self.f.write("  Found menu URLs on page:\n")
        if not menu_urls:
            self.f.write("    <None>\n")
        elif type(menu_urls) is list:
            for url in menu_urls:
                self.f.write("    -" + str(url) + "\n")
        else:
            self.f.write("    -" + str(menu_urls) + "\n")

        self.f.write("\n  Parsed URLs:\n")
        if not used_urls:
            self.f.write("    <None>\n")
        elif type(used_urls) is list:
            for url in used_urls:
                self.f.write("    -" + str(url) + "\n")
        else:
            self.f.write("    -" + str(used_urls) + "\n")

        self.f.write("\n  To be processed:\n")
        if not to_be_processed:
            self.f.write("    <None>\n")
        elif type(to_be_processed) is list:
            for url in to_be_processed:
                self.f.write("    -" + str(url) + "\n")
        else:
            self.f.write("    -" + str(to_be_processed) + "\n")

        self.iteration += 1

    def end(self):
        """After done with parsing whole site - show parsing time"""
        self.after = time.time()
        self.f.write("\n\n{} {} {}\n\n"
                     .format(
                        "Working time is",
                        round(self.after-self.before, 1),
                        "sec"))
        self.f.close()
