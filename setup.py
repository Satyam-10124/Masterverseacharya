from setuptools import setup, find_packages

setup(
    name="masterversacharya",
    version="0.1.0",
    description="A spiritual guidance assistant",
    author="Satyam Singhal",
    packages=find_packages(),
    install_requires=[
        "google-adk",
        "google-generativeai",
        "python-dotenv",
        "requests"
    ],
)
