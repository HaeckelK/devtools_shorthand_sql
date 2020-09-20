"""Console script for devtools_shorthand_sql."""
import argparse
import sys

import devtools_shorthand_sql.core as core


def main() -> int:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('filename', type=str, help='Full path to shorthand file.')
    parser.add_argument('-o', '--output_filename', type=str, help='Full filename including path for where to save created \
        functions', default='shorthand_sql_created_functions.txt')
    parser.add_argument('--sql_type', choices=['sqlite', 'postgres'],
                        default='sqlite',
                        help='RDMS style to be used for produced statements.')
    args = parser.parse_args()
    core.main(args.filename, args.sql_type, args.output_filename)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
