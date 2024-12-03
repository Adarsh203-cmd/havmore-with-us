function handleResponse(response) {
    if (response.error) {
      var dialog = document.createElement('dialog');
      dialog.textContent = response.error;
  
      var closeButton = document.createElement('button');
      closeButton.textContent = 'Close';
      closeButton.addEventListener('click', function() {
        dialog.close();
      });
  
      dialog.appendChild(closeButton);
      document.body.appendChild(dialog);
      dialog.showModal();
    } 
  }