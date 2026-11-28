
import csv
import json
import time
from pathlib import Path

from triager import triage_complaint


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "test_samples.json"
OUTPUT_FILE = BASE_DIR / "accuracy.csv"

FIELDS = [
    "equipment",
    "urgency",
    "hospital",
    "next_action"
]


def is_correct(expected, predicted):
    """Check whether all four fields match exactly."""

    return all(
        expected[field] == predicted[field]
        for field in FIELDS
    )


def main():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        samples = json.load(file)

    results = []
    correct_v1 = 0
    correct_v2 = 0

    print(f"Evaluating {len(samples)} samples with v1 and v2.")
    print("This makes 40 model requests in total.\n")

    for sample in samples:
        print(f"Processing sample {sample['id']}/20")

        row = {
            "sample_id": sample["id"],
            "complaint": sample["complaint"],
            "expected_equipment": sample["equipment"],
            "expected_urgency": sample["urgency"],
            "expected_hospital": sample["hospital"],
            "expected_next_action": sample["next_action"]
        }

        for version in ("v1", "v2"):
            try:
                prediction = triage_complaint(
                    sample["complaint"],
                    version
                )

                predicted = prediction.model_dump()

                for field in FIELDS:
                    row[f"{version}_{field}"] = predicted[field]

                correct = is_correct(sample, predicted)

                row[f"{version}_correct"] = correct

                if version == "v1" and correct:
                    correct_v1 += 1

                if version == "v2" and correct:
                    correct_v2 += 1

                print(
                    f"  {version}: "
                    f"{'Correct' if correct else 'Incorrect'}"
                )

            except Exception as error:
                print(f"  {version} failed: {error}")

                for field in FIELDS:
                    row[f"{version}_{field}"] = ""

                row[f"{version}_correct"] = False
                row[f"{version}_error"] = str(error)

            # Avoid sending requests too quickly to free models.
            time.sleep(3.2)

        results.append(row)

    total = len(samples)

    accuracy_v1 = (correct_v1 / total) * 100
    accuracy_v2 = (correct_v2 / total) * 100

    column_names = [
        "sample_id",
        "complaint",
        "expected_equipment",
        "expected_urgency",
        "expected_hospital",
        "expected_next_action"
    ]

    for version in ("v1", "v2"):
        column_names.extend([
            f"{version}_equipment",
            f"{version}_urgency",
            f"{version}_hospital",
            f"{version}_next_action",
            f"{version}_correct",
            f"{version}_error"
        ])

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=column_names,
            extrasaction="ignore"
        )

        writer.writeheader()
        writer.writerows(results)

        # Add a summary row after the 20 samples.
        summary = {
            "sample_id": "OVERALL",
            "complaint": "Exact match accuracy",
            "v1_correct": f"{accuracy_v1:.2f}%",
            "v2_correct": f"{accuracy_v2:.2f}%"
        }

        writer.writerow(summary)

    print("\n=== EVALUATION SUMMARY ===")
    print(f"Total samples: {total}")
    print(f"V1 correct: {correct_v1}/{total}")
    print(f"V1 accuracy: {accuracy_v1:.2f}%")
    print(f"V2 correct: {correct_v2}/{total}")
    print(f"V2 accuracy: {accuracy_v2:.2f}%")
    print(f"\nResults saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
