# Refactor code
# -------------
# Not timed (good to get it back within 24 hours)
#
# An intern has provided the code below to update the version number
# within two different files.
# The intern has left and you need to review and improve the code before
# submitting to source control.
#
# Please do not be constrained by the existing code (i.e. you don't have
# to keep the same function names, structure)
# Aim for production quality 'best-practice/clean' code
#
# Original Requirements
# ---------------------
# A script in a build process needs to update the build version number in 2
# locations.
# - The version number will be in an environment variable "BuildNum"
# - The files to be modified will be under "$SourcePath/develop/global/src"
# directory
# - The "SConstruct" file has a line "point=123," (where 123
# (just an example) should be updated with the value of "BuildNum"
# Environment variable)
# - The "VERSION"file has a line "ADLMSDK_VERSION_POINT= 123" (where 123
# (just an example) should be updated with the value of "BuildNum"
# Environment variable)
import os
import re
import tempfile
from pathlib import Path

# SCONSTRUCT file interesting lines
# config.version = Version(
# major=15,
# minor=0,
# point=6,
# patch=0
#)

# VERSION file interesting line
# ADLMSDK_VERSION_POINT=6

SRC_SUBDIR = Path("develop") / "global" / "src"


def get_required_env(name: str) -> str:
    value = os.environ.get(name)

    if not value:
        raise EnvironmentError(f"Missing required environment variable: {name}")

    return value


def update_assignment_line(line: str, key: str, new_value: str) -> tuple[str, bool]:
    stripped = line.lstrip()

    if not stripped.startswith(key):
        return line, False

    prefix, separator, suffix = line.partition("=")

    if not separator:
        return line, False

    newline = "\n" if line.endswith("\n") else ""

    leading_space_after_equal = ""
    value_part = suffix.rstrip("\n")

    while value_part.startswith(" "):
        leading_space_after_equal += " "
        value_part = value_part[1:]

    trailing_comma = "," if value_part.rstrip().endswith(",") else ""

    return f"{prefix}={leading_space_after_equal}{new_value}{trailing_comma}{newline}", True


def update_file(file_path: Path, key: str, new_value: str) -> None:
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    original_permissions = file_path.stat().st_mode
    updated_lines = []
    replacement_count = 0

    with file_path.open("r", encoding="utf-8") as file:
        for line in file:
            updated_line, changed = update_assignment_line(line, key, new_value)

            if changed:
                replacement_count += 1

            updated_lines.append(updated_line)

    if replacement_count == 0:
        raise ValueError(f"No line found for key {key!r} in {file_path}")

    if replacement_count > 1:
        raise ValueError(f"Expected one line for key {key!r}, found {replacement_count}")

    with tempfile.NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=file_path.parent,
        delete=False,
    ) as temp_file:
        temp_file.writelines(updated_lines)
        temp_path = Path(temp_file.name)

    temp_path.chmod(original_permissions)
    temp_path.replace(file_path)


def main() -> None:
    source_path = Path(get_required_env("SourcePath"))
    build_num = get_required_env("BuildNum")

    if not build_num.isdigit():
        raise ValueError(f"BuildNum must be numeric, got: {build_num!r}")

    src_dir = source_path / SRC_SUBDIR

    update_file(
        file_path=src_dir / "SConstruct",
        key="point",
        new_value=build_num,
    )

    update_file(
        file_path=src_dir / "VERSION",
        key="ADLMSDK_VERSION_POINT",
        new_value=build_num,
    )


if __name__ == "__main__":
    main()