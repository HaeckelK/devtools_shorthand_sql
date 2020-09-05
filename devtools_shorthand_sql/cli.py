"""Console script for devtools_shorthand_sql."""
import argparse
import sys

import devtools_shorthand_sql.core as core


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('filename', type=str, help='Full path to shorthand file.')
    parser.add_argument('--sql_type', choices=['sqlite', 'postgres'],
                        default='sqlite',
                        help='RDMS style to be used for produced statements.')
    args = parser.parse_args()
    core.main(args.filename, args.sql_type)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
