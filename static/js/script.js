
function login()
{
    var username = document.getElementById("username")
    var password = document.getElementById("password")
    print('------------')
    console.log(username)
    console.log(password)

    fetch("http://127.0.0.1:5000/login", {
          method: `POST`,
          body: JSON.stringify({username:username,password:password
          }),
          headers: {
              "Content-type": "application/json charset=UTF-8"
          }
      })
      .then(function (response) {
        if (response.status !== 200) {
          console.log(`Looks like there was a problem. Status code: ${response.status}`);
          return;
        }
        response.json().then(function (data) {
          console.log(data);
        });
      })
      .catch(function (error) {
        console.log("Fetch error: " + error);
      });

}