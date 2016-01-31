define([
	'jquery',
	'underscore',
	'rsvp',
	'ytplayer',
	'searchForm',
	'searchResults',
	'dictionaryPanel',
], function( $, _, RSVP, ytplayer, searchForm, searchResults, dictionaryPanel) {

	ytplayer.initializePlayer('player');
	pending=false;

	var dp = new dictionaryPanel("#dict");

	var sf = new searchForm("#search_form");
	// Perform the search on 'search' event
	sf.el.on('search', function(evt, query){ 
		if (pending) return;
		dp.setQuery(query);
		pending = true;

		sr.pending();
		$.get("/search/", {search: query}, function(data){
			sr.setResults( data );
			pending = false;
		});
	});

	var sr = new searchResults("#result");
	// Play a video on the 'play' event
	sr.el.on('play', function(evt, args){
		time = args.time;
		vid = args.vid;
		ytplayer.player.loadVideoById(vid, time);
	});

	// Preload loading image
	loader = new Image();
	loader.src = "static/css/images/loading2.gif";

});

