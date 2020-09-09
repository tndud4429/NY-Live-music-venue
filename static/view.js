

var display_venue = function(venue){
    //insert all data

  var newImage = $("<div class='col-12'>");
  var newName = $("<div class='col-12 view-name'>");
  var newRating = $("<div class='col-12 rating'>");
  var newDescription = $("<div class='col-12 description'>");
  var addReview = $("<button class='add_review button margin'>Add Review</button>");

  newName.append(venue["name"])
  newImage.append("<img src="+venue["image"]+" class='view-image' alt='live music venue photo displayed at view page'>");
  newRating.append("rating: ").append(venue["rating"]+" ").append("<button class='edit_rating button'>Edit</button>")
  newDescription.append(venue["description"])

  if(venue["reviews"].length == 0){
    var newReview = $("<div class='col-12 review'>");
    newReview.append("There is no review.");
  }
  else{
    $.each(venue["reviews"], function(index, datum){
        if(datum["mark_as_deleted"] == false){
            var review_id = datum["id"]
            var review = $("<div class='row'>");
            var block = $("<div class='col-12 inline'>");
            var newUser = $("<div>");
            var newReview = $("<div class='review'>");
            var cancelbutton = $("<div class='col-1 inline'>");
            var newcancelButton = $("<button id=" + review_id + " class='cancelButton'>");

            cancelbutton.append(newcancelButton);
            newcancelButton.text("X");
            newUser.append("user: ").append(datum["user"]).append(cancelbutton);
            newReview.append("review: ").append(datum["review"]);
            block.append(newUser).append(newReview);
            review.append(cancelbutton).append(block);

            $("#view-reviews").append(review);
        }else{
            var review_id = datum["id"]
            var undobutton = $("<div class='row'>");
            var newundoButton = $("<button id=" + review_id + " class='submitButton undo'>");
            newundoButton.append("Undo")
            undobutton.append(newundoButton);

            $("#view-reviews").append(undobutton);
        }

    });
  }

  $("#view").append(newName);
  $("#view-image").append(newImage);
  $("#view-rating").append(newRating);
  $("#view-description").append(newDescription);
  $("#add-review").append(addReview);
}

var edit_rating = function(venue){
    $("#view-rating").empty();
    var newInput = $("<input class='ratingbox' placeholder='Enter new rating.'>").append("<div id='ratingError'>");
    var newdiscard = $("<button class='discard_rating cancelButton'>Discard</button>");
    var newsubmit = $("<button class='submit_rating submitButton'>Submit</button>")
    var newRow = $("<div class='row upperrating'>")
    var newButtons = $("<div class='row lowerrating'>")

    newRow.append(newInput)
    newButtons.append(newsubmit).append(newdiscard);
    $("#view-rating").append(newRow).append(newButtons);
    $(".ratingbox").focus();
    $(".ratingbox").val(venue["rating"]);
}

var rating_discard = function(venue){
    $("#view-rating").empty();
    var newRating = $("<div class='col-12 rating'>");
    newRating.append("rating: ").append(venue["rating"]+" ").append("<button class='edit_rating button'>Edit</button>")
    $("#view-rating").append(newRating);
}

var rating_submit = function(venue){
    var newValue = $(".ratingbox").val();
    $("#view-rating").empty();

    var data_to_update = {
                            "id": id,
                            "rating": newValue
                          }

    $.ajax({
        type: "POST",
        url: "/update_rating",
        dataType : "json",
        contentType: "application/json; charset=utf-8",
        data : JSON.stringify(data_to_update),
        success: function(result){
              $("#view").empty();
              $("#view-image").empty();
              $("#view-rating").empty();
              $("#view-description").empty();
              $("#view-reviews").empty();
              $("#add-review").empty();
              display_venue(result["venue"]);
        },
        error: function(request, status, error){
            console.log("Error");
            console.log(request)
            console.log(status)
            console.log(error)
        }
    });

}

var enter_review = function(){
    $("#add-review").empty();
    var newUser = $("<div class='col-12'>");
    var newReview = $("<div class='col-12 margin'>");
    var newdiscard = $("<button class='discard_review cancelButton margin'>Discard</button>");
    var newsubmit = $("<button class='submit_review submitButton margin'>Submit</button>")
    var newRow = $("<div class='row'>")

    newUser.append("<input class='newuser margin inputbox' placeholder='Enter a user name'>").append("<div id='nameError'>");
    newReview.append("<input class='newreview margin inputbox' placeholder='Enter a review'>").append("<div id='reviewError'>");

    newRow.append(newUser).append(newReview).append(newsubmit).append(newdiscard);
    $("#add-review").append(newRow);
    $(".newuser").focus();
}

var review_discard = function(){
    $("#add-review").empty();
    var addReview = $("<button class='add_review button margin'>Add Review</button>")
    $("#add-review").append(addReview);
}


var review_submit = function(){
    var newUser = $(".newuser").val();
    var newReview = $(".newreview").val();
    $("#add-review").empty();

    var data_to_update = {
                            "id": id,
                            "user": newUser,
                            "review": newReview
                          }
    $.ajax({
        type: "POST",
        url: "/update_review",
        dataType : "json",
        contentType: "application/json; charset=utf-8",
        data : JSON.stringify(data_to_update),
        success: function(result){
              $("#view").empty();
              $("#view-image").empty();
              $("#view-rating").empty();
              $("#view-description").empty();
              $("#view-reviews").empty();
              $("#add-review").empty();
              display_venue(result["venue"]);
        },
        error: function(request, status, error){
            console.log("Error");
            console.log(request)
            console.log(status)
            console.log(error)
        }
    });
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
function nameerror(){
  var msg = "The user name must be entered."
  var errspan = $("<span class='error'>");
  errspan.html(msg);
  $("#nameError").append(errspan);
}
function reviewerror(){
  var msg = "The review must be entered."
  var errspan = $("<span class='error'>");
  errspan.html(msg);
  $("#reviewError").append(errspan);
}

var delete_review = function(review_id){
  var data_to_delete = {
                          "id": id,
                          "review_id" : review_id
                        };

  $.ajax({
      type: "POST",
      url: "/delete_review",
      dataType : "json",
      contentType: "application/json; charset=utf-8",
      data : JSON.stringify(data_to_delete),
      success: function(result){
            $("#view").empty();
            $("#view-image").empty();
            $("#view-rating").empty();
            $("#view-description").empty();
            $("#view-reviews").empty();
            $("#add-review").empty();
            display_venue(result["venue"]);
      },
      error: function(request, status, error){
          console.log("Error");
          console.log(request)
          console.log(status)
          console.log(error)
      }
  });
}

var undo_review = function(review_id){
  var data_to_delete = {
                          "id": id,
                          "review_id" : review_id
                        };

  $.ajax({
      type: "POST",
      url: "/undo_review",
      dataType : "json",
      contentType: "application/json; charset=utf-8",
      data : JSON.stringify(data_to_delete),
      success: function(result){
            $("#view").empty();
            $("#view-image").empty();
            $("#view-rating").empty();
            $("#view-description").empty();
            $("#view-reviews").empty();
            $("#add-review").empty();
            display_venue(result["venue"]);
      },
      error: function(request, status, error){
          console.log("Error");
          console.log(request)
          console.log(status)
          console.log(error)
      }
  });
}

	$(document).ready(function(){
    $("#view").empty();
    $("#view-image").empty();
    $("#view-rating").empty();
    $("#view-description").empty();
    $("#view-reviews").empty();
    $("#add-review").empty();
    $("#nameError").empty();
    $("#reviewError").empty();
    $("#ratingError").empty();

    display_venue(venue);

    $("#view-rating").on('click', '.edit_rating', function(){
        edit_rating(venue);
    });
    $("#view-rating").on('click', '.discard_rating', function(){
        rating_discard(venue);
    });
    $("#view-rating").on('click', '.submit_rating', function(){
        $("#ratingError").empty();
        var newRating = $(".ratingbox").val();
        if(newRating=="" || $.trim(newRating)==""){
            $("#ratingError").addClass("error");
            ratingerror();
        }else if(!$.isNumeric(newRating)||newRating>5||newRating<0){
            $("#ratingError").addClass("Numericerror");
            numericerror();
        }else{
            $("#ratingError").removeClass("error");
            $("#ratingError").removeClass("Numericerror");
        }
        if(!$("#ratingError").hasClass("error")){
          rating_submit(venue);
        }
    });
    $("#add-review").on('click', '.add_review', function(){
        enter_review();
    });
    $("#add-review").on('click', '.discard_review', function(){
        review_discard();
    });
    $("#add-review").on('click', '.submit_review', function(){
        $("#nameError").empty();
        $("#reviewError").empty();
        var newUser = $(".newuser").val();
        var newReview = $(".newreview").val();
        if(newUser=="" || $.trim(newUser)==""){
          $("#nameError").addClass("error");
          nameerror();
        }else{
          $("#nameError").removeClass("error");
        }
        if(newReview=="" || $.trim(newReview)==""){
          $("#reviewError").addClass("error");
          reviewerror();
        }else{
          $("#reviewError").removeClass("error");
        }
        if(!$("#nameError").hasClass("error")&& !$("#reviewError").hasClass("error")){
          review_submit();
        }

    });

    $('#view-reviews').on('click', '.cancelButton', function(){
        var review_id = $(this).attr("id");
    		delete_review(review_id);
    });

    $('#view-reviews').on('click', '.undo', function(){
        var review_id = $(this).attr("id");
        undo_review(review_id);
    });

	});
