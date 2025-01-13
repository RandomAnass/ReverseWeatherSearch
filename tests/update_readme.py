import datetime

def update_readme():

    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    try:
        with open("report.xml", "r") as report:
            if "<failure" in report.read():
                result = "🔴"
            else:
                result = "🟢"
    except FileNotFoundError:
        result = "❓"


    with open("README.md", "r") as file:
        lines = file.readlines()


    table_start = None
    for idx, line in enumerate(lines):
        if line.startswith("| Date       | Tests Passed |"):
            table_start = idx
            break

    # create table header if no table exists
    if table_start is None:
        lines.append("\n")
        lines.append("| Date       | Tests Passed |\n")
        lines.append("|------------|--------------|\n")
        table_start = len(lines)

    new_row = f"| {yesterday} | {result}           |\n"
    if len(lines) > table_start + 15:  #last 15 entries
        lines = lines[:table_start + 3] + [new_row] + lines[table_start + 4:]
    else:
        lines.append(new_row)

    with open("README.md", "w") as file:
        file.writelines(lines)

if __name__ == "__main__":
    update_readme()
