$(document).ready(function() {

    //Custom messages
    $('#ccSubmit').on('click', function() {
        cmd = {'cmd'   : $('#ccCmd').val(),
               'user'  : $('#ccUser').val(),
               'target': $('#ccTarget').val(),
               'info'  : $('#ccInfo').val()}
        processCommand(cmd, this)
    })

    //Open messages
        $('#acSubmit').on('click', function() {
        $.ajax({
            type: 'POST',
            url: 'apps/py/wv_sendCommand.py',
            data: $('#acSubmit').val(),
            success: function(data) {
                $(buttonId).text(data)
            },
            error: function() {
                alert(':(')
            }
        })
    })

    //Admin Cmds
    //PLAY
    $('#play').on('click', function() {
        cmd = {'cmd'   : 'play',
               'user'  : 'admin',
               'target': 'player',
               'info'  : ''}
        processCommand(cmd, this)
    })

    //PLAY Popular
    $('#playPopular').on('click', function() {
        cmd = {'cmd'   : 'popular',
               'user'  : 'admin',
               'target': 'player',
               'info'  : ''}
        processCommand(cmd, this)
    })

    //PAUSE
    $('#pause').on('click', function() {
        cmd = {'cmd'   : 'pause',
               'user'  : 'admin',
               'target': 'player',
               'info'  : ''}
        processCommand(cmd, this)
    })

    //SKIP
    $('#skip').on('click', function() {
        cmd = {'cmd'   : 'skip',
               'user'  : 'admin',
               'target': 'player',
               'info'  : ''}
        processCommand(cmd, this)
    })
    //Standard user cmds
    //UP VOTE
    $('#upSong').on('click', function() {
        cmd = {'cmd'   : 'upSong',
               'user'  : 'admin',
               'target': 'player',
               'info'  : ''}
        processCommand(cmd, this)
    })
    
    //DOWN VOTE
    $('#downSong').on('click', function() {
        cmd = {'cmd'   : 'downSong',
               'user'  : 'admin',
               'target': 'player',
               'info'  : ''}
        processCommand(cmd, this)
    })
    
    //Seach cmds
    //search
    $('#searchBox').on('click', function() {
        $.ajax({
            type: 'POST',
            url: 'apps/py/client_search.py',
            data: {'cmd'   : 'search',
                   'user'  : 'admin',
                   'target': 'search',
                   'info'  : 'Basshunter'},
            success: function(data) {
                for (var i = 0; i < data.length; i++) {
                    $('#serachResults').text( $('#serachResults').text() + data[i] )
                }
               
                alert(data)
            },
            error: function() {
                alert(':(')
            }
        })
    })
})

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