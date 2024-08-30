

  // allows the submission of Clear Results button when the input field is empty
  $(document).ready(function() {
    $('#clearResultsBtn').click(function() {
        // Remove required attribute from input field
        $('#clubForm input[name="player_name"]').prop('required', false);
    });
  });