"""
Setup script for NOMAD Threat Intelligence Framework
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="nomad-threat-intel",
    version="1.0.0",
    author="NOMAD Development Team",
    author_email="nomad@example.com",
    description="AI-powered threat intelligence orchestration framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/campbellmcgregor/nomad-threat-intel-framework",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "pytest-asyncio>=0.18",
            "black>=22.0",
            "isort>=5.0",
            "flake8>=4.0",
            "mypy>=0.910",
        ],
        "production": [
            "gunicorn>=20.0",
            "prometheus-client>=0.14",
            "redis>=4.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "nomad=nomad_workflow_enhanced:main",
            "nomad-rss=scripts.run_rss_agent:main",
            "nomad-orchestrator=scripts.run_orchestrator:main",
            "nomad-ciso=scripts.run_ciso_report:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.yml", "*.yaml"],
    },
)