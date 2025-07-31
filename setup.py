from setuptools import setup, find_packages

setup(
    name="rubik-solver",
    version="0.1.0",
    description="A scalable Rubik's Cube solver for 2x2, 3x3, and 4x4 cubes",
    author="Rubik's Cube Solver Team",
    author_email="example@example.com",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "matplotlib",
    ],
    extras_require={
        "visualization": ["imageio"],
        "interactive": ["ipywidgets"],
        "ml": ["tensorflow", "scikit-learn"],
    },
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)