import re


dpkg_status_file_path = "./status"  # file from Ubuntu 18.04.3 LTS
# dpkg_status_file_path = './status.real'  # file from https://gist.github.com/lauripiispanen/29735158335170c27297422a22b48caa
description_regex = re.compile(
    r"^Description: (.+)"  # Matches everything after 'Description: '
)
dependency_regex = re.compile(
    r"\w+\S*"  # Matches 'python3-apport' from 'python3-apport (>= 2.20.9-0ubuntu7.9)'
)


def file_opener(file=dpkg_status_file_path):
    with open(file, "r", encoding="utf8") as f:
        content = f.read()
    return content


def dpkg_parser(string=file_opener()):
    """Parses a dpkg status file (https://www.debian.org/doc/debian-policy/ch-controlfields.html)
       and returns a sorted dictionary with package name as the key,
       and {dependency, reverse-dependency, description} as the value
    """
    package_info = {}
    sections = string.split("\n\n")  # Sections are separated by two new lines
    for section in sections:  # package
        if section == "":
            continue
        description = []
        depends_on = []
        for line in section.split("\n"):  # info about package
            if line == "":
                break
            if line.startswith("Package"):
                package = line.split()[1]
                continue
            if line.startswith("Description"):
                description.append(re.search(description_regex, line).group(1))
                continue
            if line.startswith(" /"):  # skip
                continue
            if line.startswith(" "):
                if line.startswith(" ."):
                    line = ""
                description.append(line)
                continue
            if line.startswith("Depends") or line.startswith("Pre-Depends"):
                for item in line.split(", "):
                    if item.startswith("Depends") or item.startswith("Pre-Depends"):
                        depends_on.append(item.split()[1])
                    else:
                        depends_on.append(re.search(dependency_regex, item).group(0))
                depends_on.sort()  # sort dependencies
        if not description:  # For the EOF case
            break
        # Building data structure
        if package_info.get(package) is None:  # Is this a new package in the dict?
            package_info[package] = {
                "depends": depends_on,
                "reverse-depends": [],
                "description": description,
            }
        else:
            package_info[package] = {
                "depends": depends_on,
                "reverse-depends": package_info[package]["reverse-depends"],
                "description": description,
            }
        # Making connections to dependencies in order to build reverse dependencies
        for package_dependency in package_info[package]["depends"]:
            if package_info.get(package_dependency) is None:  # is package in dict?
                package_info[package_dependency] = {"reverse-depends": []}
            package_info[package_dependency]["reverse-depends"].append(package)
    sorted_package_info = {
        key: package_info[key] for key in sorted(package_info)
    }  # sort package names
    return sorted_package_info


if __name__ == "__main__":
    print(dpkg_parser())
