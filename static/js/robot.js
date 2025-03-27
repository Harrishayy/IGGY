//function runs an AJAX post to the server to tell the robot which direction to move and at what speed
function move_robot(direction) {
    const speed = document.getElementById("speed").value;

    $.ajax({
        url: "/robot-move",
        type: "POST",
        data: JSON.stringify({"speed":speed, "direction":direction}),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(response) {
            console.log(response["log"]);
        }
    });
};

function accelerometer(){
    $.ajax({
        url: "/accelerometer",
        type: "POST",
        data: JSON.stringify({}),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(response) {
            console.log(response["log"]);
        }
    });
}

//adds a listener to the webpage so that we can use w,a,s,d controls
document.addEventListener("keydown", function(event) {
    if(event.key == "w") {
        move_robot("w");
    }
    else if(event.key == "s") {
        move_robot("s");
    }
    else if(event.key == "a") {
        move_robot("a");
    }
    else if(event.key == "d") {
        move_robot("d");
    }
    else if(event.key == "q") {
        move_robot("stop");
    }
});

setInterval(accelerometer, 1000);