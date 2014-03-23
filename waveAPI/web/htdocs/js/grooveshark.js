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

/*

function processNextSnapshot( image ) {
    if (image.length != 1){
        do {
            image.shift(0,1);
        }
        while ( $(image[0]).attr('src') != '/static_media/img/branding/snapshot_19px.png' );
        if ( image.length > 1 ){
            setTimeout( function () {snapshotOver(image)}, 500 );
        }
    }
}

$.ajax({
        url: url,
        type: 'POST',
        async: true,
        cache: false,
        data: {},
        success: function(data){},
        error: function(){},
        complete: function(){}
    });

*/