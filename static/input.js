  $(document).ready(function () {
      // Attach click event handler to all list containers (i.e., ul elements)
      $("ul.multi-select").on("click", "li input[type='checkbox'], li label, .selectAll", function () {
          var list = $(this).closest("ul"); // Get the list container
          var checkboxes = list.find("li input[type='checkbox']").not(".selectAll");
          var selected = checkboxes.filter(":checked").map(function () {
              return $(this).val();
          }).get();
          list.find(".selectAll").prop("checked", checkboxes.length == selected.length);
          console.log("Selected options in " + list.data("list-name") + ":", selected);
          event.stopPropagation();
      });

      // Attach click event handler to "Select All" checkboxes
      $("ul.multi-select .selectAll").click(function () {
          var list = $(this).closest("ul"); // Get the list container
          var checkboxes = list.find("li input[type='checkbox']").not(".selectAll");
          checkboxes.prop("checked", this.checked);
      });
  });


$(document).ready(function(){
  $(".collapsible-header").click(function(){
    var collapsible = $(this).closest(".collapsible");
    collapsible.toggleClass("active");
    var content = collapsible.find(".content");
    if (collapsible.hasClass("active")) {
      content.css("max-height", content.prop("scrollHeight") + "px");
    } else {
      content.css("max-height", "0px");
    }
  });
});



