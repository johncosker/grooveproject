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
        alert (cmd['cmd'])
        //processCommand(cmd, this)
    })
    
    //Seach cmds
    //search
    $('#searchBox').on('click', function() {
        enableDisableButton( $(this ) )
        $.ajax({
            type: 'POST',
            url: 'apps/py/client_search.py',
            data: {'cmd'   : 'search',
                   'user'  : 'admin',
                   'target': 'search',
                   'info'  : $('#searchText').val()},
            success: function(data) {
                htmlStr = "<table style='width:800px'><tr><th></th><th>Song</th><th>Artist</th><th>Album</th></tr>"
                for (var i = 0; i < data.length; i++) {
                    htmlStr += "<tr stream= " + data[i]['stream'] +" >" +
                               "<th><input type='checkbox' name='songAdd'></th>" +
                               "<th class='song'>" + data[i]['song']   + "</th>" +
                               "<th class='artist'>" + data[i]['artist'] + "</th>" +
                               "<th class='album'>" + data[i]['album']  + "</th></tr>"
                }
                htmlStr += "</table>"
                $('#searchContent').html(htmlStr)
            },
            complete: function() {
                enableDisableButton( $('#searchBox') )

            },
            error: function() {
                alert(':(')
            }
        })
    })
    //Add selected song
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

function processCommand(cmd, buttonId) {
    enableDisableButton( $(buttonId) )
   $.ajax({
            type: 'POST',
            url: 'apps/py/wv_sendCommand.py',
            data: cmd,
            success: function(data) {
                
            },
            complete: function() {
                enableDisableButton( $(buttonId) )
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