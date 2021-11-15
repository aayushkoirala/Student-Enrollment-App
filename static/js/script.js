function currClasses() {
    console.log("hello");

    const xhttp = new XMLHttpRequest();
    const method = "GET";
    const url = "http://127.0.0.1:5000/student/classes";
    const async = true;
    xhttp.open(method, url, async);
    xhttp.send();
    xhttp.onload = function() {
        const html = JSON.parse(this.responseText);
        console.log(html);
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