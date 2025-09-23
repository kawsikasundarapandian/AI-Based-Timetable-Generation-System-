from ortools.sat.python import cp_model
import pandas as pd

courses = ['Math', 'Physics', 'Chemistry', 'Biology', 'Computer']
faculty = ['Alice', 'Bob', 'Charlie', 'David', 'Eva']
faculty_mapping = dict(zip(courses, faculty))

rooms = ['R1', 'R2', 'R3']

days = ['Mon', 'Tue', 'Wed']

timetable = pd.DataFrame(columns=['Day', 'Course', 'Staff', 'Room'])
model = cp_model.CpModel()

course_vars = {}
for course in courses:
    for day in days:
        for room in rooms:
            course_vars[(course, day, room)] = model.NewBoolVar(f'{course}_{day}_{room}')

for course in courses:
    model.Add(sum(course_vars[(course, day, room)]
                  for day in days for room in rooms) == 1)

for day in days:
    for room in rooms:
        model.Add(sum(course_vars[(course, day, room)] for course in courses) <= 1)

for day in days:
    for f in faculty:
        model.Add(sum(course_vars[(course, day, room)]
                      for course, fac in faculty_mapping.items() if fac==f
                      for room in rooms) <= 1)
solver = cp_model.CpSolver()
status = solver.Solve(model)

if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
    rows = []
    for course in courses:
        for day in days:
            for room in rooms:
                if solver.Value(course_vars[(course, day, room)]) == 1:
                    rows.append({
                        'Day': day,
                        'Course': course,
                        'Staff': faculty_mapping[course],
                        'Room': room
                    })
    timetable = pd.concat([timetable, pd.DataFrame(rows)], ignore_index=True)
    print("Timetable Generated Successfully!\n")
    display(timetable.sort_values(by=['Day']))
else:
    print("No feasible timetable found.")
timetable.to_csv('generated_timetable.csv', index=False)
print("Timetable saved as 'generated_timetable.csv'")
