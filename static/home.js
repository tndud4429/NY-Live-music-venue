
var display_last10 = function(new_venues){
    //empty old data
    $("#home_list").empty();
    $("#home").empty();
    $("#search-err").empty();
    var summary = $("<div id='summary' class='row'>");
    summary.append("NY Live Music Venue is to help the users who are looking for a place to listen to live music in NYC and to introduce new venues for live music.");
    $("#home").append(summary);

    var length = new_venues.length;

    for (var i=0; i<10; i++){
      var id = new_venues[length-1]["id"]
      var newline = $("<div id=" + id + " class='row newlist'>");
      var newImage = $("<div class='col-4 img'>");
      var newName = $("<div class='col-2 name'>");
      var newDescription = $("<div class='col-6 description'>");

      let url= "'" + window.location.search +"../view/"+id + "'"
      newImage.append("<a href=" + url+ ">" + "<img class='fit-picture img-fluid image' src= "+ new_venues[length-1]["image"]+" alt='live music venue photo displayed at home page'>" + "</a>");
      newName.append("<a href=" + url +" class='name'>" + new_venues[length-1]["name"] + "</a>");
      newDescription.append(new_venues[length-1]["description"]);
      newline.append(newName).append(newImage).append(newDescription);
      length = length-1;
      $("#home_list").append(newline);
    }

    $("#searchbox").val("");
    $("#searchbox").focus();

}

var search_venue = function(venue_name){
    document.location.href="../search/" + venue_name
}

function searcherror(){
	var msg = "A name of venue must be entered."
	var errspan = $("<span class='error'>");
	errspan.html(msg);
	$("#search-err").append(errspan);
}


	$(document).ready(function(){
    $("#home_list").empty();
    $("#home").empty();
    $("#search-err").empty();

		$("#searchbox").autocomplete({
			   source: venues
		});

    display_last10(venues);

		$('#searchbox').keypress(function(event){
      $("#search-err").empty();
      var keycode = (event.keyCode ? event.keyCode : event.which);
      var currentName = $("#searchbox").val();
			if(keycode == '13' && currentName!="" && $.trim(currentName)!=""){
				search_venue(currentName);
			}else if(keycode == '13' && (currentName==""||$.trim(currentName)=="")){
				searcherror();
      }
      $("#searchbox").focus();
		});

		$("#submit").click(function(){
      var currentName = $("#searchbox").val();
			if(currentName!="" && $.trim(currentName)!=""){
				search_venue(currentName);
			}else if(currentName==""||$.trim(currentName)==""){
        searcherror();
			}
      $("#searchbox").focus();
		});

	});
