function init(){
    let action = document.getElementById('action').innerText; 
    if (action === "add"){
        const form = document.getElementById('addPostForm');
        // create a post
        let default_formattedDate = document.getElementById('default_date').innerText;
        let date_from = document.getElementById('date_fm');
        let date_to = document.getElementById('date_to');
        date_from.value = formattedDate(default_formattedDate);
        date_to.value = formattedDate(default_formattedDate);
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            if (addPost()) {
                form.submit();
            } else {
                alert("An date error has occurred.");
            }
        })

    } else {
        // edit a post
        const form = document.getElementById('editPostForm');
        console.log('addPost.');
        let edit_date_from = document.getElementById('edit_date_fm').innerText;
        let edit_date_to = document.getElementById('edit_date_to').innerText;
        let target_date_fm = document.getElementById('target_date_fm');
        let target_date_to = document.getElementById('target_date_to');
        target_date_fm.value = formattedDate(edit_date_from);
        target_date_to.value = formattedDate(edit_date_to);
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            if (editPost()) {
                form.submit();
            } else {
                alert("An date error has occurred.");
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

function addPost(){
    let date_fm = document.getElementById('date_fm').value;
    let date_to = document.getElementById('date_to').value;
    if (isDateFormEarlier(date_fm, date_to)) {
        return true;
        // Place any additional code you want to execute when date_from is NOT earlier than date_to here.
      } else {
        return false;
        // Place any code here for when the dates are correctly ordered.
      }
}

function editPost() {
    let date_fm = document.getElementById('target_date_fm').value;
    let date_to = document.getElementById('target_date_to').value;
    // Compare the date from with the date to
    if (isDateFormEarlier(date_fm, date_to)) {
        return true;
        // Place any additional code you want to execute when date_from is NOT earlier than date_to here.
    } else {
        return false;
        // Place any code here for when the dates are correctly ordered.
    }
}

function isDateFormEarlier(dateFrom, dateTo) {
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
