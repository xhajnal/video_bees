import re


def parse_population_size(file_name):
    if "bee" in str(file_name).lower():
        spam = re.findall(r"\dbee", str(file_name).lower())
        if not spam:
            return False
        elif len(spam) > 1:
            return False
        else:
            ## return the digit
            return spam[0][0]
    else:
        return False
