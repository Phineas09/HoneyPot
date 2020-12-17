function loadAllPackets() {

    let formData = new FormData();
    
    formData.append('getAllContents', true);

    var request = new XMLHttpRequest();

	request.onreadystatechange = function() {
        if(this.readyState == 4 && this.status == 200) {
            //console.log(this.responseText);
            var response = JSON.parse(this.responseText);
            if(response.statusCode == 200) {
                document.getElementById("tableContents").innerHTML = response.returnValue;
            }
        }
    };
    
	request.open('POST', '/PHP/backEnd.php');
	request.send(formData);
}

function getNumberOfAttacksToday() {

    let formData = new FormData();
    
    formData.append('getNumberOfAttacksToday', true);

    var request = new XMLHttpRequest();

	request.onreadystatechange = function() {
        if(this.readyState == 4 && this.status == 200) {
            //console.log(this.responseText);
            var response = JSON.parse(this.responseText);
            if(response.statusCode == 200) {
                document.getElementById("todayCount").innerHTML = response.returnValue;
            }
        }
    };
    
	request.open('POST', '/PHP/backEnd.php');
	request.send(formData);
}

loadAllPackets();
getNumberOfAttacksToday();