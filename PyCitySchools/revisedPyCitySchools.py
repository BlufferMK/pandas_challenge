# %% [markdown]
# # PyCity Schools Analysis
# 
# There are 15 total schools included in PyCity.  There are a total of 39,170 students, and the district total budget is about $25,650,000.  Eight of the 15 schools are charter schools.  All of the schools range in size of enrollment from 427 students on the low end, all the way up to 4,719 students.  All but 3 of the shools have enrollments greater than 1500 students.
# 
# Student Math and Reading scores were merged with data about the schools in order to do an analysis of the results.  One takeaway is that the Charter Schools generally have lower per student Budgets.  In addition, the highest performing schools, in terms of percent of students passing both math and reading, were all Charter schools. The bottom 5 performing schools were all District schools.  
# 
# Comparing bins of spending ranges to math and reading results showed that schools with the lowest per student budgets had higher rates of passing math and reading.  Schools that spent more per students had lower passing rates.  This seems counterintuitive.  One would think that spending more would likely help at least some schools to raise results well enough to positively affect the averages.  This may be partially explained by looking at the size of the schools.  Small and medium schools (less than 2000 students) had relatively higher passing rates and lower per student budgets.  Passing rates for large schools were quite a bit lower, and these schools, on average, have higher spending per student.  It seems that perhaps there is something about running a large school that requires more money and does not provide the same high achievement.
#   
# ---

# %%
# Dependencies and Setup
import pandas as pd
from pathlib import Path

# File to Load (Remember to Change These)
school_data_to_load = Path("../Resources/schools_complete.csv")
student_data_to_load = Path("../Resources/students_complete.csv")

# Read School and Student Data File and store into Pandas DataFrames
schools_df = pd.read_csv(school_data_to_load)
student_df = pd.read_csv(student_data_to_load)


# Combine the data into a single dataset.  
data_complete = pd.merge(student_df, schools_df, how="left", on=["school_name", "school_name"])


# %% [markdown]
# ## District Summary

# %%
# Calculate the total number of unique schools
school_count = len(schools_df["school_name"])
school_count

# %%
# Calculate the total number of students
student_count = len(student_df["Student ID"].unique())
print(student_count)

# enrollments
enrollments= schools_df["size"].unique()
print(enrollments)
enrollments_total = enrollments.sum()

enrollments_total

# %%
schools_df


# %%
# Calculate the total budget
budgets_all = schools_df["budget"].sum()
print(budgets_all)



# %%
# Calculate the average (mean) math score
avg_math_score = data_complete["math_score"].mean()
avg_math_score

# %%
# Calculate the average (mean) reading score
avg_reading_score = data_complete["reading_score"].mean()
avg_reading_score

# %%
# Use the following to calculate the percentage of students who passed math (math scores greather than or equal to 70)
passing_math_count = data_complete[(data_complete["math_score"] >= 70)].count()["student_name"]
passing_math_percentage = passing_math_count / float(student_count) * 100
passing_math_percentage

# %%
# Calculate the percentage of students who passed reading (hint: look at how the math percentage was calculated)  
passing_reading_count = data_complete[(data_complete["reading_score"] >= 70)].count()["student_name"] 
passing_reading_percentage = passing_reading_count / float(student_count) * 100
passing_reading_percentage

# %%
# Use the following to calculate the percentage of students that passed math and reading
passing_math_reading_count = data_complete[
    (data_complete["math_score"] >= 70) & (data_complete["reading_score"] >= 70)
].count()["student_name"]
overall_passing_rate = passing_math_reading_count /  float(student_count) * 100
overall_passing_rate

# %%
# Create a high-level snapshot of the district's key metrics in a DataFrame
district_summary = pd.DataFrame([{"Total Schools":school_count,"Total Students":student_count,
                                  "Total Budget":budgets_all,"Average Math Score": avg_math_score,
                                  "Average Reading Score":avg_reading_score,"% Passing Math":passing_math_percentage,
                                  "% Passing Reading":passing_reading_percentage,"% Overall Passing":overall_passing_rate}])


# Formatting
district_summary["Total Students"] = district_summary["Total Students"].map("{:,}".format)
district_summary["Total Budget"] = district_summary["Total Budget"].map("${:,.2f}".format)

# Display the DataFrame
district_summary

# %% [markdown]
# ## School Summary

# %%
# Use the code provided to select all of the school types
data_complete.head()

school_types = schools_df.set_index('school_name')['type']
school_types

# %%
# Calculate the total student count per school

per_school_stud_count = schools_df.set_index('school_name')['size']
per_school_stud_count

# %%
# Calculate the total school budget and per capita spending per school
# school budgets
per_school_budget = schools_df.set_index('school_name')['budget']
per_school_budget


per_school_capita = per_school_budget/per_school_stud_count
per_school_capita

# %%
# Calculate the average test scores per school

 
math_avgs = (data_complete.groupby('school_name')['math_score'].mean())
reading_avgs = (data_complete.groupby('school_name')['reading_score'].mean())
reading_avgs


# %%
# Calculate the number of students per school with math scores of 70 or higher

per_school_passing_math = data_complete[(data_complete["math_score"]>=70)]
per_school_passing_math
total_school_passing_math = per_school_passing_math.groupby(["school_name"]).size()
total_school_passing_math

# %%
# Calculate the number of students per school with reading scores of 70 or higher
per_school_passing_reading = data_complete[(data_complete["reading_score"]>=70)]
per_school_passing_reading
total_school_passing_reading = per_school_passing_reading.groupby(["school_name"]).size()
total_school_passing_reading


# %%
# Use the provided code to calculate the number of students per school that passed both math and reading with scores of 70 or higher
per_school_passing_both = data_complete[(data_complete["reading_score"]>=70) & (data_complete["math_score"]>=70)]
per_school_passing_both
total_school_passing_both = per_school_passing_both.groupby(["school_name"]).size()
total_school_passing_both

# %%
# Use the provided code to calculate the passing rates
# per_school_passing_math = school_students_passing_math / per_school_counts * 100
# per_school_passing_reading = school_students_passing_reading / per_school_counts * 100
# overall_passing_rate = school_students_passing_math_and_reading / per_school_counts * 100

per_school_math_percent = total_school_passing_math/per_school_stud_count *100
per_school_math_percent

per_school_reading_percent = total_school_passing_reading/per_school_stud_count *100
per_school_reading_percent

per_school_both_percent = total_school_passing_both/per_school_stud_count *100
per_school_both_percent

# %%
# Create a DataFrame called `per_school_summary` with columns for the calculations above.
per_school_summary = pd.DataFrame({"School Type":school_types, "Student Count":per_school_stud_count, "Budget":per_school_budget, "Budget per Student":per_school_capita,
                                   "Average Math Score":math_avgs, "Average Reading Score":reading_avgs, "Percent Passing Math":per_school_math_percent,
                                   "Percent Passing Reading":per_school_reading_percent, "Percent Passing Both":per_school_both_percent})
# Display the DataFrame
per_school_summary

# %%
# Formatting
#per_school_summary["Budget per Student"] = per_school_summary["Budget per Student"].map("${:,.2f}".format)

# %% [markdown]
# ## Highest-Performing Schools (by % Overall Passing)

# %%
# Sort the schools by `% Overall Passing` in descending order and display the top 5 rows.
top_schools = per_school_summary.sort_values(by=["Percent Passing Both"], ascending=False)
top_schools.head(5)

# %% [markdown]
# ## Bottom Performing Schools (By % Overall Passing)

# %%
# Sort the schools by `% Overall Passing` in ascending order and display the top 5 rows.
bottom_schools = per_school_summary.sort_values(by=["Percent Passing Both"], ascending=True)
bottom_schools.head(5)

# %% [markdown]
# ## Math Scores by Grade

# %%
# Use the code provided to separate the data by grade
ninth_graders = data_complete[(data_complete["grade"] == "9th")]
tenth_graders = data_complete[(data_complete["grade"] == "10th")]
eleventh_graders = data_complete[(data_complete["grade"] == "11th")]
twelfth_graders = data_complete[(data_complete["grade"] == "12th")]

# Group by `school_name` and take the mean of the `math_score` column for each.
ninth_grade_math_school = ninth_graders.groupby(["school_name"])                       
ninth_grade_math_scores=(ninth_grade_math_school["math_score"].mean())

tenth_grade_math_school = tenth_graders.groupby(["school_name"])
tenth_grade_math_scores = (tenth_grade_math_school["math_score"].mean())

eleventh_grade_math_school = eleventh_graders.groupby(["school_name"])                       
eleventh_grade_math_scores=(eleventh_grade_math_school["math_score"].mean())

twelfth_grade_math_school = twelfth_graders.groupby(["school_name"])                       
twelfth_grade_math_scores=(twelfth_grade_math_school["math_score"].mean())

# Combine each of the scores above into single DataFrame called `math_scores_by_grade`

math_scores_by_grade = pd.DataFrame({"9th Grade":ninth_grade_math_scores, "10th Grade":tenth_grade_math_scores, 
                                     "11th Grade":eleventh_grade_math_scores, "12th Grade":twelfth_grade_math_scores})

# Display the DataFrame
math_scores_by_grade

# %% [markdown]
# ## Reading Score by Grade 

# %%

# Group by `school_name` and take the mean of the `reading_score` column for each.
ninth_grade_reading_school = ninth_graders.groupby(["school_name"])                       
ninth_grade_reading_scores = (ninth_grade_reading_school["reading_score"].mean())

tenth_grade_reading_school = tenth_graders.groupby(["school_name"])
tenth_grade_reading_scores = (tenth_grade_reading_school["reading_score"].mean())

eleventh_grade_reading_school = eleventh_graders.groupby(["school_name"])                       
eleventh_grade_reading_scores = (eleventh_grade_reading_school["reading_score"].mean())

twelfth_grade_reading_school = twelfth_graders.groupby(["school_name"])                       
twelfth_grade_reading_scores = (twelfth_grade_reading_school["reading_score"].mean())


# Combine each of the scores above into single DataFrame called `reading_scores_by_grade`
reading_scores_by_grade = pd.DataFrame({"9th Grade":ninth_grade_reading_scores, "10th Grade":tenth_grade_reading_scores, 
                                     "11th Grade":eleventh_grade_reading_scores, "12th Grade":twelfth_grade_reading_scores})


# Minor data wrangling
#reading_scores_by_grade = reading_scores_by_grade[["9th grade", "10th grade", "11th grade", "12th grade"]]
#reading_scores_by_grade.index.name = None

# Display the DataFrame
reading_scores_by_grade

# %% [markdown]
# ## Scores by School Spending

# %%
# Establish the bins 
spending_bins = [0, 585, 630, 645, 680]
labels = ["<$585", "$585-630", "$630-645", "$645-680"]

# %%
# Create a copy of the school summary since it has the "Per Student Budget" 
organized_df = per_school_summary.copy()
organized_df

# %%
# Use `pd.cut` to categorize spending based on the bins.
organized_df["Spending Ranges(Per Student)"]=pd.cut(organized_df["Budget per Student"],spending_bins, labels=labels)

spending_math_scores = organized_df.groupby(["Spending Ranges(Per Student)"], observed=False)["Average Math Score"].mean()
spending_reading_scores = organized_df.groupby(["Spending Ranges(Per Student)"], observed=False)["Average Reading Score"].mean()
spending_passing_math = organized_df.groupby(["Spending Ranges(Per Student)"],observed=False)["Percent Passing Math"].mean()
spending_passing_reading = organized_df.groupby(["Spending Ranges(Per Student)"],observed=False)["Percent Passing Reading"].mean()
overall_passing_spending = organized_df.groupby(["Spending Ranges(Per Student)"],observed=False)["Percent Passing Both"].mean()

spending_passing_reading

# %%
# Assemble into DataFrame
spending_summary = pd.DataFrame({"Average Math Score":spending_math_scores, "Average Reading Score":spending_reading_scores, 
                                     "% Passing Math":spending_passing_math, "% Passing Reading":spending_passing_reading, "% Overall Passing":overall_passing_spending})

# Formatting
spending_summary["Average Math Score"] = spending_summary["Average Math Score"].map("{:,.1f}".format)
spending_summary["Average Reading Score"] = spending_summary["Average Reading Score"].map("{:,.1f}".format)
spending_summary["% Passing Math"] = spending_summary["% Passing Math"].map("{:,.1f}%".format)
spending_summary["% Passing Reading"] = spending_summary["% Passing Reading"].map("{:,.1f}%".format)
spending_summary["% Overall Passing"] = spending_summary["% Overall Passing"].map("{:,.1f}%".format)

# Display results
spending_summary

# %% [markdown]
# ## Scores by School Size

# %%
# Establish the bins.
size_bins = [0, 1000, 2000, 5000]
labels = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]

# %%
# Categorize the spending based on the bins
# Use `pd.cut` on the "Total Students" column of the `per_school_summary` DataFrame.

organized_df["Total Students Ranges"]=pd.cut(organized_df["Student Count"],size_bins, labels=labels)

organized_df

# %%
# Calculate averages for the desired columns. 
size_math_scores = organized_df.groupby(["Total Students Ranges"],observed=False)["Average Math Score"].mean()
size_reading_scores = organized_df.groupby(["Total Students Ranges"],observed=False)["Average Reading Score"].mean()
size_passing_math = organized_df.groupby(["Total Students Ranges"],observed=False)["Percent Passing Math"].mean()
size_passing_reading = organized_df.groupby(["Total Students Ranges"],observed=False)["Percent Passing Reading"].mean()
size_passing_overall = organized_df.groupby(["Total Students Ranges"],observed=False)["Percent Passing Both"].mean()
size_student_budget = organized_df.groupby(["Total Students Ranges"],observed=False)["Budget per Student"].mean()
size_student_budget

# %%
# Create a DataFrame called `size_summary` that breaks down school performance based on school size (small, medium, or large).
# Use the scores above to create a new DataFrame called `size_summary`

size_summary = pd.DataFrame({"Average Math Score":size_math_scores, "Average Reading Score":size_reading_scores, 
                                     "% Passing Math":size_passing_math, "% Passing Reading":size_passing_reading, "% Overall Passing":size_passing_overall})

size_summary["Average Math Score"] = size_summary["Average Math Score"].map("{:,.1f}".format)
size_summary["Average Reading Score"] = size_summary["Average Reading Score"].map("{:,.1f}".format)
size_summary["% Passing Math"] = size_summary["% Passing Math"].map("{:,.1f}%".format)
size_summary["% Passing Reading"] = size_summary["% Passing Reading"].map("{:,.1f}%".format)
size_summary["% Overall Passing"] = size_summary["% Overall Passing"].map("{:,.1f}%".format)

# Display results
size_summary

# %% [markdown]
# ## Scores by School Type

# %%
# Group the per_school_summary DataFrame by "School Type" and average the results.
average_math_score_by_type = per_school_summary.groupby(["School Type"])["Average Math Score"].mean()
average_reading_score_by_type = per_school_summary.groupby(["School Type"])["Average Reading Score"].mean()
average_percent_passing_math_by_type = per_school_summary.groupby(["School Type"])["Percent Passing Math"].mean()
average_percent_passing_reading_by_type = per_school_summary.groupby(["School Type"])["Percent Passing Reading"].mean()
average_percent_overall_passing_by_type = per_school_summary.groupby(["School Type"])["Percent Passing Both"].mean()

# %%
# Assemble the new data by type into a DataFrame called `type_summary`

type_summary = pd.DataFrame({"Average Math Score":average_math_score_by_type, "Average Reading Score":average_reading_score_by_type, 
                                     "% Passing Math":average_percent_passing_math_by_type, "% Passing Reading":average_percent_passing_reading_by_type, "% Overall Passing":average_percent_overall_passing_by_type})

type_summary["Average Math Score"] = type_summary["Average Math Score"].map("{:,.1f}".format)
type_summary["Average Reading Score"] = type_summary["Average Reading Score"].map("{:,.1f}".format)
type_summary["% Passing Math"] = type_summary["% Passing Math"].map("{:,.1f}%".format)
type_summary["% Passing Reading"] = type_summary["% Passing Reading"].map("{:,.1f}%".format)
type_summary["% Overall Passing"] = type_summary["% Overall Passing"].map("{:,.1f}%".format)

# Display results
type_summary


