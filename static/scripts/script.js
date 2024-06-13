// classroom.html
// const classroomName = document.querySelector('#classname'); 
// let currentClassroomIndex = 0;
// const classrooms = [{% for classroom in classrooms %}{ id: {{ classroom.id }}, name: "{{ classroom.name }}" }{% if not forloop.last %},{% endif %}{% endfor %}];


function updateClassroomName() {
    classroomName.textContent = classrooms[currentClassroomIndex].name;
}

function redirectToClassroom() {
    const classroomId = classrooms[currentClassroomIndex].id;
    window.location.href = `/classrooms/${classroomId}/topics/`;
}

function changeClassroom(direction) {
    if (direction === 'next') {
        currentClassroomIndex = (currentClassroomIndex + 1) % classrooms.length;
    } else if (direction === 'previous') {
        currentClassroomIndex = (currentClassroomIndex - 1 + classrooms.length) % classrooms.length;
    }
    updateClassroomName(); 
}







// topic_tasks
document.addEventListener("DOMContentLoaded", function() {
    var links = document.querySelectorAll('.lbl-nums a');
    links.forEach(function(link, index) {
        link.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent default link behavior
            var allDivs = document.querySelectorAll('.lbl-nums div');
            allDivs.forEach(function(div) {
                div.classList.remove('active'); // Remove active class from all divs
            });
            // Add active class to the parent div of the clicked link
            link.parentNode.classList.add('active');
        });
    });
});

var canvas, ctx, flag = false,
    prevX = 0,
    currX = 0,
    prevY = 0,
    currY = 0,
    dot_flag = false;

var selectedColor = "black";
var selectedLineWidth = 2;
var pencilActive = false;

function init() {
    if (pencilActive) {
        canvas.removeEventListener("mousemove", findxy);
        canvas.removeEventListener("mousedown", findxy);
        canvas.removeEventListener("mouseup", findxy);
        canvas.removeEventListener("mouseout", findxy);
        pencilActive = false;
    } else {
        canvas = document.getElementById('can');
        ctx = canvas.getContext("2d");
        w = canvas.width;
        h = canvas.height;
        ctx.lineCap = "round"

        canvas.addEventListener("mousemove", findxy);
        canvas.addEventListener("mousedown", findxy);
        canvas.addEventListener("mouseup", findxy);
        canvas.addEventListener("mouseout", findxy);
        pencilActive = true;
    }
}

function color(obj) {
    selectedColor = obj.style.backgroundColor;
}

function line(obj) {
    switch (obj.id) {
        case "two":
            selectedLineWidth = 2;
            break;
        case "three":
            selectedLineWidth = 6;
            break;
        case "four":
            selectedLineWidth = 10;
            break;
    }
}

function draw() {
    ctx.beginPath();
    ctx.moveTo(prevX, prevY);
    ctx.lineTo(currX, currY);
    ctx.strokeStyle = selectedColor;
    ctx.lineWidth = selectedLineWidth;
    ctx.stroke();
    ctx.closePath();
}

function erase() {
    var m = confirm("Суретті өшіргіңіз келеді ме?");
    if (m) {
        ctx.clearRect(0, 0, w, h);
        document.getElementById("canvasimg").style.display = "none";
    }
}

function findxy(e) {
    if (e.type == 'mousedown') {
        prevX = currX;
        prevY = currY;
        currX = e.clientX - canvas.getBoundingClientRect().left;
        currY = e.clientY - canvas.getBoundingClientRect().top;

        flag = true;
        dot_flag = true;
        if (dot_flag) {
            ctx.beginPath();
            ctx.fillStyle = selectedColor;
            ctx.fillRect(currX, currY, 2, 2);
            ctx.closePath();
            dot_flag = false;
        }
    }
    if (e.type == 'mouseup' || e.type == "mouseout") {
        flag = false;
    }
    if (e.type == 'mousemove') {
        if (flag) {
            prevX = currX;
            prevY = currY;
            currX = e.clientX - canvas.getBoundingClientRect().left;
            currY = e.clientY - canvas.getBoundingClientRect().top;
            draw();
        }
    }
}
function openClsIns() {
    document.getElementById("cls-ins").style.display = "block";
}

function closeClsIns() {
    document.getElementById("cls-ins").style.display = "none";
}




// book
const images = document.querySelectorAll('.img');

let zoomEnabled = false;

function enableZoom() {
    zoomEnabled = true;
}

function disableZoom() {
    zoomEnabled = false;
    images.forEach(img => {
        img.removeEventListener("mousemove", onMouseMove);
        img.removeEventListener("mouseleave", onMouseLeave);
        img.style.transformOrigin = "center";
        img.style.transform = "scale(1)";
    });
}

images.forEach(img => {
    img.addEventListener('mouseenter', () => {
        if (zoomEnabled) {
            img.addEventListener("mousemove", onMouseMove);
            img.addEventListener("mouseleave", onMouseLeave);
        }
    });
});

function onMouseMove(e) {
    const x = e.clientX - e.target.offsetLeft;
    const y = e.clientY - e.target.offsetTop;

    e.target.style.transformOrigin = `${x}px ${y}px`;
    e.target.style.transform = "scale(2)";
}

function onMouseLeave(e) {
    e.target.style.transformOrigin = "center";
    e.target.style.transform = "scale(1)";
}




// navbar
function openIns() {
    document.getElementById("ins").style.display = "block";
}
    function closeIns() {
    document.getElementById("ins").style.display = "none";
}
    function openSet() {
    document.getElementById("set").style.display = "block";
}
    function closeSet() {
    document.getElementById("set").style.display = "none";
}