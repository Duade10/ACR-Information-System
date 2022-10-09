function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

function getDateTimeAndScheduledReports() {
    /* Displays sweet alert for application for protection guarantee. */

    $.ajax({
        url: "/get-date-time-and-scheduled-reports/",
        dataType: 'json',
        success: function(res) {
            console.log(res);
            if (res.pr_report.bool === true) {
                displayNotification('application for protection guratantee', res.pr_report.name, res.pr_report.station, res.pr_report.time, res.pr_report.for_a, res.pr_report.time_from, res.pr_report.time_to, res.pr_report.url, res.pr_report.stationId, res.pr_report.station330Id);
            }
        }
    })
}
// ===========GET REQUEST ==============

function getChartReading() {
    $.ajax({
        url: "/get-stations-last-load/",
        dataType: 'json',
        beforeSend: function() {
            $("#refresh-station-load-button").addClass("btn-progress")
        },
        success: function(res) {
            if (res.success === false) {
                failNotification("Couldn't get last station load");
            }
            var statistics_chart = document.getElementById("myChart").getContext('2d');
            var ctx = document.getElementById("myChart4").getContext('2d');
            var myChart = new Chart(ctx, {
                type: 'pie',
                data: {
                    datasets: [{
                        data: res.sub_stations_load,
                        backgroundColor: [
                            '#191d21',
                            '#63ed7a',
                            '#ffa426',
                            '#fc544b',
                            '#6777ef',
                            '#3f0000',
                            '#008080',
                            '#319230',
                            '#ffd700',
                        ],
                        label: 'Dataset 1'
                    }],
                    labels: res.sub_stations,
                },
                options: {
                    responsive: true,
                    legend: {
                        position: 'bottom',
                    },
                }
            });
            $("#refresh-station-load-button").removeClass("btn-progress")
        },
        failure: function() {
            $("#refresh-station-load-button").removeClass("btn-progress")
        },
        error: function(data, status, error) {
            console.log(status)
            if (status === "timeout") {
                failNotification("Timeout. Couldn't get last station load. Slow Network");

            } else {
                failNotification(" Couldn't get last station load");
                $("#refresh-station-load-button").removeClass("btn-progress")
            }
        }
    })
}


function getHourlyReading() {
    $.ajax({
        url: "/get-hourly-reading/",
        dataType: "json",
        timeout: 3000,
        success: function(res) {
            var statistics_chart = document.getElementById("myChart").getContext('2d');
            new Chart(statistics_chart, {
                type: 'line',
                data: {
                    labels: res.reading_hour,
                    datasets: [{
                        label: 'Station Load',
                        data: res.reading_load,
                        borderWidth: 5,
                        borderColor: '#6777ef',
                        backgroundColor: 'transparent',
                        pointBackgroundColor: '#fff',
                        pointBorderColor: '#6777ef',
                        pointRadius: 4
                    }]
                },
                options: {
                    legend: {
                        display: false
                    },
                    scales: {
                        yAxes: [{
                            gridLines: {
                                display: false,
                                drawBorder: false,
                            },
                            ticks: {
                                stepSize: 150
                            }
                        }],
                        xAxes: [{
                            gridLines: {
                                color: '#fbfbfb',
                                lineWidth: 2
                            }
                        }]
                    },
                }
            });
        },
        failure: function() {},
        error: function(data, status, error) {
            console.log(status)
            if (status === "timeout") {
                failNotification("Timeout. Couldn't get hourly reading. Slow Network");

            } else {
                failNotification(" Couldn't get hourly reading");
            }
        }
    })
}

// ==================FORM SUBMISSION==============

$('#GoogleSheetUpdate-form').on('submit', function(e) {
    e.preventDefault();
    let url = $('#google-sheet-url').val();
    let sheetId = url.match(/\/d\/(.+)\//);
    $.ajax({
        type: 'POST',
        url: "/settings/google-sheet-update/",
        data: {
            sheetPk: $('#google-sheet-id').val(),
            sheetId: sheetId[1],
            csrfmiddlewaretoken: getCookie('csrftoken'),
            dataType: "json",
        },
        success: function(data) {
            $('#output').html(data)
            successNotification(data.msg);
            $(".btn").removeClass("btn-progress");
            $('#google-sheet-display').load(' #google-sheet-display', function() {
                $(this).children().unwrap()
            });
        },
        failure: function() {
            var msg = "Update failed"
            failNotification(msg);
        },
        error: function(data, status, error) {
            console.log(status)
            if (status === "timeout") {
                failNotification("Update Failed. Timeout. Try again slow internet");
            } else {
                failNotification("Update Failed");
                $(".btn").removeClass("btn-progress")
            }
        }
    })
})



$('#operational-form').on('submit', function(e) {

    e.preventDefault();
    console.log($('#id_phase').val());
    $.ajax({
        type: "POST",
        url: "/reports/operational-reports/create/",
        data: {
            fromTime: $('#id_from_time').val(),
            toTime: $('#id_to_time').val(),
            feeder: $('#id_feeder').val(),
            reason: $('#id_reason').val(),
            phase: $('#id_phase').val(),
            frequency: $('#id_frequency').val(),
            loadLoss: $('#id_load_loss').val(),
            dispatch: $('#id_dispatch').val(),
            description: $('#id_description').val(),
            csrfmiddlewaretoken: getCookie('csrftoken'),
            dataType: "json",

        },

        success: function(data) {
            $('#output').html(data)
            successNotification(data.msg);
            $('#id_from_time').val('');
            $('#id_to_time').val('');
            $('#id_feeder').val('');
            $('#id_reason').val('');
            $('#id_phase').val('');
            $('#id_frequency').val('');
            $('#id_load_loss').val('');
            $('#id_dispatch').val('');
            $('#id_description').val('');


        },

        failure: function() {
            var msg = 'Your form did not submit sucessfully'
            failNotification(msg);

        }


    });


});





//================STATIONS HOURLY READING==================

// AYEDE 330 AJAX

function Ayede330HourlyUploadSingleReading(readingPk) {
    // FUNCTIONS SENDS HOURLY READING PRIMARY KEY TO AYEDE 330 HOURLY READING VIEW: 
    $.ajax({
        type: "POST",
        url: "/readings/ayede-330-hourly-reading/upload-single/",
        data: {
            readingPk: readingPk,
            csrfmiddlewaretoken: getCookie('csrftoken'),
            dataType: "json",

        },
        timeout: 15000,
        retryCount: 0,
        retryLimit: 1,
        beforeSend: function() {
            $(".btn").addClass("btn-progress")
        },

        success: function(data) {
            $('#output').html(data)
            successNotification(data.msg);
            $(".btn").removeClass("btn-progress");



        },

        failure: function() {
            var msg = 'Reading not uploaded successfully'
            failNotification(msg);

        },
        error: function(data, status, error) {
            console.log(status)
            if (status === "timeout") {
                failNotification("Timeout. Update Failed. Slow Network");
                $.ajax(this);
                return;


            } else {
                failNotification("Upload Failed");
                $(".btn").removeClass("btn-progress")


            }
        }


    });

}

function Ayede330HourlyClearSingleReading(readingPk) {
    // FUNCTIONS SENDS HOURLY READING PRIMARY KEY TO AYEDE 330 HOURLY READING VIEW: 
    $.ajax({
        type: "POST",
        url: "/readings/ayede-330-hourly-reading/clear/",
        data: {
            readingPk: readingPk,
            csrfmiddlewaretoken: getCookie('csrftoken'),
            dataType: "json",

        },
        timeout: 15000,
        retryCount: 0,
        retryLimit: 1,
        beforeSend: function() {
            $(".btn").addClass("btn-progress")
        },

        success: function(data) {
            $('#output').html(data)
            successNotification(data.msg);
            $(".btn").removeClass("btn-progress");
            $('#ayede-hourly-reading').load(' #ayede-hourly-reading', function() {
                $(this).children().unwrap()
            });
            socket.send('hourly_reading');
        },

        failure: function() {
            var msg = 'Reading not uploaded successfully'
            failNotification(msg);

        },
        error: function(data, status, error) {
            console.log(status)
            if (status === "timeout") {
                failNotification("Timeout. Update Failed. Slow Network");
                $.ajax(this);
                return;


            } else {
                failNotification("Upload Failed");
                $(".btn").removeClass("btn-progress")


            }
        }


    });

}

// AYEDE 132 AJAX

function Ayede132HourlyUploadSingleReading(readingPk) {
    // FUNCTIONS SENDS HOURLY READING PRIMARY KEY TO AYEDE 330 HOURLY READING VIEW: 
    $.ajax({
        type: "POST",
        url: "/readings/ayede-132-hourly-reading/upload-single/",
        data: {
            readingPk: readingPk,
            csrfmiddlewaretoken: getCookie('csrftoken'),
            dataType: "json",

        },
        timeout: 5000,
        retryCount: 0,
        retryLimit: 1,
        beforeSend: function() {
            $(".btn").addClass("btn-progress")
        },

        success: function(data) {
            $('#output').html(data)
            successNotification(data.msg);
            $(".btn").removeClass("btn-progress");
            $('#hourly-reading').load(' #hourly-reading', function() {
                $(this).children().unwrap()
            });
        },

        failure: function() {
            var msg = 'Reading not uploaded successfully'
            failNotification(msg);

        },
        error: function(data, status, error) {
            console.log(status)
            if (status === "timeout") {
                failNotification("Timeout. Update Failed. Slow Network");
                $.ajax(this);
                return;


            } else {
                failNotification("Upload Failed");
                $(".btn").removeClass("btn-progress")


            }
        }


    });

}


//==================DOCUMENTS.READY==================
$(document).ready(function() {
    if (window.location.pathname === '/') {
        getHourlyReading();
        getChartReading();
    }
});



setInterval(function() {
    getDateTimeAndScheduledReports();
}, 120000)