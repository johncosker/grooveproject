$(document).ready(function() {
    //Admin Cmds
    //PLAY
    $('#play').on('click', function() {
        cmd = {'cmd': 'play',
               'user': 'admin',
               'target': 'player',
               'info': ''}
        processCommand(cmd, this)
    })

    //PLAY Popular
    $('#popular').on('click', function() {
        cmd = {'cmd': 'play',
               'user': 'admin',
               'target': 'player',
               'info': ''}
        processCommand(cmd, this)
    })

    //PAUSE
    $('#pause').on('click', function() {
        cmd = {'cmd': 'pause',
               'user': 'admin',
               'target': 'player',
               'info': ''}
        processCommand(cmd, this)
    })

    //SKIP
    $('#skip').on('click', function() {
        cmd = {'cmd': 'skip',
               'user': 'admin',
               'target': 'player',
               'info': ''}
        processCommand(cmd, this)
    })
    //Standard user cmds
    //UP VOTE
    $('#upSong').on('click', function() {
        cmd = {'cmd': 'upSong',
               'user': 'admin',
               'target': 'player',
               'info': ''}
        processCommand(cmd, this)
    })
    
    //DOWN VOTE
    $('#downSong').on('click', function() {
        cmd = {'cmd': 'downSong',
               'user': 'admin',
               'target': 'player',
               'info': ''}
        processCommand(cmd, this)
    })
    
    //Seach cmds
    //search
    $('#searchBox').on('click', function() {
        alert('hi')
    })

    $('#cmdBtn').on('click', function() {
        cmd = {'cmd': $('#cmdBox').val(),
               'user': 'admin',
               'target': 'player',
               'info' : ''}  
        processCommand(cmd, this)
    })
})

function processCommand(cmd, buttonId) {
   $.ajax({
            type: 'POST',
            url: 'apps/py/wv_sendCommand.py',
            data: cmd,
            success: function(data) {
                $(buttonId).text(data)
            }
        })
}
