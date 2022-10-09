"use strict";

$("#swal-1").click(function() {
    swal('Hello');
});

$("#swal-2").click(function() {
    swal('Good Job', 'You clicked the button!', 'success');
});

$("#swal-3").click(function() {
    swal('Good Job', 'You clicked the button!', 'warning');
});

$("#swal-4").click(function() {
    swal('Good Job', 'You clicked the button!', 'info');
});

$("#swal-5").click(function() {
    swal('Good Job', 'You clicked the button!', 'error');
});

$("#swal-uploaded").click(function() {
    swal('Uploaded', 'This hourly reading has been uploaded', 'error');
});


$("#swal-7").click(function() {
    swal({
        title: 'What is your name?',
        content: {
            element: 'input',
            attributes: {
                placeholder: 'Type your name',
                type: 'text',
            },
        },
    }).then((data) => {
        swal('Hello, ' + data + '!');
    });
});

$("#swal-8").click(function() {
    swal('This modal will disappear soon!', {
        buttons: false,
        timer: 3000,
    });
});