
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
students = []

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form["name"].strip()
        marks = float(request.form["marks"])

        if name and 0 <= marks <= 100:
            grade = (
                "A" if marks >= 90 else
                "B" if marks >= 75 else
                "C" if marks >= 60 else
                "D" if marks >= 40 else "Fail"
            )

            students.append({
                "id": len(students) + 1,
                "name": name,
                "marks": marks,
                "grade": grade
            })

        return redirect("/")

    search = request.args.get("search", "").strip().lower()
    filtered = [
        s for s in students
        if search in s["name"].lower()
    ]

    return render_template(
        "index.html", students=filtered, search=search
    )

@app.route("/edit/<int:student_id>", methods=["POST"])
def edit(student_id):
    for student in students:
        if student["id"] == student_id:
            try:
                marks = float(request.form["marks"])
                if 0 <= marks <= 100:
                    student["marks"] = marks
                    student["grade"] = (
                        "A" if marks >= 90 else
                        "B" if marks >= 75 else
                        "C" if marks >= 60 else
                        "D" if marks >= 40 else "Fail"
                    )
            except ValueError:
                pass
            break

    return redirect("/")

@app.route("/delete/<int:student_id>", methods=["POST"])
def delete(student_id):
    students[:] = [
        s for s in students if s["id"] != student_id
    ]
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
