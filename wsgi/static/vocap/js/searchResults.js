define([
	'jquery',
	'underscore',
	'text!results_template',
	'jqueryui',
], function($, _, results_template){
	
	var searchResults = function( elem ){
		this.el = $( elem );
		this.template = results_template;
		this.bindPlayClick();
		return this;
	};

	searchResults.prototype.setResults = function( results ) {
		this.el.html(_.template(this.template, results));
		this.el.find('#accordion > div').accordion({ header: 'h3', collapsible: true,  heightStyle: "content" });
	};

	searchResults.prototype.pending = function() {
	      this.el.html( '<div class="loading">Loading... &nbsp;<img src="static/css/images/loading2.gif"></div>' );
	};

	searchResults.prototype.playClick = function(event) {
        time = $(event.target).data("time");
        vid = $(event.target).data("vid");
        var args = {time: time, vid: vid};
		$(this.el).trigger('play', args);
		return false;
	};

	searchResults.prototype.bindPlayClick = function() {
		this.el.on( 'click', '.play', _.bind( this.playClick, this ));
	};

	return searchResults;

});
