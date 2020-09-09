

var display_venue = function(venue){

  $("#edit").empty();
  $(".list").empty();
    //insert all data

  var newline = $("<div class='row newlist'>");
  var newImage = $("<div class='col-12'>");
  var newName = $("<div class='col-12 name'>");
  var newRating = $("<div class='col-12 rating'>")
  var newDescription = $("<div class='col-12 description'>")

  newName.append(venue["name"])
  newImage.append("<img src="+venue["image"]+" class=image>");
  newRating.append("rating: ").append(venue["rating"])
  newDescription.append(venue["description"])
  newline.append(newImage).append(newRating).append(newDescription);

  if(venue["reviews"].length == 0){
    var newReview = $("<div class='col-12 review'>");
    newReview.append("There is no review.");
  }
  else{
    $.each(venue["reviews"], function(index, datum){
      var newUser = $("<div class='col-12'>");
      var newReview = $("<div class='col-12 review'>");
      newUser.append("user: ").append(datum["user"]);
      newReview.append("review: ").append(datum["review"]);
      newline.append(newUser).append(newReview);
    });
  }

  $("#edit").append(newName);
  $(".list").append(newline);

}

var update_venue = function(id, new_user, new_review){
    var data_to_save = {
      "id" : id,
      "user" : new_user,
      "review": new_review
    }
    $.ajax({
        type: "POST",
        url: "/update_venue",
        dataType : "json",
        contentType: "application/json; charset=utf-8",
        data : JSON.stringify(data_to_save),

        success: function(result){
            var id = result["id"]
            document.location.href="../view/" + id;
        },
        error: function(request, status, error){
            console.log("Error");
            console.log(request)
            console.log(status)
            console.log(error)
        }
    });
}

function usererror(){
  var msg = "The user name must be entered."
  var errspan = $("<span class='error'>");
  errspan.html(msg);
  $("#userError").append(errspan);
}

function reviewerror(){
  var msg = "The review must be entered."
  var errspan = $("<span class='error'>");
  errspan.html(msg);
  $("#reviewError").append(errspan);
}

	$(document).ready(function(){
    $("#userError").empty();
    $("#reviewError").empty();

    display_venue(venue);

    $("#discardbutton").click(function(){
      document.location.href="../view/" + id;
    });

    $("#add-review").click(function(){
      $("#userError").empty();
      $("#reviewError").empty();

      var currentUser = $("#username").val();
      var currentReview = $("#review").val();

      if(currentUser=="" || $.trim(currentUser)==""){
        $("#userError").addClass("error");
        usererror();
      }else{
        $("#userError").removeClass("error");
      }

      if(currentReview=="" || $.trim(currentReview)==""){
        $("#reviewError").addClass("error");
        reviewerror();
      }else{
        $("#reviewError").removeClass("error");
      }
      if(!$("#userError").hasClass("error")&& !$("#reviewError").hasClass("error")){
        update_venue(id, currentUser, currentReview);
			}
    });

	});
