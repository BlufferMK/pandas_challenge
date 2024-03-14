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
data_complete = pd.merge(student_df, schools_df, how="outer", on=["school_name", "school_name"])


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



# %%
# Calculate the total budget
budgets_all = schools_df["budget"].unique()
print(budgets_all)

budgets_total = budgets_all.sum()
print(budgets_total)

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
                                  "Total Budget":budgets_total,"Average Math Score": avg_math_score,
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

school_types = schools_df['type']
school_types

# %% [markdown]
# make a dataframe for each school

# %%
school_name_df = data_complete.set_index("school_name")

Huang_df = school_name_df.loc["Huang High School", :]

Bailey_df = school_name_df.loc["Bailey High School", :]

Cabrera_df = school_name_df.loc["Cabrera High School", :]

Figueroa_df = school_name_df.loc["Figueroa High School", :]

Ford_df = school_name_df.loc["Ford High School", :]

Griffin_df = school_name_df.loc["Griffin High School", :]

Hernandez_df = school_name_df.loc["Hernandez High School", :]

Holden_df = school_name_df.loc["Holden High School", :]

Johnson_df = school_name_df.loc["Johnson High School", :]

Pena_df = school_name_df.loc["Pena High School", :]

Rodriguez_df = school_name_df.loc["Rodriguez High School", :]

Shelton_df = school_name_df.loc["Shelton High School", :]

Thomas_df = school_name_df.loc["Thomas High School", :]

Wilson_df = school_name_df.loc["Wilson High School", :]

Wright_df = school_name_df.loc["Wright High School", :]


# %%
# Calculate the total student count per school

per_school_counts = {}
for school_name in data_complete['school_name']:
    if school_name in per_school_counts:
        per_school_counts[school_name] +=1
    else:
        per_school_counts[school_name]=1

per_school_data = {
    'school_name': ['Huang High School', 'Figueroa High School', 'Shelton High School', 'Hernandez High School', 'Griffin High School', 'Wilson High School', 'Cabrera High School', 'Bailey High School', 'Holden High School', 'Pena High School', 'Wright High School', 'Rodriguez High School', 'Johnson High School', 'Ford High School', 'Thomas High School'],
    'Students': [2917, 2949, 1761, 4635, 1468, 2283, 1858, 4976, 427, 962, 1800, 3999, 4761, 2739, 1635]
}

stud_count_df = pd.DataFrame(per_school_data)
stud_count_df['School Type']=school_types

stud_count_df

# %%
# Calculate the total school budget and per capita spending per school
# school budgets
budgets_all
stud_count_df["Budget"]=budgets_all

stud_count_df["Per Capita"] = stud_count_df["Budget"]/stud_count_df["Students"]
stud_count_df

# %%
# Calculate the average test scores per school

 
math_sums = pd.DataFrame(data_complete.groupby('school_name')['math_score'].sum())
reading_sums = pd.DataFrame(data_complete.groupby('school_name')['reading_score'].sum())
reading_sums

tot_math_df = pd.merge(stud_count_df, math_sums,on="school_name")
tot_scores_df = pd.merge(tot_math_df,reading_sums, on = "school_name")
tot_scores_df

tot_scores_df["Average Math Score"]=tot_scores_df["math_score"]/tot_scores_df["Students"]
tot_scores_df["Average Reading Score"]=tot_scores_df["reading_score"]/tot_scores_df["Students"]

sorted_tot_scores_df=tot_scores_df.sort_values(by= 'school_name')
sorted_tot_scores_df = sorted_tot_scores_df.reset_index(drop=True)
sorted_tot_scores_df

# %%
# Calculate the number of students per school with math scores of 70 or higher

# %%
# Calculate the number of students per school with math scores of 70 or higher

Hu_pass_math_count = Huang_df[(Huang_df["math_score"] >= 70)].count()["student_name"]
Ba_pass_math_count = Bailey_df[(Bailey_df["math_score"] >= 70)].count()["student_name"]
Ca_pass_math_count = Cabrera_df[(Cabrera_df["math_score"] >= 70)].count()["student_name"]
Fi_pass_math_count = Figueroa_df[(Figueroa_df["math_score"] >= 70)].count()["student_name"]
Fo_pass_math_count = Ford_df[(Ford_df["math_score"] >= 70)].count()["student_name"]
Gr_pass_math_count = Griffin_df[(Griffin_df["math_score"] >= 70)].count()["student_name"]
He_pass_math_count = Hernandez_df[(Hernandez_df["math_score"] >= 70)].count()["student_name"]
Ho_pass_math_count = Holden_df[(Holden_df["math_score"] >= 70)].count()["student_name"]
Jo_pass_math_count = Johnson_df[(Johnson_df["math_score"] >= 70)].count()["student_name"]
Pe_pass_math_count = Pena_df[(Pena_df["math_score"] >= 70)].count()["student_name"]
Ro_pass_math_count = Rodriguez_df[(Rodriguez_df["math_score"] >= 70)].count()["student_name"]
Sh_pass_math_count = Shelton_df[(Shelton_df["math_score"] >= 70)].count()["student_name"]
Th_pass_math_count = Thomas_df[(Thomas_df["math_score"] >= 70)].count()["student_name"]
Wi_pass_math_count = Wilson_df[(Wilson_df["math_score"] >= 70)].count()["student_name"]
Wr_pass_math_count = Wright_df[(Wright_df["math_score"] >= 70)].count()["student_name"]

sorted_tot_scores_df['pass_math_count']=[Ba_pass_math_count,Ca_pass_math_count,Fi_pass_math_count,Fo_pass_math_count,Gr_pass_math_count,He_pass_math_count,Ho_pass_math_count, Hu_pass_math_count,Jo_pass_math_count,Pe_pass_math_count,Ro_pass_math_count,Sh_pass_math_count,Th_pass_math_count,Wi_pass_math_count,Wr_pass_math_count]

sorted_tot_scores_df.head()



# %%
# Calculate the number of students per school with reading scores of 70 or higher
Hu_pass_read_count = Huang_df[(Huang_df["reading_score"] >= 70)].count()["student_name"]
Ba_pass_read_count = Bailey_df[(Bailey_df["reading_score"] >= 70)].count()["student_name"]
Ca_pass_read_count = Cabrera_df[(Cabrera_df["reading_score"] >= 70)].count()["student_name"]
Fi_pass_read_count = Figueroa_df[(Figueroa_df["reading_score"] >= 70)].count()["student_name"]
Fo_pass_read_count = Ford_df[(Ford_df["reading_score"] >= 70)].count()["student_name"]
Gr_pass_read_count = Griffin_df[(Griffin_df["reading_score"] >= 70)].count()["student_name"]
He_pass_read_count = Hernandez_df[(Hernandez_df["reading_score"] >= 70)].count()["student_name"]
Ho_pass_read_count = Holden_df[(Holden_df["reading_score"] >= 70)].count()["student_name"]
Jo_pass_read_count = Johnson_df[(Johnson_df["reading_score"] >= 70)].count()["student_name"]
Pe_pass_read_count = Pena_df[(Pena_df["reading_score"] >= 70)].count()["student_name"]
Ro_pass_read_count = Rodriguez_df[(Rodriguez_df["reading_score"] >= 70)].count()["student_name"]
Sh_pass_read_count = Shelton_df[(Shelton_df["reading_score"] >= 70)].count()["student_name"]
Th_pass_read_count = Thomas_df[(Thomas_df["reading_score"] >= 70)].count()["student_name"]
Wi_pass_read_count = Wilson_df[(Wilson_df["reading_score"] >= 70)].count()["student_name"]
Wr_pass_read_count = Wright_df[(Wright_df["reading_score"] >= 70)].count()["student_name"]

sorted_tot_scores_df['pass_reading_count']=[Ba_pass_read_count,Ca_pass_read_count,
                                  Fi_pass_read_count,Fo_pass_read_count,Gr_pass_read_count,
                                  He_pass_read_count,Ho_pass_read_count, Hu_pass_read_count,Jo_pass_read_count,
                                  Pe_pass_read_count,Ro_pass_read_count,Sh_pass_read_count,
                                  Th_pass_read_count,Wi_pass_read_count,Wr_pass_read_count]


sorted_tot_scores_df

# %%
# Use the provided code to calculate the number of students per school that passed both math and reading with scores of 70 or higher
students_passing_math_and_reading = data_complete[(data_complete["reading_score"] >= 70) & (data_complete["math_score"] >= 70)]
school_students_passing_math_and_reading = students_passing_math_and_reading.groupby(["school_name"]).size()
school_students_passing_math_and_reading
new_index = sorted_tot_scores_df.set_index("school_name")
new_index['pass_both_count']=school_students_passing_math_and_reading

new_index

# %%
# Use the provided code to calculate the passing rates
# per_school_passing_math = school_students_passing_math / per_school_counts * 100
# per_school_passing_reading = school_students_passing_reading / per_school_counts * 100
# overall_passing_rate = school_students_passing_math_and_reading / per_school_counts * 100

new_index['per_school_passing_math']=new_index['pass_math_count']/new_index['Students']*100
new_index['per_school_passing_reading']=new_index['pass_reading_count']/new_index['Students']*100
new_index['per_school_passing_both']=new_index['pass_both_count']/new_index['Students']*100
new_index

# %%
# Create a DataFrame called `per_school_summary` with columns for the calculations above.

columns_to_drop = ['math_score', 'reading_score', 'pass_math_count', 'pass_reading_count', 'pass_both_count']
new_index = new_index.drop(columns_to_drop, axis=1)

organized_df =new_index[["School Type", "Students", "Budget","Per Capita","Average Math Score", "Average Reading Score", "per_school_passing_math", "per_school_passing_reading", "per_school_passing_both"]]


# %%
# Create a DataFrame called `per_school_summary` with columns for the calculations above.
per_school_summary = organized_df.rename(columns={"Budget":"Total School Budget", "Per Capita":"Per Student Budget",
                                                  "per_school_passing_math":"% Passing Math","per_school_passing_reading":"% Passing Reading",
                                                  "per_school_passing_both":"% Overall Passing"})

# Formatting
#per_school_summary["Per Student Budget"] = per_school_summary["Per Student Budget"].map("${:,.2f}".format)

# Display the DataFrame
per_school_summary

# %% [markdown]
# ## Highest-Performing Schools (by % Overall Passing)

# %%
# Sort the schools by `% Overall Passing` in descending order and display the top 5 rows.
top_schools = per_school_summary.sort_values(by=["% Overall Passing","Students"], ascending=False)
top_schools.head(5)

# %% [markdown]
# ## Bottom Performing Schools (By % Overall Passing)

# %%
# Sort the schools by `% Overall Passing` in ascending order and display the top 5 rows.
bottom_schools = per_school_summary.sort_values(by=["% Overall Passing"], ascending=True)
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
ninth_grade_math_scores=pd.DataFrame(ninth_grade_math_school["math_score"].mean())
ninth_math_scores = ninth_grade_math_scores.rename(columns={"math_score":"9th grade"})

tenth_grade_math_school = tenth_graders.groupby(["school_name"])
tenth_grade_math_scores = pd.DataFrame(tenth_grade_math_school["math_score"].mean())
tenth_math_scores = tenth_grade_math_scores.rename(columns={"math_score":"10th grade"})

eleventh_grade_math_school = eleventh_graders.groupby(["school_name"])                       
eleventh_grade_math_scores=pd.DataFrame(eleventh_grade_math_school["math_score"].mean())
eleventh_math_scores = eleventh_grade_math_scores.rename(columns={"math_score":"11th grade"})

twelfth_grade_math_school = twelfth_graders.groupby(["school_name"])                       
twelfth_grade_math_scores=pd.DataFrame(twelfth_grade_math_school["math_score"].mean())
twelfth_math_scores = twelfth_grade_math_scores.rename(columns={"math_score":"12th grade"})

# Combine each of the scores above into single DataFrame called `math_scores_by_grade`
math_merge1 = pd.merge(ninth_math_scores, tenth_math_scores, on="school_name")
math_merge2 = pd.merge(math_merge1,eleventh_math_scores, on="school_name")
math_scores_by_grade = pd.merge(math_merge2, twelfth_math_scores, on="school_name")

# Minor data wrangling
math_scores_by_grade.index.name = None

# Display the DataFrame
math_scores_by_grade

# %% [markdown]
# ## Reading Score by Grade 

# %%
# Use the code provided to separate the data by grade
#ninth_graders = school_data_complete[(school_data_complete["grade"] == "9th")]
#tenth_graders = school_data_complete[(school_data_complete["grade"] == "10th")]
#eleventh_graders = school_data_complete[(school_data_complete["grade"] == "11th")]
#twelfth_graders = school_data_complete[(school_data_complete["grade"] == "12th")]

# Group by `school_name` and take the mean of the the `reading_score` column for each.
ninth_grade_reading_school = ninth_graders.groupby(["school_name"])                       
ninth_grade_reading_scores=pd.DataFrame(ninth_grade_reading_school["reading_score"].mean())
ninth_reading_scores = ninth_grade_reading_scores.rename(columns={"reading_score":"9th grade"})

tenth_grade_reading_school = tenth_graders.groupby(["school_name"])
tenth_grade_reading_scores = pd.DataFrame(tenth_grade_reading_school["reading_score"].mean())
tenth_reading_scores = tenth_grade_reading_scores.rename(columns={"reading_score":"10th grade"})

eleventh_grade_reading_school = eleventh_graders.groupby(["school_name"])                       
eleventh_grade_reading_scores=pd.DataFrame(eleventh_grade_reading_school["reading_score"].mean())
eleventh_reading_scores = eleventh_grade_reading_scores.rename(columns={"reading_score":"11th grade"})

twelfth_grade_reading_school = twelfth_graders.groupby(["school_name"])                       
twelfth_grade_reading_scores=pd.DataFrame(twelfth_grade_reading_school["reading_score"].mean())
twelfth_reading_scores = twelfth_grade_reading_scores.rename(columns={"reading_score":"12th grade"})

# Combine each of the scores above into single DataFrame called `reading_scores_by_grade`
reading_merge1 = pd.merge(ninth_reading_scores, tenth_reading_scores, on="school_name")
reading_merge2 = pd.merge(reading_merge1,eleventh_reading_scores, on="school_name")
reading_scores_by_grade = pd.merge(reading_merge2, twelfth_reading_scores, on="school_name")

# Minor data wrangling
reading_scores_by_grade = reading_scores_by_grade[["9th grade", "10th grade", "11th grade", "12th grade"]]
reading_scores_by_grade.index.name = None

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

# %%
# Use `pd.cut` to categorize spending based on the bins.
organized_df["Spending Ranges(Per Student)"]=pd.cut(organized_df["Per Student Budget"],spending_bins, labels=labels)

spending_math_scores = organized_df.groupby(["Spending Ranges(Per Student)"], observed=False)["Average Math Score"].mean()
spending_reading_scores = organized_df.groupby(["Spending Ranges(Per Student)"], observed=False)["Average Reading Score"].mean()
spending_passing_math = organized_df.groupby(["Spending Ranges(Per Student)"],observed=False)["% Passing Math"].mean()
spending_passing_reading = organized_df.groupby(["Spending Ranges(Per Student)"],observed=False)["% Passing Reading"].mean()
overall_passing_spending = organized_df.groupby(["Spending Ranges(Per Student)"],observed=False)["% Overall Passing"].mean()

spending_passing_reading

# %%
# Assemble into DataFrame

spend_merge_1 = pd.merge(spending_math_scores, spending_reading_scores, on="Spending Ranges(Per Student)")
spend_merge_2 = pd.merge(spend_merge_1, spending_passing_math, on="Spending Ranges(Per Student)")
spend_merge_3 = pd.merge(spend_merge_2, spending_passing_reading, on="Spending Ranges(Per Student)")
spending_summary = pd.merge(spend_merge_3,overall_passing_spending, on = "Spending Ranges(Per Student)")



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

organized_df["Total Students Ranges"]=pd.cut(organized_df["Students"],size_bins, labels=labels)



# %%
# Calculate averages for the desired columns. 
size_math_scores = organized_df.groupby(["Total Students Ranges"],observed=False)["Average Math Score"].mean()
size_reading_scores = organized_df.groupby(["Total Students Ranges"],observed=False)["Average Reading Score"].mean()
size_passing_math = organized_df.groupby(["Total Students Ranges"],observed=False)["% Passing Math"].mean()
size_passing_reading = organized_df.groupby(["Total Students Ranges"],observed=False)["% Passing Reading"].mean()
size_passing_overall = organized_df.groupby(["Total Students Ranges"],observed=False)["% Overall Passing"].mean()
size_student_budget = organized_df.groupby(["Total Students Ranges"],observed=False)["Per Student Budget"].mean()


# %%
# Create a DataFrame called `size_summary` that breaks down school performance based on school size (small, medium, or large).
# Use the scores above to create a new DataFrame called `size_summary`
size_merge_1 = pd.merge(size_math_scores, size_reading_scores, on="Total Students Ranges")
size_merge_2 = pd.merge(size_merge_1, size_passing_math, on="Total Students Ranges")
size_merge_3 = pd.merge(size_merge_2, size_passing_reading, on="Total Students Ranges")
size_merge_4 = pd.merge(size_merge_3,size_student_budget, on = "Total Students Ranges")
size_summary = pd.merge(size_merge_4,size_passing_overall, on = "Total Students Ranges")

# Display results
size_summary

# %% [markdown]
# ## Scores by School Type

# %%
# Group the per_school_summary DataFrame by "School Type" and average the results.
average_math_score_by_type = per_school_summary.groupby(["School Type"])["Average Math Score"].mean()
average_reading_score_by_type = per_school_summary.groupby(["School Type"])["Average Reading Score"].mean()
average_percent_passing_math_by_type = per_school_summary.groupby(["School Type"])["% Passing Math"].mean()
average_percent_passing_reading_by_type = per_school_summary.groupby(["School Type"])["% Passing Reading"].mean()
average_percent_overall_passing_by_type = per_school_summary.groupby(["School Type"])["% Overall Passing"].mean()

# %%
# Assemble the new data by type into a DataFrame called `type_summary`
type_merge_1 = pd.merge(average_math_score_by_type, average_reading_score_by_type, on="School Type")
type_merge_2 = pd.merge(type_merge_1, average_percent_passing_math_by_type, on="School Type")
type_merge_3 = pd.merge(type_merge_2, average_percent_passing_reading_by_type, on="School Type")
type_summary = pd.merge(type_merge_3,average_percent_overall_passing_by_type, on = "School Type")

# Display results
type_summary

# %%



