import argparse
import yaml


def main():
    parser = argparse.ArgumentParser(
        description="Change the deadline of a series of exercice.")
    parser.add_argument(
        "--course_folder", help="Path to the INGInious root", required=True)
    parser.add_argument(
        "--exercises_id", help="Id of the series of exercice", required=True)
    parser.add_argument(
        "--new_deadline", help="New deadline for the series of exercice", required=False)
    parser.add_argument(
        "--author", help="Author of the series of exercice", required=False)
    parser.add_argument(
        "--submissions_limit", help="New submission limit for the series of exercice", required=False)
    args = parser.parse_args()

    tasks_list = []
    with open(f"{args.course_folder}/course.yaml", 'r') as file:
        course_yaml = yaml.safe_load(file)
        toc = course_yaml["dispenser_data"]
        for e in toc:
            if (e["id"] == args.exercises_id):
                task_list = list(e["tasks_list"].keys())

    for task in task_list:
        yaml_file_path = f"{args.course_folder}/{task}/task.yaml"
        with open(yaml_file_path) as f:
            lines = f.readlines()
            if args.new_deadline:
                if "false" not in lines[0]:
                    lines[0] = f"accessible: {args.new_deadline}\n"
            if args.author:
                if "author" in lines[1]:
                    lines[1] = f"author: {args.author}\n"
            if args.submissions_limit:
                [amount, period] = args.submissions_limit.split(",")
                for line in lines:
                    if "    amount:" in line:
                        lines[lines.index(line)] = f"    amount: {
                            amount}\n"
                    if "    period:" in line:
                        lines[lines.index(line)] = f"    period: {
                            period}\n"

            with open(yaml_file_path, "w") as f:
                f.writelines(lines)


if __name__ == "__main__":
    main()
