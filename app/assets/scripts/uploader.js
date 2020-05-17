$("#submit").click(function() {
  var $this = $(this);

  $this.html('<span class="spinner-border spinner-border-sm"></span>');

  setTimeout(() => {
    $this.html("Submit");
  }, 10000);
});
