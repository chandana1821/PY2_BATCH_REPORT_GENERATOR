import argparse
import os
from services.report_service import ReportService


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)

    args = parser.parse_args()

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    service = ReportService(args.input, args.output)
    service.generate_report()


if __name__ == "__main__":
    main()