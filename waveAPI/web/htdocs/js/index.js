$(document).ready(function() {
    responsiveFormatting()
    startWebSockets()
    g_playTable = $('#playListTable').dataTable({
        "bFilter":   false,
        "bPaginate": false,
        "bInfo":     false,
        "sScrollY":  "100px",
        "oLanguage": {"sEmptyTable": "No songs in the play list."},
        "aoColumns": [{ "bSortable": false },
                      { "bSortable": true },
                      { "bSortable": true },
                      { "bSortable": true }]
    })

    g_searchTable = $('#searchResultsTable').dataTable({
        "bFilter":   false,
        "bPaginate": false,
        "bInfo":     false,
        "sScrollY":  "100px",
        "oLanguage": {"sEmptyTable": "No songs in the play list."},
        "aoColumns": [{ "bSortable": false },
                      { "bSortable": true },
                      { "bSortable": true },
                      { "bSortable": true }]
    })

    // PLAY
    $('#play').on('click', function() {
        var cmd = {'cmd':    'play',
                   'user':   'admin',
                   'target': 'player',
                   'info':   ''}
        processCommand(cmd, this)
    })

    // PLAY Popular
    $('#playPopular').on('click', function() {
        var cmd = {'cmd'   : 'popular',
                   'user'   : 'admin',
                   'target' : 'player',
                   'info'     : ''}
        processCommand(cmd, this)
    })

    // PAUSE
    $('#pause').on('click', function() {
        var cmd = {'cmd':    'pause',
                   'user':   'admin',
                   'target': 'player',
                   'info':   ''}
        processCommand(cmd, this)
    })

    // SKIP
    $('#skip').on('click', function() {
        var cmd = {'cmd':    'skip',
                   'user':   'admin',
                   'target': 'player',
                   'info':   ''}
        processCommand(cmd, this)
    })

    // Standard user cmds
    // UP VOTE
    $('#upSong').on('click', function() {
        var cmd = {'cmd':    'upSong',
                   'user':   'admin',
                   'target': 'player',
                   'info':   ''}
        processCommand(cmd, this)
    })

    // DOWN VOTE
    $('#downSong').on('click', function() {
        var cmd = {'cmd':    'downSong',
                   'user':   'admin',
                   'target': 'player',
                   'info':   ''}
        alert (cmd['cmd'])
        //processCommand(cmd, this)
    })

    // Seach cmds
    // Search
    $('#searchButton').on('click', function() {
        $('#searchResultsTab').trigger('click')
        g_searchTable.fnClearTable()
        var cmd = {'cmd':    'search',
                   'user':   'admin',
                   'target': 'search',
                   'info':   $('#searchInput').val()}
        searchConn = new WebSocket('ws://localhost:5506/')
        searchConn.onmessage = function (e) {updateSearchResults(e.data)}
        searchConn.onopen = function(){searchConn.send(JSON.stringify(cmd))}
    })

    // Add selected song
    $('.addSong').on('click', function() {
        var row = $(this).closest('tr')
        var cmd = {'cmd':    'addSong',
                   'user':   'admin',
                   'target': 'dataBase',
                   'info':   '',
                   'song':   $(row).find('.song').text(),
                   'album':  $(row).find('.album').text(),
                   'artist': $(row).find('.artist').text()}
        processCommand(cmd, this)
    })

    $('#searchInput').keydown(function(event) {
        if (event.keyCode == 13) {
            $('#searchButton').trigger('click')
        }
    })

    $(window).on('resize', function() {
        responsiveFormatting()
    })
})

//  *********************  FUNCTIONS  *********************  //

function startWebSockets() {
    console.log('start')
    connection = new WebSocket('ws://localhost:5506/')
    console.log('started')
    // When the connection is open, send some data to the server
    connection.onopen = function () {
        console.log('connection.onopen')
        connection.send('INIT_CONN') // Send the message 'Ping' to the server
    }

    // Log errors
    connection.onerror = function (error) {
        console.log('conn error ' + error)
        //alert("Server error: Can not connect to server.")
    }

    // Log messages from the server
    connection.onmessage = function (e) {
        console.log('Server: ' + e.data)
    }
}

function processCommand(cmd, buttonId) {
    connection.send(JSON.stringify(cmd))
}

function enableDisableButton(button) {
    if ($(button).attr("disabled") == 'disabled') {
        $(button).attr("disabled", false)

    } else {
        $(button).attr("disabled", true)
    }
}

function updateSearchResults(entries) {
    entries = JSON.parse(entries).songs
derek = entries
    console.log(entries)
    console.log('derek')
    var EL = entries.length
    for (var x =0; x < EL; x++) {
        g_searchTable.fnAddData(['<buttontype="button" class="addSong btn btn-default" onClick="addSong(this)"' +
                                 'SongID='+ entries[x].SongID +' ArtistID='+ entries[x].ArtistID +'>Add</button>',
                                 '<div class="searchDiv song">' + entries[x].song + '</div>',
                                 '<div class="searchDiv artist">' + entries[x].artist + '</div>',
                                 '<div class="searchDiv album">' + entries[x].album + '</div>'])
    }
    searchConn.close()
}

function updatePlayList(entries) {
    // TODO :: SHOW LAST SEARCH RETUSTS
}

function addSong(button_row) {
    var row = $(button_row).closest('tr')
    var cmd = {'cmd':      'addSongBySourceType',
               'user':     'admin',
               'target':   'dataBase',
               'info':     '',
               'SongID':   $(button_row).attr('SongId'),
               'ArtistID': $(button_row).attr('ArtistId'),
               'song':     $(row).find('.song').text(),
               'album':    $(row).find('.album').text(),
               'artist':   $(row).find('.artist').text()}
    processCommand(cmd, this)
}

function responsiveFormatting() {
    var width = $('#mainNavContainer').width()
    $('.li_searchBox').width(width - 225)
}
