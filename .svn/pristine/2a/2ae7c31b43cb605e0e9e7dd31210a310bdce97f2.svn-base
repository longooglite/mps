// [Copyright]
// SmartPath v1.0
// Copyright 2014-2015 Mountain Pass Solutions, Inc.
// This unpublished material is proprietary to Mountain Pass Solutions, Inc.
// [End Copyright]

(function ($) {

    //
    // Fake LeftNav 'Tabs' to form sub-section 'Panes'
    //
    $('.cv-menu').on('click', '.cv-pubmed-menuitem', function(e){
        var sel = '.' + $(this).data('cvTabSelector'),
            $pane = $(sel),
            $tabs = $('.cv-pubmed-menuitem'),
            $panes = $('.cv-pubmed-tab-content');

        $tabs.removeClass('active');
        $(this).addClass('active');

        if($pane.length){
            $panes.removeClass('active');
            $pane.addClass('active');
        }
        else{
            // alert('BUGBUG: UX error');
        }

        window.scrollTo(0, 0);

        e.stopPropagation(); // Stop normal POSTing from cv-menu
        e.preventDefault();
    });

    //
    // MINE/NOTMINE: btn-group -> radio buttons form-setting...
    //
    $('body').on('click', '.import-btn-group .btn-group button', function(e){
        var $btn = $(this),
            $allBtns = $btn.parent().find('button'),
            sOwn = ($btn.hasClass('import-mine')) ? 'mine' : 'notmine',
            $target = $btn.closest('.import-btn-group').find('input[value='+sOwn+']'),
            $others = $btn.closest('.import-btn-group input[type=radio]').not('input[value='+sOwn+']'),
            $select = $btn.closest('tr').find('select:first');

        $allBtns.removeClass('active');							// Toggle Button states
        $btn.addClass('active');
        $target.prop('checked', true); 							// Toggle corresponding Radio
        if(sOwn == 'mine'){$select.show()}else{$select.hide()}  // Toggle Select
        $('#save').removeClass('btn-default')
                  .addClass('btn-primary')
                  .prop('disabled', false);						// Enable Save btn on any Change

        // GA event:
        if (typeof ga != "undefined") {
            ga('send', 'event', 'pub_med', sOwn);
        };
    });

    // UN-MARK button: A way to UNMARK Mine or Not Mine is an [X] button with tooltip:
    //          'Mark as unreviewed - this item will not appear in either the Mine or Not Mine publication lists, though it may be re-added later from Search & Review.'
    $('body').on('click', '.unmark-btn', function(e){
        var $unmark = $(this),
            $row = $unmark.closest('tr'),
            $radios = $row.find('.import-btn-group input[type=radio]'),
            $notRevd = $row.find('.import-btn-group input[value="notreviewed"]'),
            $btns = $row.find('.btn-group button');

        // Munge Form DOM to un-mark item:
        $radios.prop('checked', false);
        $radios.removeAttr('checked');
        $btns.removeClass('active');
        $notRevd.prop('checked', true);
        $notRevd.attr('checked', 'checked');

        // Enable Save Changes Button
        _enableSaveChanges();

        // Move the item to the Search & Review list...
        // $('body .cv-pubmed-search table:first tbody').prepend($row);
        $row.css({'opacity':0.33});
    });
    // Enable the exposed Save Changes button on Mine list
    $('body').on('change', '.cv-pubmed-mine select', function(){
        _enableSaveChanges();
    });

    //
    // Client Side String Highlighting...
    //
    var $synopses = $('.synopsis'),
        sFirst = $('#authorfirstname').val(),
        sLast = $('#authorlastname').val();

    $synopses.each(function(i,el){
        var $syn = $(this),
            html = $syn.html(),
            iAuth = html.indexOf('.'),
            auths = html.substr(0, iAuth),
            postAuths = html.substr(iAuth);

        if(sLast.length > 1){
            // New highlighting heuristics:
            //      'la fi' highlights 'La FI'
            //      'la' highlights 'La' in 'La FI'
            //      'la f' highlights 'La F' in 'La FI'
            //  note: works on any 2+ character Last Name, any 0 or 0+ FirstInitial(s)

            var sUpperLast = sLast.substr(0,1).toUpperCase() + sLast.substr(1),
                sUpperFIs = (sFirst.trim().length > 0) ? sFirst.trim().toUpperCase() : '';

            // Highlight 'Last FI' super-strings:
            if(sUpperFIs.length > 0){
                var sFullDelim = sUpperLast + ' ' + sUpperFIs;
                auths = auths.replace(sFullDelim, ('<span class="cv-highlight">'+sFullDelim+'</span>'))
            }

            // Highlight 'Last' only:
            auths = auths.replace(sUpperLast, ('<span class="cv-highlight">'+sUpperLast+'</span>'));

            // Remove Double-Highlight Spans:
            auths = auths.replace(('<span class="cv-highlight"><span class="cv-highlight">'+sUpperLast+'</span>'), ('<span class="cv-highlight">'+sUpperLast));

            // Put back highlighted string...
            $syn.html((auths + postAuths).replace('&amp;', '&'));
        }
    });

    //
    // Fake Form Enter key handling for Search Bar
    //
    $('#authorlastname, #authorfirstname, #affiliation').on('keyup', function(event){
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if(keycode == '13') {
            $('#submitamundo').click();
        }
    });

    var _showLoading = function(){
        $('#pubmed-loading').fadeIn();
    };

    //
    // POST methods
    //
    var _sendGoogleAnalyticsAsyncEvent = function(sLabel){
        // GA event:
        var sLast = $('#authorlastname').val().replace(' ',''),
            sFirst = $('#authorfirstname').val().replace(' ',''),
            sFirstLast = (sLast.length > 0) ? ((sFirst.length > 0) ? 'first_and_lastnames': 'lastname_only') : ((sFirst.length > 0) ? 'firstname_only': 'empty_strings');

        if (typeof ga != "undefined") {
            ga('send', 'event', sLabel, sFirstLast, {useBeacon: true});
        };
    };

    var _enableSaveChanges = function(){
        $('#save').removeClass('btn-default')
                  .addClass('btn-primary')
                  .prop('disabled', false);
    }

    var _post = function(sUrl, sGA){
        _showLoading();
        _sendGoogleAnalyticsAsyncEvent(sGA);

        cvApp.ubiquitousPageRequest({
            data: JSON.stringify($('#cvpubMed').serializeObject()),
            type: 'POST',
            url: sUrl
        });
    };

    $('#submitamundo').on('click', function(event){
        _post('/cv/pubmed/search', 'pubmed_search');
    });

    $('#moreamundo').on('click', function(event){
        _post('/cv/pubmed/search', 'pubmed_next');
    });

    $('#save').on('click', function(event){
        _post('/cv/pubmed/save', 'pubmed_save');
    });

})(jQuery);
