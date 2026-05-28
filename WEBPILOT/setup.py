from setuptools import setup, find_packages

setup(
    name="webpilot",
    version="1.0.0",
    description="Autonomous Web Agent — Microsoft Build AI Hackathon 2026",
    author="Nishchal Soni & Kuldeep Parmar",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "anthropic>=0.34.0",
        "playwright>=1.44.0",
        "rich>=13.7.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "webpilot=webpilot.main:main",
            "webpilot-demo=webpilot.demo:main",
        ]
    },
)
