function getTimeString(){
    var currentTime = new Date ( );
    var currentHours = currentTime.getHours ( );
    var currentMinutes = currentTime.getMinutes ( );
    var currentSeconds = currentTime.getSeconds ( );
    var currentDate = currentTime.toDateString()
    // Pad the minutes and seconds with leading zeros, if required
    currentMinutes = ( currentMinutes < 10 ) ? "0" + currentMinutes : currentMinutes;
    currentSeconds = ( currentSeconds < 10 ) ? "0" + currentSeconds : currentSeconds;

    // Convert an hours component of "0" to "12"
    currentHours = ( currentHours == 0 ) ? 12 : currentHours;

    // Compose the string for display
    var currentTimeString = currentDate + " " + currentHours + ":" + currentMinutes + ":" + currentSeconds;

    return currentTimeString
}

function updateClock (){
    currentTimeString = getTimeString()
    
    $("#clock").html(currentTimeString);
        
 }

function writeTables(data){
    for (var key in data){
        dd = data[key]
        var tbl_body = ""
        $.each(dd, function() {
            var tbl_row = "";
            $.each(this, function(k, v){
                tbl_row += "<td>" + v + "</td>";
            });
            tbl_body += "<tr>" + tbl_row + "</tr>"
        });
        $('#' + key).html(tbl_body)
    }

    $('#lastupdated').html('Last updated '+ getTimeString())
}

function update(){
    $.ajax({url: "/update", success: function(result){
            writeTables(result);
        }});
}

$(document).ready(function()
{
    update()
    setInterval('updateClock()', 1000);
    setInterval('update()', 30000)
});