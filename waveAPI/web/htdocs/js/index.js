$(document).ready(function() {
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
    pageLoadFunctions()

    // playListTab
    $('#playListTab').on('click', function() {
        g_playTable.fnClearTable()
        getPlaylistQ()
    })

    $('#play').on('click', function() {
        var cmd = {'cmd':    'play',
                   'user':   getUser(),
                   'target': 'player',
                   'info':   ''}
        processCommand(cmd, this, foo)
    })

    // PLAY Popular
    $('#playPopular').on('click', function() {
        var cmd = {'cmd':    'popular',
                   'user':   getUser(),
                   'target': 'player',
                   'info':   ''}
        processCommand(cmd, this, foo)
    })

    // PAUSE
    $('#pause').on('click', function() {
        var cmd = {'cmd':    'pause',
                   'user':   getUser(),
                   'target': 'player',
                   'info':   ''}
        processCommand(cmd, this, foo)
    })

    // SKIP
    $('#skip').on('click', function() {
        var cmd = {'cmd':    'skip',
                   'user':   getUser(),
                   'target': 'player',
                   'info':   ''}
        processCommand(cmd, this, foo)
    })

    // Standard user cmds
    // UP VOTE
    $('.upvote').on('click', function() {
        var cmd = {'cmd':    'upSong',
                   'user':   getUser(),
                   'target': 'player',
                   'info':   ''}
        processCommand(cmd, this, foo)
    })

    // DOWN VOTE
    $('.downvote').on('click', function() {
        var cmd = {'cmd':    'downSong',
                   'user':   getUser(),
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
                   'user':   getUser(),
                   'target': 'search',
                   'info':   $('#searchInput').val()}
        var searchConn = new WebSocket(g_wsproto)
        searchConn.onmessage = function (e) {updateSearchResults(e.data)}
        searchConn.onopen = function(){searchConn.send(JSON.stringify(cmd))}
    })

    // Add selected song
    $('.addSong').on('click', function() {
        var row = $(this).closest('tr')
        var cmd = {'cmd':    'addSong',
                   'user':   getUser(),
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
    if (window.location.protocol === "https:") {
        g_wsproto = "wss://localhost:5506/"
    } else {
        g_wsproto = "ws://localhost:5506/"
    }
    login()
    getPlaylistQ()
}

function login() {
    $('#loginDialog').modal('show')
}


function foo() {}

function startWebSockets() {
    connection = new WebSocket(g_wsproto)
    // When the connection is open, send some data to the server
    connection.onopen = function () {
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
    var conn = new WebSocket(g_wsproto)
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

g_user = 'derek'
g_pass = '1'
g_uid = 'cea251a4-ee22-354c-b419-0bd1f9a3794e'
function getUser() {
    return btoa(g_user + ':' + g_pass + ':' + g_uid)
}

//Get playlist queue
function getPlaylistQ() {
    processCommand({'cmd':    'showdb',
                    'user':   getUser(),
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
        g_playTable.fnAddData([
          '<div class="searchDiv posision">' + songs[x].rowid + '</div>',
          '<div class="searchDiv song">' + songs[x].name + '</div>',
          '<div class="searchDiv artist">' + songs[x].artist + '</div>',
          '<div class="searchDiv album">' + songs[x].votes +
            '<span class="glyphicon glyphicon glyphicon-hand-down upvote" aria-hidden="true"></span>' +
            '<span class="glyphicon glyphicon glyphicon-hand-up downvote" aria-hidden="true"></span>' +
         '</div>'])
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
        g_searchTable.fnAddData([
          '<buttontype="button" class="addSong btn btn-default" onClick="addSong(this)"' +
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
               'user':     getUser(),
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
    $('.li_searchBox').width($('#mainNavContainer').width() - 225)

    var newHeight = $('body').height() + 50
    $('#mainContainer').height(newHeight)
    $('#searchResults').height(newHeight)
    $('#settings').height(newHeight)
    $('.dataTables_scrollBody').height(newHeight)
}
