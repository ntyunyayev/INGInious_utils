import argparse
import yaml


def main():
    parser = argparse.ArgumentParser(
        description="Change the deadline of a series of exercice.")
    parser.add_argument(
        "--course_folder", help="Path to the INGInious root", required=True)
    parser.add_argument(
        "--series_title", help="Id of the series of exercice", required=True)
    parser.add_argument(
        "--new_deadline", help="New deadline for the series of exercice", required=True)

    args = parser.parse_args()

    tasks_list = []
    yaml_path = f"{args.course_folder}/course.yaml"
    course_yaml = {}
    with open(yaml_path, 'r') as file:
        course_yaml = yaml.safe_load(file)
        toc = course_yaml["dispenser_data"]["toc"]
        for e in toc:
            if (e["title"] == args.series_title):
                task_list = list(e["tasks_list"])

    for task in task_list:
        task_config = course_yaml["dispenser_data"]["config"][task]
        if "false" not in str(task_config["accessibility"]).lower():
            task_config["accessibility"] = args.new_deadline
    with open(yaml_path, 'w') as file:
        yaml.dump(course_yaml, file, default_flow_style=False)


if __name__ == "__main__":
    main()
