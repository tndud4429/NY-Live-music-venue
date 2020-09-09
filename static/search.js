

var display_list = function(new_venues){
    //empty old data
    $("#searchresult").empty();
    $("#search_list").empty();
    $("#search-err").empty();
    var result = $("<div id='summary' class='row'>");
    result.append("There are " + new_venues.length + " results.");
    $("#searchresult").append(result);

    //insert all new data
    $.each(new_venues, function(index, datum){
      var id = new_venues[index]["id"]
      var newline = $("<div id=" + id + " class='row newlist'>");
      var newImage = $("<div class='col-4 img'>");
      var newName = $("<div class='col-2 name'>");
      var newDescription = $("<div class='col-6 description'>");

      let url= "'" + window.location.search +"../view/"+id + "'"
      newImage.append("<a href=" + url +">" + "<img class='fit-picture img-fluid image' src= "+ datum["image"]+" alt='live music venue photo displayed at search page'>")+ "</a>";
      newName.append("<a href=" + url +" class='name'>" + datum["name"] + "</a>");
      newDescription.append(datum["description"]);
      newline.append(newName).append(newImage).append(newDescription);

      $("#search_list").append(newline);
    })

    $("#searchbox").val("");
    $("#searchbox").focus();
}

	$(document).ready(function(){
    $("#search_list").empty();
    $("#searchresult").empty();
    $("#search-err").empty();

    display_list(search_result);

		$("#searchbox").autocomplete({
			source: venues
		});

	});
