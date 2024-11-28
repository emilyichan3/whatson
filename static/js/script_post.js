const setDateError = () => {
    // below is adding error class in the input-date elements.
    const inputDateControls = document.querySelectorAll('input[type="date"]');
   
    inputDateControls.forEach((input) => {
        console.log(input);
        input.classList.add('error');
        input.classList.remove('success');
    });
};


function init(){
    // if there is a date-error shown on flashes container
    let flashMessages = document.getElementsByClassName('date-error');
    if (flashMessages.length > 0) {
        // adding error class in the input-date elements.
        setDateError();
    }
        
    let action = document.getElementById('action').innerText; 
    // using action to distinguish the elements in content 
    if (action === "add"){
        // create an event
        const form = document.getElementById('addEventForm');
        
        let default_formattedDate = document.getElementById('default_date').innerText;
        let date_from = document.getElementById('date_from');
        let date_to = document.getElementById('date_to');
        // Set default values for both date inputs
        date_from = formattedDate(default_formattedDate);
        date_to = formattedDate(default_formattedDate);

        form.addEventListener('submit', function(event) {
            event.preventDefault();
            form.submit();
        })

    } else if (action === "edit") {
        // edit exist event
        const form = document.getElementById('editEventForm');
        let edit_date_from = document.getElementById('edit_date_fm').innerText;
        let edit_date_to = document.getElementById('edit_date_to').innerText;
        let target_date_fm = document.getElementById('target_date_fm');
        let target_date_to = document.getElementById('target_date_to');
        target_date_fm.value = formattedDate(edit_date_from);
        target_date_to.value = formattedDate(edit_date_to);
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            form.submit();
        })
    } else {
        const form = document.getElementById('editEventForm');
        let edit_date_from = document.getElementById('edit_date_fm').innerText;
        let edit_date_to = document.getElementById('edit_date_to').innerText;
        let target_date_fm = document.getElementById('target_date_fm');
        let target_date_to = document.getElementById('target_date_to');
        target_date_fm.value = formattedDate(edit_date_from);
        target_date_to.value = formattedDate(edit_date_to);
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

function isStartDateEarlierEndDate(dateFrom, dateTo) {
    const dateFromObj = new Date(dateFrom);
    const dateToObj = new Date(dateTo);
    
    if (dateFromObj.getTime() <= dateToObj.getTime()) 
    {
        return true; // dateFrom is earlier than dateTo
    } else {
        return false; // dateFrom is not earlier than dateTo
    }
}

addEventListener('load', init);
