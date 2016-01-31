define(['jquery'], function($) {
	var ytplayer = {
		initialized: false,
		initializePlayer: function(frame_id) {
			if (typeof(YT) == 'undefined' || typeof(YT.Player) == 'undefined') {
				window.onYouTubeIframeAPIReady = function() {
					ytplayer.player = new YT.Player(frame_id, { });
					ytplayer.initialized = true;
					console.log('Player initialised!');
				};
				$.getScript( "//www.youtube.com/iframe_api", function( data, textStatus, jqxhr ) {
					console.log( "Loading YouTube API: " + jqxhr.status + ', ' + textStatus );
				});
			}
		},
	};
	return ytplayer;
});
