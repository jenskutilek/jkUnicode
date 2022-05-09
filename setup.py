from setuptools import setup
from mypyc.build import mypycify


if __name__ == "__main__":
    setup(
        # ext_modules=mypycify([
        #     "lib/jkUnicode/tools/helpers.py",
        # ]),
    )
