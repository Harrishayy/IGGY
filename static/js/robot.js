function move_robot(direction) {
    const speed = document.getElementById("speed").value;
    const time = document.getElementById("time").value;

    console.log(speed,time);

    $.ajax({
        url: "/robot-move",
        type: "POST",
        data: JSON.stringify({"speed":speed, "time":time, "direction":direction}),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(response) {
            console.log(response);
        }
    });
};

document.addEventListener('keydown', function(event) {
    if(event.key == 'w') {
        move_robot('w');
    }
    else if(event.key == 's') {
        move_robot('s');
    }
    else if(event.key == 'a') {
        move_robot('a');
    }
    else if(event.key == 'd') {
        move_robot('d');
    }
});