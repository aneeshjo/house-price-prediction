from setuptools import find_packages, setup


setup(
    name="house-price-prediction",
    version="0.0.1",
    author="Aneesh",
    description="End-to-End House Price Prediction using Machine Learning",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
)