$(document).ready(function() {
    pageLoadFunctions()

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
        processCommand(cmd, this, foo)
    })

    // PLAY Popular
    $('#playPopular').on('click', function() {
        var cmd = {'cmd':    'popular',
                   'user':   'admin',
                   'target': 'player',
                   'info':   ''}
        processCommand(cmd, this, foo)
    })

    // PAUSE
    $('#pause').on('click', function() {
        var cmd = {'cmd':    'pause',
                   'user':   'admin',
                   'target': 'player',
                   'info':   ''}
        processCommand(cmd, this, foo)
    })

    // SKIP
    $('#skip').on('click', function() {
        var cmd = {'cmd':    'skip',
                   'user':   'admin',
                   'target': 'player',
                   'info':   ''}
        processCommand(cmd, this, foo)
    })

    // Standard user cmds
    // UP VOTE
    $('#upSong').on('click', function() {
        var cmd = {'cmd':    'upSong',
                   'user':   'admin',
                   'target': 'player',
                   'info':   ''}
        processCommand(cmd, this, foo)
    })

    // DOWN VOTE
    $('#downSong').on('click', function() {
        var cmd = {'cmd':    'downSong',
                   'user':   'admin',
                   'target': 'player',
                   'info':   ''}
        processCommand(cmd, this, foo)
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
        console.log(cmd)
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
        processCommand(cmd, this, foo)
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
function pageLoadFunctions() {
    responsiveFormatting()
    getPlaylistQ()
}


function foo() {}

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
    }

    // Log messages from the server
    connection.onmessage = function (e) {
        console.log('Server: ' + e.data)
    }
}

function processCommand(cmd, buttonId, callback) {
    var conn = new WebSocket('ws://localhost:5506/')
    conn.onopen = function () {
        console.log(cmd)
        conn.send(JSON.stringify(cmd))
    }
    conn.onerror = function (error) {
        console.log('conn error ' + error)
    }
    conn.onmessage = function (e) {
        console.log('Server: ' + e.data)
        callback(JSON.parse(e.data))
    }
    
}

//Get playlist queue
function getPlaylistQ() {
    processCommand({'cmd':    'showdb',
                    'user':   'admin',
                    'target': 'dataBase',
                    'info':   ''},
                   $(this).closest('tr'),
                   populatePlaylist)     
}

function populatePlaylist(songs) {
    songs = songs.songs
    g_playTable.fnClearTable()
    var EL = songs.length
    for (var x = 0; x < EL; x++) {
        g_playTable.fnAddData(['<div class="searchDiv song">' + songs[x].name + '</div>',
                               '<div class="searchDiv artist">' + songs[x].artist + '</div>',
                               '',
                               '<div class="searchDiv album">' + songs[x].votes + '</div>'])
    }
     setTimeout(function() {getPlaylistQ()}, 30000)
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
    console.log(entries)
    var EL = entries.length
    for (var x = 0; x < EL; x++) {
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
    processCommand(cmd, this, foo)
}

function responsiveFormatting() {
    var width = $('#mainNavContainer').width()
    $('.li_searchBox').width(width - 225)
}
