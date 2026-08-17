#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
histogrammer.py

Create a command-line histogram from a numeric column in a text file.

Example:
    python histogrammer.py -c 3 -f data.txt

With 20 bins and '#' as histogram symbol:
    python histogrammer.py -c 3 -f data.txt -b 20 -g "#"

CSV file:
    python histogrammer.py -c 3 -f data.csv -s ","

Show the column header:
    python histogrammer.py -c 3 -f data.txt -k
"""

import argparse
import statistics
import sys
from pathlib import Path


DEFAULT_BINS = 10
DEFAULT_SEPARATOR = "\t"
DEFAULT_SYMBOL = "="


# ============================================================================
# Command line
# ============================================================================

def parse_arguments():
    parser = argparse.ArgumentParser(
        description=(
            "Read a numeric column from a text file and "
            "create a histogram in the command line."
        )
    )

    parser.add_argument(
        "-c",
        "--column",
        type=int,
        required=True,
        help="Column to analyze (1-based).",
    )

    parser.add_argument(
        "-f",
        "--file",
        type=Path,
        required=True,
        help="Input file.",
    )

    parser.add_argument(
        "-s",
        "--separator",
        default=DEFAULT_SEPARATOR,
        help=r'Field separator. Default: TAB ("\t").',
    )

    parser.add_argument(
        "-g",
        "--symbol",
        default=DEFAULT_SYMBOL,
        choices=["#", "=", "0", "o", "."],
        help="Histogram symbol. Default: '='.",
    )

    parser.add_argument(
        "-b",
        "--bins",
        type=int,
        default=DEFAULT_BINS,
        help="Number of histogram bins. Default: 10.",
    )

    parser.add_argument(
        "-k",
        "--header",
        action="store_true",
        help="Display the header of the selected column.",
    )

    return parser.parse_args()


# ============================================================================
# Input
# ============================================================================

def read_column(filename, column, separator):
    """
    Read one column from a text file.

    The first line is treated as the header.
    Numeric values are returned as floats.

    Returns:
        values  : list[float]
        errors  : list[tuple[int, str]]
        header  : str
    """

    if not filename.exists():
        raise FileNotFoundError(
            f"Input file does not exist: {filename}"
        )

    if not filename.is_file():
        raise ValueError(
            f"Input path is not a file: {filename}"
        )

    values = []
    errors = []

    with filename.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as infile:

        try:
            header_line = next(infile)
        except StopIteration:
            raise ValueError("Input file is empty.")

        header_fields = header_line.rstrip("\r\n").split(separator)

        if column < 1:
            raise ValueError(
                "Column numbers start at 1."
            )

        if column > len(header_fields):
            raise ValueError(
                f"Column {column} does not exist. "
                f"The file contains {len(header_fields)} columns."
            )

        header = header_fields[column - 1].strip()

        for line_number, line in enumerate(infile, start=2):
            fields = line.rstrip("\r\n").split(separator)

            if column > len(fields):
                errors.append(
                    (line_number, "<missing column>")
                )
                continue

            raw_value = fields[column - 1].strip()

            if not raw_value:
                errors.append(
                    (line_number, "<empty>")
                )
                continue

            try:
                values.append(float(raw_value))
            except ValueError:
                errors.append(
                    (line_number, raw_value)
                )

    return values, errors, header


# ============================================================================
# Histogram
# ============================================================================

def create_bins(values, number_of_bins):
    """
    Create equally sized bins.

    Returns a list of dictionaries:

        {
            "lower": float,
            "upper": float,
            "count": int,
        }

    Bin intervals are:

        [lower, upper)

    except for the final bin:

        [lower, upper]
    """

    minimum = min(values)
    maximum = max(values)

    # Special case: all values are identical.
    if minimum == maximum:
        return [
            {
                "lower": minimum,
                "upper": maximum,
                "count": len(values),
            }
        ]

    width = (maximum - minimum) / number_of_bins

    bins = []

    for index in range(number_of_bins):
        lower = minimum + index * width
        upper = minimum + (index + 1) * width

        bins.append(
            {
                "lower": lower,
                "upper": upper,
                "count": 0,
            }
        )

    # Assign every value to exactly one bin.
    for value in values:

        if value == maximum:
            index = number_of_bins - 1
        else:
            index = int((value - minimum) / width)

            # Protect against floating point edge cases.
            index = max(
                0,
                min(index, number_of_bins - 1),
            )

        bins[index]["count"] += 1

    return bins


def calculate_relative_frequencies(bins):
    """Add relative frequencies to the bins."""

    total = sum(
        item["count"]
        for item in bins
    )

    if total == 0:
        return

    for item in bins:
        item["relative"] = item["count"] / total


def create_histogram_bars(bins, symbol, maximum_width=50):
    """
    Scale histogram bars relative to the most populated bin.

    The largest bin always gets maximum_width characters.
    """

    largest_count = max(
        item["count"]
        for item in bins
    )

    if largest_count == 0:
        return

    for item in bins:
        if item["count"] == 0:
            item["bar"] = ""
            continue

        length = round(
            item["count"] / largest_count * maximum_width
        )

        length = max(1, length)

        item["bar"] = symbol * length


# ============================================================================
# Output
# ============================================================================

def format_number(value):
    """
    Format bin boundaries.

    Four decimal places are retained, as in the original script.
    """

    return f"{value:.4f}"


def print_histogram(
    bins,
    symbol,
    header=None,
    maximum_width=50,
):
    """Print the histogram."""

    calculate_relative_frequencies(bins)

    create_histogram_bars(
        bins,
        symbol,
        maximum_width,
    )

    print()

    if header is not None:
        print(f"Column: {header}")
        print()

    print(
        f"{'Bin':<25}"
        f"{'Count':>8}"
        f"{'Relative':>12}"
        f"  Histogram"
    )

    print("-" * 0)

    for item in bins:

        lower = format_number(item["lower"])
        upper = format_number(item["upper"])

        interval = f"{lower} to {upper}"

        print(
            f"{interval:<25}"
            f"{item['count']:>8}"
            f"{item['relative']:>11.2%}"
            f"  | {item['bar']}"
        )

    print()


def print_statistics(values):
    """Print basic statistics."""

    print("Statistics")
    print("-" * 40)

    print(f"N     = {len(values)}")
    print(f"Mean  = {statistics.mean(values):.2f}")

    if len(values) >= 2:
        print(
            f"STDEV = {statistics.stdev(values):.2f}"
        )
    else:
        print(
            "STDEV = undefined "
            "(at least two values required)"
        )

    print()


def print_input_summary(args, header):
    """Print detected input parameters."""

    print()
    print("Input")
    print("-" * 40)

    print(f"File      : {args.file}")
    print(f"Column    : {args.column}")
    print(f"Bins      : {args.bins}")
    print(f"Separator : {repr(args.separator)}")
    print(f"Symbol    : {args.symbol}")

    if args.header:
        print(f"Header    : {header}")

    print()


def print_errors(errors):
    """Print a useful summary of non-numeric values."""

    if not errors:
        return

    print()
    print(
        f"Warning: {len(errors)} non-numeric "
        f"value(s) were ignored."
    )

    print("Examples:")

    for line_number, value in errors[:10]:
        print(
            f"  line {line_number}: {value!r}"
        )

    if len(errors) > 10:
        print(
            f"  ... and {len(errors) - 10} more."
        )

    print()


# ============================================================================
# Main
# ============================================================================

def main():
    args = parse_arguments()

    # Validate arguments.
    if args.bins < 1:
        print(
            "Error: Number of bins must be at least 1.",
            file=sys.stderr,
        )
        return 2

    if args.column < 1:
        print(
            "Error: Column number must be at least 1.",
            file=sys.stderr,
        )
        return 2

    try:
        values, errors, header = read_column(
            args.file,
            args.column,
            args.separator,
        )

    except (FileNotFoundError, ValueError, OSError) as error:
        print(
            f"Error: {error}",
            file=sys.stderr,
        )
        return 1

    if not values:
        print(
            f"Error: No numeric values were found "
            f"in column {args.column}.",
            file=sys.stderr,
        )

        if errors:
            print_errors(errors)

        return 1

    print_input_summary(args, header)

    print_errors(errors)

    # Create histogram.
    bins = create_bins(
        values,
        args.bins,
    )

    print_histogram(
        bins,
        args.symbol,
        header if args.header else None,
    )

    print_statistics(values)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

