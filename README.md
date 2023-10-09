# Cloud_GPU_Price_Performance_Analyzer
This project analyzes cloud GPU offerings by assigning a price/performance score based on key features like VRAM, RAM, vCPUs, storage, and price.


The goal is to provide an easy way to compare and evaluate different cloud GPU options using a standard scoring system.

The score is calculated using a weighted formula that normalizes each feature to a 0-1 scale and combines them based on configured weights.

Higher scores represent better price/performance. The final score is also converted to a letter grade A-F for easy interpretation.

Features
Loads GPU data from an Excel spreadsheet
Config driven weights and min/max values for normalization
Calculates normalized and weighted score for each GPU
Converts score to letter grade
Includes tests for validation
Usage
The main entry point is main.py. Simply run:

Copy code

python main.py
This will:

Load data.xlsx
Process and normalize features
Calculate scores
Output score and grade for each GPU
The notebook GPU-Analysis.ipynb provides examples of analyzing the processed data.

Resources
data.xlsx: contains sample GPU data
config.py: weights and min/max values for normalization
main.py: main script
utils.py: functions for loading, normalizing and scoring
GPU-Analysis.ipynb: sample analysis notebook
Next Steps
Potential enhancements:

Expand to more GPU models
Add more features like PCIe vs SXM
Build web interface for easy lookup
Automate data updates via web scraping
Credits
Created by [Your Name] as a sample project to demonstrate GPU analysis in Python.
