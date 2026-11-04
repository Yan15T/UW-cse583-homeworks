#HW1: Fremont Bridge Bicycle Data Analysis

## Process
I used pandas to read the bicycle count data into a DataFrame and inspected 
the columns and data types. I converted the Date column to datetime, calculated
the combined East and West bicycle counts, and extracted the hour and year.
I selected the 2016 data, found one time point with a missing sidewalk count,
and removed it before calculating the average bicycle count for each hour.
I used pandas and matplotlib to create and save the hourly count plot.

I used ChatGPT as a tutoring assistant to understand the Pandas steps and
date parsing. I ran the code and reviewed the output as I worked through
the assignment.

## Bonus: Date Formats

Python's `datetime.datetime` represents an individual date and time.
NumPy's `datetime64` represents dates in arrays with a specified time unit.
Pandas uses `datetime64[ns]` for datetime columns, which works well with
DataFrame operations such as `.dt.hour` and `.dt.year`.
