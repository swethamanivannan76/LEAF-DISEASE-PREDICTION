$('#upload-form').submit(function(event) {
    event.preventDefault();
    var formData = new FormData(this);
    $.ajax({
      url: '/predict',
      type: 'POST',
      data: formData,
      processData: false,
      contentType: false,
      success: function(response) {
        $('#result').text('Predicted disease: ' + response.disease);
      },
      error: function(xhr, status, error) {
        $('#result').text('Error: ' + error);
      }
    });
  });
  