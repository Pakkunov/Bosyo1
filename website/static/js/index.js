
document.addEventListener('click', function(event) {
    if (event.target.closest('.modal') === null) {
      var modals = document.querySelectorAll('.modal.show');
      modals.forEach(function(modal) {
        bootstrap.Modal.getInstance(modal).hide();
      });
    }
  });
  
  document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
      var modals = document.querySelectorAll('.modal.show');
      modals.forEach(function(modal) {
        bootstrap.Modal.getInstance(modal).hide();
      });
    }
  });
  