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
                //console.log(html[key]["num_enrolled"]);
        }
        text += "</table>";
        
        document.getElementById("currentClasses").innerHTML = text;
    };
}

function potentialClasses(){
    const xhttp = new XMLHttpRequest();
    const method = "GET";
    const url = "http://127.0.0.1:5000/student/potential_classes";
    const async = true;
    xhttp.open(method, url, async);
    xhttp.send();
    xhttp.onload = function() {
        const html = JSON.parse(this.responseText);
        let text =
            "<table><tr><th>Course Name</th><th>Teacher</th><th>Time</th><th>Students Enrolled</th><th>Add Course</th></tr>";
        for (key in html) {
            
            
            if(html[key]["addable"] === 1)
            {
            let btn = document.createElement("button"); 
            btn.innerHTML = "+";
            document.body.appendChild(btn);
            text +=
                "<tr><td id='potenta'>" + 
                html[key]["class_name"] +"</td><td>" +
                html[key]["teacher_name"] +"</td><td>" +
                html[key]["time"] +"</td><td>" +
                html[key]["num_enrolled"] +"/" + html[key]["capacity"] +
                "</td><td>" + btn +"</td></tr>";
            }

            if(html[key]["addable"] === 0)
            {
            text +=
                "<tr><td>" + 
                html[key]["class_name"] +"</td><td>" +
                html[key]["teacher_name"] +"</td><td>" +
                html[key]["time"] +"</td><td>" +
                html[key]["num_enrolled"] +"/" + html[key]["capacity"] +
                "</td><td>"+ "<button type='button' disabled>+</button>"+"</td></tr>";
            }
           
            
        }
        text += "</table>";

        document.getElementById("potentialClasses").innerHTML = text;
    };

    

}
function allClasses() {
    console.log("hellddddo");

    const xhttp = new XMLHttpRequest();
    const method = "GET";
    const url = "http://127.0.0.1:5000/student/all_classes";
    const async = true;
    xhttp.open(method, url, async);
    xhttp.send();
    xhttp.onload = function() {
        const html = JSON.parse(this.responseText);
        console.log(html);
        // let text =
        //     "<table><tr><th>Course Name</th><th>Teacher</th><th>Time</th><th>Students Enrolled</th></tr>";
        // for (key in html) {
        //     text +=
        //         "<tr><td>" +
        //         html[key]["class_name"] +
        //         "</td><td>" +
        //         html[key]["teacher_name"] +
        //         "</td><td>" +
        //         html[key]["time"] +
        //         "</td><td>" +
        //         html[key]["num_enrolled"] +
        //         "/" +
        //         html[key]["capacity"] +
        //         "</td></tr>";
        // }
        // text += "</table>";

        // document.getElementById("currentClasses").innerHTML = text;
    };
}


// btn.onclick = (
//     function(entry){
//         return function(){
//             chooseUser(entry);
//         }
//     }
//     )(entry);
