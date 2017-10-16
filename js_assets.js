function index_change_reaction(){
	// Do whatever you'd like here
	console.log("My favorite color is", BOKEH_GLOBALS.aux.favorite_color);
}

function initialize_BOKEH_GLOBALS(source, JSON_aux){
	if(typeof BOKEH_GLOBALS != "undefined"){return;} // Already exists, don't rerun the initialization
	if(window.location.port == ""){alert("It appears you're viewing this document from your filesystem. You should open this page from a server, eg localhost, so that the windows can communicate properly.\nYou can start a server with the command 'python3 -m http.server 8000'");} 
	BOKEH_GLOBALS = Object();

	// ColumnDataSource
	BOKEH_GLOBALS.source = source;

	// Auxiliary variables
	BOKEH_GLOBALS.aux = JSON.parse(JSON_aux);

	// where you should store functions referenced by Bokeh
	BOKEH_GLOBALS.fns = Object();
	// Don't change these
	BOKEH_GLOBALS.fns.send_index_signal = function(){window.localStorage.bokeh_indices = JSON.stringify(BOKEH_GLOBALS.source.attributes.selected['1d'].indices.sort());}
	BOKEH_GLOBALS.fns.selection_reaction = function(){BOKEH_GLOBALS.fns.send_index_signal();BOKEH_GLOBALS.fns.index_change_reaction();}
	// This function is required, but can be customized. (it can be left as an empty function, eg function(){})
	BOKEH_GLOBALS.fns.index_change_reaction = index_change_reaction;
	// You can make more of your own functions.  If your function changes the selected indices, it should end with calling BOKEH_GLOBALS.fns.selection_reaction

	// Callback that reacts to index change
	window.addEventListener('storage', function(e){  
	  	if(e.key != 'bokeh_indices'){return;}
	  	BOKEH_GLOBALS.source.attributes.selected['1d'].indices = JSON.parse(window.localStorage.bokeh_indices);
		BOKEH_GLOBALS.source.change.emit();
		BOKEH_GLOBALS.fns.index_change_reaction();
	});
}
