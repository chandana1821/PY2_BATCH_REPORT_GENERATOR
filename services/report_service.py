import pandas as pd
import os
import json

class ReportService:

    def __init__(self, input_folder, output_folder):
        self.input_folder = input_folder
        self.output_folder = output_folder

    def load_data(self):
        try:
            students = pd.read_csv(os.path.join(self.input_folder, "students.csv"))
            attendance = pd.read_csv(os.path.join(self.input_folder, "attendance.csv"))
            return students, attendance
        except FileNotFoundError as e:
            print("Error: Required input file missing.")
            print(e)
            exit()

    def clean_data(self, df):
        df = df.drop_duplicates()
        df = df.fillna(0)
        return df

    def generate_report(self):

        students, attendance = self.load_data()

        students = self.clean_data(students)
        attendance = self.clean_data(attendance)

        merged = pd.merge(students, attendance, on="studentId")

        merged["avgMarks"] = merged["marks"]
        merged["status"] = merged["avgMarks"].apply(lambda x: "PASS" if x >= 50 else "FAIL")

        report = merged[["studentId", "name", "attendancePercent", "avgMarks", "status"]]

        report_path = os.path.join(self.output_folder, "report.csv")
        report.to_csv(report_path, index=False)

        summary = {
            "totalStudents": len(report),
            "avgAttendance": float(report["attendancePercent"].mean()),
            "avgMarks": float(report["avgMarks"].mean()),
            "passCount": int((report["status"] == "PASS").sum()),
            "failCount": int((report["status"] == "FAIL").sum()),
            "top3Students": report.sort_values(by="avgMarks", ascending=False)["name"].head(3).tolist()
        }

        summary_path = os.path.join(self.output_folder, "summary.json")

        with open(summary_path, "w") as f:
            json.dump(summary, f, indent=4)

        print("Reports generated successfully!")