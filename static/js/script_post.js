function init(){
    let action = document.getElementById('action').innerText; 
    if (action === "add"){
        const form = document.getElementById('addEventForm');
        // create an event
        let default_formattedDate = document.getElementById('default_date').innerText;
        let date_from = document.getElementById('date_from');
        let date_to = document.getElementById('date_to');
        date_from = formattedDate(default_formattedDate);
        date_to = formattedDate(default_formattedDate);
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            if (addEvent()) {
                form.submit();
            } else {
                alert("End date should not be earlier than the start date.");
            }
        })

    } else {
        // edit an event
        const form = document.getElementById('editEventForm');
        let edit_date_from = document.getElementById('edit_date_fm').innerText;
        let edit_date_to = document.getElementById('edit_date_to').innerText;
        let target_date_fm = document.getElementById('target_date_fm');
        let target_date_to = document.getElementById('target_date_to');
        target_date_fm.value = formattedDate(edit_date_from);
        target_date_to.value = formattedDate(edit_date_to);
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            if (editEvent()) {
                form.submit();
            } else {
                alert("End date should not be earlier than the start date.");
            }
        })
    }
}

function formattedDate(targetDate){
    // Convert the date string to a JavaScript Date object
    let jsDate = new Date(targetDate);
    // Format jsDate to "yyyy-MM-dd"
    let year = jsDate.getFullYear();
    let month = String(jsDate.getMonth() + 1).padStart(2, '0');  // Months are zero-indexed
    let day = String(jsDate.getDate()).padStart(2, '0');

    let formattedDate =  `${year}-${month}-${day}`;
    return formattedDate;
}

function addEvent(){
    let date_fm = document.getElementById('date_from').value;
    let date_to = document.getElementById('date_to').value;
    if (isStartDateEarlierEndDate(date_fm, date_to)) {
        return true;
        // Place any additional code you want to execute when date_from is NOT earlier than date_to here.
      } else {
        return false;
        // Place any code here for when the dates are correctly ordered.
      }
}

function editEvent() {
    let date_fm = document.getElementById('target_date_fm').value;
    let date_to = document.getElementById('target_date_to').value;
    // Compare the date from with the date to
    if (isStartDateEarlierEndDate(date_fm, date_to)) {
        return true;
        // Place any additional code you want to execute when date_from is NOT earlier than date_to here.
    } else {
        return false;
        // Place any code here for when the dates are correctly ordered.
    }
}

function isStartDateEarlierEndDate(dateFrom, dateTo) {
    const dateFromObj = new Date(dateFrom);
    const dateToObj = new Date(dateTo);
    console.log("isDateFormEarlier");
    if (dateFromObj.getTime() <= dateToObj.getTime()) 
    {
        return true; // dateFrom is earlier than dateTo
    } else {
        return false; // dateFrom is not earlier than dateTo
    }
}

addEventListener('load', init);
