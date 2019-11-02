"""
Parse https://unicode.org/Public/emoji/12.1/emoji-test.txt into JSON.

When run as main, saves the output to emoji.json
"""
import json
import re
import urllib.request

# Matches the fully-qualified entries in the file
# and has named groups for the character and the description of the emoji
REGEX = re.compile(r'^[^#]*; fully-qualified\s+# (?P<char>[^ ]+) E\d+\.\d (?P<descr>.+)$')  # noqa: E501


def test_line(string):
    """Test whether a string matches REGEX."""
    return True if re.match(REGEX, string) is not None else False


def extract_info(string):
    """Extract the literal emoji codepoint sequence and the description."""
    matches = re.match(REGEX, string)
    char = matches.group('char')
    descr = matches.group('descr')
    return {
        'char': char,
        'descr': descr
    }


def main(url):
    """Download the url and extract its information into a list of dicts."""
    with urllib.request.urlopen(url) as response:
        body = response.read().decode()
        emoji = [
            extract_info(line) for line in
            body.split('\n')
            if test_line(line)
        ]
        return emoji


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Fetch and process the Unicode 12.1 emoji-test.txt file')
    parser.add_argument('-f', '--format',
                        action='store_const',
                        const=2, default=None,
                        help='Export an indented JSON object')

    args = parser.parse_args()
    emoji = main('https://unicode.org/Public/emoji/12.1/emoji-test.txt')
    emoji_json = json.dumps(emoji, indent=args.format)
    print(emoji_json)
