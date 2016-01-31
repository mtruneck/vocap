define([
	'jquery',
	'underscore'
], function($, _){

	var searchForm = function( form ){
		this.el = $(form);
		this.el.find('#submit_search').on('click', _.bind(this.handleSubmit, this));
		this.el.on('submit', _.bind(this.handleSubmit, this));
	};

	searchForm.prototype.handleSubmit = function(event) {
		event.preventDefault();
		var query = $.trim( this.el.find('[name="search_query"]').val() );
		if ( !query ) { return; }
		this.el.trigger( 'search', [ query ] );
	};

	return searchForm;
	
});
