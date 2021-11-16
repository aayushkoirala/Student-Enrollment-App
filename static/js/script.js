function currClasses() {
    const xhttp = new XMLHttpRequest();
    const method = "GET";
    const url = "http://127.0.0.1:5000/student/classes";
    const async = true;
    xhttp.open(method, url, async);
    xhttp.send();
    xhttp.onload = function() {
        const html = JSON.parse(this.responseText);
        let text =
            "<table><tr><th>Course Name</th><th>Teacher</th><th>Time</th><th>Students Enrolled</th></tr>";
        for (key in html) {
            text +=
                "<tr><td>" +
                html[key]["class_name"] +
                "</td><td>" +
                html[key]["teacher_name"] +
                "</td><td>" +
                html[key]["time"] +
                "</td><td>" +
                html[key]["num_enrolled"] +
                "/" +
                html[key]["capacity"] +
                "</td></tr>";
        }
        text += "</table>";

        document.getElementById("currentClasses").innerHTML = text;
    };
}

function getTeacherClasses() {
    const xhttp = new XMLHttpRequest();
    const method = "GET";
    const url = "http://127.0.0.1:5000/teacher/classes";
    const async = true;
    xhttp.open(method, url, async);
    xhttp.send();
    xhttp.onload = function() {
        const html = JSON.parse(this.responseText);
        console.log(html);
        let text =
            "<table><tr><th>Course Name</th><th>Teacher</th><th>Time</th><th>Students Enrolled</th></tr>";
        for (key in html) {
            console.log(key);
            text +=
                "<tr><td>" +
                "<a href='/student_grades/" +
                key +
                "'>" +
                html[key]["class_name"] +
                "</a>" +
                "</td><td>" +
                html[key]["teacher_name"] +
                "</td><td>" +
                html[key]["time"] +
                "</td><td>" +
                html[key]["num_enrolled"] +
                "/" +
                html[key]["capacity"] +
                "</td></tr>";
        }
        text += "</table>";

        document.getElementById("currentClasses").innerHTML = text;
    };
}

function getGrades(class_id) {
    console.log(class_id);
    const xhttp = new XMLHttpRequest();
    const method = "GET";

    const url = "http://127.0.0.1:5000/student_get_grades/" + class_id;
    const async = true;
    xhttp.open(method, url, async);
    xhttp.send();
    xhttp.onload = function() {
        console.log(this.responseText);
        const html = JSON.parse(this.responseText);
        let text =
            "<table id='students'><tr><th>Student Name</th><th>Grade</th></tr>";
        for (key in html) {
            console.log(key);
            text +=
                "<tr><td name='name'>" +
                html[key]["student_name"] +
                "</td><td>" +
                "<input type='text' name='grade_values' value=" +
                html[key]["grade"] +
                ">" +
                "</td></tr>";
        }
        text += "</table>";
        console.log(text);
        document.getElementById("currentStudents").innerHTML = text;
    };
}

function updateDB() {
    var input = document.getElementsByName("grade_values");
    var table = document.getElementById("students");
    var student = [];
    var student_grade = [];
    for (var r = 1, n = table.rows.length; r < n; r++) {
        student.push(table.rows[r].cells[0].innerHTML);
    }
    for (var i = 0; i < input.length; i++) {
        var a = input[i];
        student_grade.push(a.value);
    }
    var json_data = new Object();
    for (var i = 0; i < student_grade.length; i++) {
        json_data[student[i]] = student_grade[i];
    }
    const xhttp = new XMLHttpRequest();
    const method = "PUT";

    const url = "http://127.0.0.1:5000/update_grades";
    const async = true;
    xhttp.open(method, url, async);
    console.log(json_data);
    xhttp.send(JSON.stringify(json_data));
}