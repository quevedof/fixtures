// allows the submission of Clear Results button when the input field is empty
$(document).ready(function() {
  $('#clearResultsBtn').click(function() {
      // Remove required attribute from input field
      $('#clubForm input[name="player_name"]').prop('required', false);
  });
});

// Removes a fixtures table
function removeTable(table_no) {
  fetch('', {
      method: 'DELETE',
      headers: {
           'Content-Type':'application/json',
           'X-CSRFToken': getCookie('csrftoken'),
      },
      body:JSON.stringify({'table_no': table_no})
  })
  .then(res => {
      if (res.ok) {
          window.location.href = window.location.pathname;
      } else {
          console.error('Error deleting resource:', res.status);
      }
  })
  .catch(error => console.error('Error deleting resource:', error));
  }
  
  // returns csrf token
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
  }