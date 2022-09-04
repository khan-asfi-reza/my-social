import os
import pkgutil

from pathlib import Path


PATH = Path(__file__).resolve().parent


def find_fixture_modules():
    """
    Finds fixtures located in the fixtures directory
    """
    modules = [
        "tests.fixtures.{}".format(name)
        for _, name, is_pkg in pkgutil.iter_modules([os.path.join(PATH, "fixtures")])
        if not is_pkg and not name.startswith("_") and name != "factories"
    ]

    return modules


pytest_plugins = find_fixture_modules()

factories = [
    "tests.fixtures.factories.{}".format(name)
    for _, name, is_pkg in pkgutil.iter_modules(
        [os.path.join(PATH, "fixtures", "factories")]
    )
    if not is_pkg and not name.startswith("_")
]
