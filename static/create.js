
var save_venue = function(new_venue){
    var data_to_save = new_venue
    $.ajax({
        type: "POST",
        url: "/save_venue",
        dataType : "json",
        contentType: "application/json; charset=utf-8",
        data : JSON.stringify(data_to_save),

        success: function(result){
            var id = result["id"]
            var new_venues = result["venues"]
            var msg = "New item successfully created."
        		var new_div = $("<div>");

            let url= "'" + window.location.search +"./view/"+ id + "'";
            new_div.append("New item successfully created. " + "<a href=" + url+ ">" + "See it here." + "</a>");
            $("#create").append(new_div);
            $("#searchbox").autocomplete({
                source: new_venues
            });
        },
        error: function(request, status, error){
            console.log("Error");
            console.log(request)
            console.log(status)
            console.log(error)
        }
    });
}

function nameerror(){
  var msg = "The name must be entered."
  var errspan = $("<span class='error'>");
  errspan.html(msg);
  $("#nameError").append(errspan);
}
function imageerror(){
  var msg = "The link for an image must be entered."
  var errspan = $("<span class='error'>");
  errspan.html(msg);
  $("#imageError").append(errspan);
}
function descriptionerror(){
  var msg = "The description must be entered."
  var errspan = $("<span class='error'>");
  errspan.html(msg);
  $("#descriptionError").append(errspan);
}
function ratingerror(){
  var msg = "The rating must be entered."
  var errspan = $("<span class='error'>");
  errspan.html(msg);
  $("#ratingError").append(errspan);
}
function numericerror(){
  var msg = "The rating must be a number between 0 and 5."
  var errspan = $("<span class='error'>");
  errspan.html(msg);
  $("#ratingError").append(errspan);
}

	$(document).ready(function(){
    $("#create").empty();
		$("#create-venue").click(function(){
      $("#create").empty();
      $("#nameError").empty();
      $("#imageError").empty();
      $("#descriptionError").empty();
      $("#ratingError").empty();
      $("#numericError").empty();

      var currentName = $("#name").val();
      var currentImage = $("#image").val();
      var currentDescription = $("#description").val();
      var currentRating = $("#rating").val();

      if(currentName=="" || $.trim(currentName)==""){
        $("#nameError").addClass("error");
        nameerror();
      }else{
        $("#nameError").removeClass("error");
      }
      if(currentImage=="" || $.trim(currentImage)==""){
        $("#imageError").addClass("error");
        imageerror();
      }else{
        $("#imageError").removeClass("error");
      }
      if(currentDescription=="" || $.trim(currentDescription)==""){
        $("#descriptionError").addClass("error");
        descriptionerror();
      }else{
        $("#descriptionError").removeClass("error");
      }
      if(currentRating=="" || $.trim(currentRating)==""){
        $("#ratingError").addClass("error");
        ratingerror();
      }else if(!$.isNumeric(currentRating)||currentRating>5||currentRating<0){
        $("#ratingError").addClass("numericError");
        numericerror();
      }else{
        $("#ratingError").removeClass("error");
        $("#ratingError").removeClass("numericError");
      }
      if(!$("#nameError").hasClass("error")&& !$("#imageError").hasClass("error")&&
        !$("#descriptionError").hasClass("error")&& !$("#ratingError").hasClass("error")&&
        !$("#ratingError").hasClass("numericError")){
        var new_venue ={
          "name" : currentName,
          "image" : currentImage,
          "description" : currentDescription,
          "rating" : currentRating
        }
  			save_venue(new_venue);
        $("#name").val("");
        $("#image").val("");
        $("#description").val("");
        $("#rating").val("");
        $("#name").focus();
			}

		});

	});
