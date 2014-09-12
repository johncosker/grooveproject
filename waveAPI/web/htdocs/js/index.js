$(document).ready(function() {
    g_playTable = $('#playListTable').dataTable({
		"bFilter":       false,
		"bPaginate": false,
		"bInfo":         false,
		"oLanguage": {"sEmptyTable": "No songs in the play list."}
		})

    g_searchTable = $('#searchResultsTable').dataTable({
		"bFilter":        false,
		"bPaginate":  false,
		"bInfo":          false,
		"oLanguage": {"sEmptyTable": "No search results."}
	})
/*
    // Set up event streamer listener
    var eventStreamer = new EventSource('apps/py/webUpdate.py')
    eventStreamer.addEventListener(function() {
        alert(':)')
        // http://www.html5rocks.com/en/tutorials/eventsource/basics/
    })
    */

    // PLAY
    $('#play').on('click', function() {
        cmd = {'cmd'   : 'play',
					 'user'   : 'admin',
					 'target' : 'player',
					 'info'    : ''}
        processCommand(cmd, this)
    })

    //PLAY Popular
    $('#playPopular').on('click', function() {
        cmd = {'cmd'   : 'popular',
					 'user'   : 'admin',
					 'target' : 'player',
					 'info'     : ''}
        processCommand(cmd, this)
    })

    // PAUSE
    $('#pause').on('click', function() {
        cmd = {'cmd'   : 'pause',
					 'user'   : 'admin',
					 'target' : 'player',
					 'info'    : ''}
        processCommand(cmd, this)
    })

    // SKIP
    $('#skip').on('click', function() {
        cmd = {'cmd'   : 'skip',
					 'user'  : 'admin',
					 'target': 'player',
					 'info'  : ''}
        processCommand(cmd, this)
    })

    // Standard user cmds
    // UP VOTE
    $('#upSong').on('click', function() {
        cmd = {'cmd'   : 'upSong',
					 'user'   : 'admin',
					 'target' : 'player',
					 'info'    : ''}
        processCommand(cmd, this)
    })

    // DOWN VOTE
    $('#downSong').on('click', function() {
        cmd = {'cmd'    : 'downSong',
					'user'   : 'admin',
					'target' : 'player',
					'info'    : ''}
        alert (cmd['cmd'])
        //processCommand(cmd, this)
    })

    // Seach cmds
    // Search
    $('#searchButton').on('click', function() {
        $.ajax({
            type: 'POST',
            url: 'apps/py/client_search.py',
            data: {'cmd'   : 'search',
					  'user'   : 'admin',
					  'target' : 'search',
					  'info'    : $('#searchInput').val()},
            success: function(data) {
				updateSearchResults(data)
            },
            error: function() {
                //updateSearchResults(TODO :: ERROR ROW)
            }
        })
    })

    // Add selected song
    $('#AddSelectedSong').on('click', function() {
        $('input:checkbox[name=songAdd]:checked').each(function () {
            row = $(this).closest('tr')
            cmd = {'cmd'   : 'addSong',
                   'user'  : 'admin',
                   'target': 'dataBase',
                   'info'  : '',
                   'song':   $(row).find('.song').text(),
                   'album':  $(row).find('.album').text(),
                   'artist': $(row).find('.artist').text(),
                   'stream': $(row).attr('stream')
                  }
            processCommand(cmd, this)
        });
    })
})

//  *********************  FUNCTIONS  *********************  //

function processCommand(cmd, buttonId) {
   $.ajax({
            type: 'POST',
            url: 'apps/py/wv_sendCommand.py',
            data: cmd,
            success: function(data) {
                
            },
            error: function() {
                alert(':(')
            }
        })
}

function enableDisableButton(button) {
    if ($(button).attr("disabled") == 'disabled') {
        $(button).attr("disabled", false)

    }
    else {
        $(button).attr("disabled", true)
    }
}

function updatePlayList(entries) {
	var EL = entries.length()
	for (var x =0; x < EL; x++) {
		g_searchTable.fnAddData(["N/A",
											      entries[x].song,
												  entries[x].artist,
												  entries[x].album,
												])
	}
}

function updateSearchResults(entries) {
	// TODO :: SHOW LAST SEARCH RETUSTS
}