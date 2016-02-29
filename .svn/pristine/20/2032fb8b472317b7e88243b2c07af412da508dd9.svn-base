// [Copyright]
// SmartPath v1.0
// Copyright 2014-2015 Mountain Pass Solutions, Inc.
// This unpublished material is proprietary to Mountain Pass Solutions, Inc.
// [End Copyright]


//
// BUGBUG: Long ago the Dashboard & Roster shared a code path...they do not anymore.  Separate the conjoined twins!
//

var gGridWidget;
$(function() {
     gGridWidget = $.widget( "wfWidgets.gridWidget", {
        options: {
            filterBar: false,
            url: '/appt/page/roster',
            method: 'POST',
            dataTable: false,
            mode: 'html',
            page: 'roster',
            columns: false,
            workflow_url: '/appt/jobaction/'
        },

        _hasSubRows: false,

        _create: function(){
            var $this = this,
                $grid = $this.element;

            this.data = {
                filters: false,
                rows: false
            };

            // is there a URL?
            $this.options.url = $grid.data('url');

            // is there a Filter bar?
            if(typeof $grid.data('filterBar') != 'undefined'){
                $this.options.filterBar = $($grid.data('filterBar'));
            }

            // Setup an init bool to use for re-drawing controls or not later:
            $this._dataTableInitd = false;

            // Load DATA from JSON
            $this._requestJSON();

            //We have special filter needs...add a special filter callback fn
            $.fn.dataTable.ext.search.push($this._filterDataTableCallback);

            // Bind certain BUCKET events
            $this.element.on('click', 'tr.group a', function(e){
                var $link = $(this),
                    $row = $link.closest('tr'),
                    sClass = $row.data('class'),
                    $rows = $row.closest('tbody').find("tr[data-dash-expando='"+wfApp._safeDomGuid(sClass)+"']");

                $row.toggleClass('open closed').find('.glyphicon:first').toggleClass('glyphicon-chevron-up glyphicon-chevron-down');
                $rows.toggle();
            });

            // Bind Default anywhere on row clicks to workflow page from DASHBOARD ONLY
            $('body').on('click', '.wf-gridWidget-highlights .wf-data-table tbody tr td', function(e){
                var $tr = $(e.target).closest('tr');
                var $href = $tr.find('.wf_default_wf_link:first').attr('href');
                e.preventDefault();
                e.stopPropagation();
                if(typeof $href != 'undefined' && $href.length > 0){
                    window.location.href = $href;
                }
            });

            $('body').on('click', '.wf-dash-delete', function(e){
                var $link = $(this);
                e.preventDefault();
                e.stopPropagation();
                var isSure = window.confirm('Are you sure wish to remove this event from your Dashboard View?');
                if(isSure){
                    $.ajax({
                        url: $(this).data("delete"),
                        type: 'POST',
                        success: function(data, textStatus, xhr) {
                            // REDIRECT in reponse should just work...
                            // $this._removeDeletedRow($(this));
                            if(wfApp._sessionExpiryLogoutRequired(data)){return false;} // Just in case we get a Success response...of the Login form
                            window.location.reload();
                        },
                        error: function(jqXHR, textStatus, errorThrown) {
                            console.log('AJAX Error:', jqXHR, textStatus, errorThrown);
                        }
                    });
                }
            });

            $('body').on('click', '.wf-actions-btn-wrapper ul li a', function(){
                var sCmd = $(this).data('command'),
                    zIDs = $this._getCurrentRowIDs();

                if(sCmd == 'print'){
                    // Print
                    //alert('User hit Print, we have ' + zIDs.length + ' in an array ready to send to the server...');
                    $('#wf-rooster-grid_wrapper .buttons-print').trigger('click');
                }
                else if(sCmd == 'csv'){
                    // CSV
                    //alert('User hit Export to CSV, we have ' + zIDs.length + ' in an array ready to send to the server...');
                    $('#wf-rooster-grid_wrapper .buttons-csv').trigger('click');
                }
                else if(sCmd == 'excel'){
                    // CSV
                    //alert('User hit Export to CSV, we have ' + zIDs.length + ' in an array ready to send to the server...');
                    $('#wf-rooster-grid_wrapper .buttons-excel').trigger('click');
                }
                else{
                    // PDF
                    //alert('User hit Export to PDF, we have ' + zIDs.length + ' in an array ready to send to the server...');
                    $('#wf-rooster-grid_wrapper .buttons-pdf').trigger('click');
                }
                // console.log(zIDs);
            });

            currentWidget = $this;

        },

        _getInstance: function(){
            return this;
        },

        _createDataTable: function(rows){
            var $this = this;

            // Then we have to create generated column options for the DataTable init...
            var colOpts = [];
            for(var index=0; index < $this.options.columns.length; index++){
                var oCol = $this.options.columns[index],
                    jCol = {};

                jCol.title = oCol.title;
                jCol.data = oCol.guid;
                jCol.visible = oCol.visible;
                jCol.render = oCol.render || null;
                if($this.options.page == 'dashboard'){jCol.orderData = [0,index];}
                colOpts.push(jCol);
            }

            // Dashboard options for DataTable:
            var instanceOptions = {};

            instanceOptions = {
                data: rows,
                columns: colOpts,
                theme: 'bootstrap',
                deferRender: true,
                orderFixed: [[ 0, 'asc' ]],
                order: [[ 0, 'asc' ], [1,'desc']],
                displayLength: -1,
                drawCallback: function(){$this._dashboardDrawCallback();},
                fixedHeader: {headerOffset: 94, forceChange: false},
                initComplete: function () {
                    //new $.fn.dataTable.FixedHeader( $oTable, {offsetTop: 94} );
                },
                rowCallback: $this._dashboardRowRenderCallback,
                autoWidth: false,
                oLanguage: {
                    sEmptyTable: 'No matching records found.',
                    sZeroRecords: 'No matching records found.'
                }
            }

            // Then finally we init the dataTable...
            var $oTable = $('<table id="wf-rooster-grid" class="table wf-data-table table-condensed wf-clientsort"></table>');
            $('.wf-gridWidget').prepend($oTable);
            currentDT.oTbl = $oTable.DataTable(instanceOptions);
            $('#wf-filter').trigger('click'); // Forces Dashboard Bucketing, and also filter load
            currentWidget._initDataTableUXs();

        },

        _dashboardRowRenderCallback: function(row, data){
            var $this = currentWidget;
            $(row).attr('data-dash-expando', wfApp._safeDomGuid(data.events));
        },

        _hideShowSubs: function(){
            // NEW: Hide/Show Subrows integrated
            if(!$('#hideshowsubs').prop('checked')){ $('#wf-rooster-grid tbody tr:visible .subRow').hide(); }
            else{ $('#wf-rooster-grid tbody tr:visible .subRow').show(); }
        },

        _dashboardDrawCallback: function(settings){
            var $this = this;

            $this._initDataTableUXs();

            // We filter() the grid after load...wait for that...
            if(currentDtFilters == null){
                return true;
            }

            var api = currentDT.oTbl,
                lastSort = [],
                rows = api.rows( {page:'current'} ).nodes(),
                rowData = api.rows( {page:'current'} ).data(),
                iCat = 0, numRows = 0, totRows = 0,
                sHeader = '<tr class="group open" style="background:#999; color:#fff;" data-class="{{class}}"><td colspan="12"><a href="#" class="rowGroupLink"><span class="glyphicon glyphicon-chevron-{{open}}"></span>{{nameRows}}</a> (<span class="numRows">{{numRows}}</span>)</td></tr>',
                curCat = '', zOrderedCats = [], zOpenStates = [];

            for(i = 0; i < rowData.length; i++){ // ! Assumes data is in Status Order !

                if($.inArray(rowData[i].events, zOrderedCats) < 0){ // Load up used Categories
                    zOrderedCats.push(rowData[i].events);
                }

                var $row = $(rows).eq( i ),
                    rowStatus = rowData[i].events,
                    status = rowStatus,
                    bVisible = $row.is(':visible');

                if(curCat == ''){ // Render first Category Header...
                    zOpenStates[0] = bVisible;
                    $row.before( sHeader.replace('{{nameRows}}', status).replace('{{class}}',status).replace('{{open}}', (bVisible ? 'up':'down')) );
                    curCat = status;
                }

                if(status == curCat){ // Does the current row match the current header?
                    numRows++; // Increment Count...
                }
                else{  // !! New Category!!
                    curCat = rowStatus;
                    zOpenStates.push(bVisible); // store open-ess

                    // Magically insert the Count of the last Status into that header:
                    var $prevHeader = $row.closest('tbody').find('tr.group:last');
                    if(typeof $prevHeader != 'undefined' && $prevHeader.length == 1){
                        $prevHeader.find('td:first').html( $prevHeader.find('td:first').html().replace('{{numRows}}', numRows) );
                    }
                    totRows += numRows;
                    numRows = 1;
                    iCat++; // And set the Next cat...
                    $row.before( sHeader.replace('{{nameRows}}', status).replace('{{class}}',status).replace('{{open}}', (bVisible ? 'up':'down')) );
                }
                // Last row...still must insert the last numRows
                if(i == rows.length-1){
                    // Magically insert the Count of the last Status into that header:
                    totRows += numRows;
                    var $headers = $row.closest('tbody').find('tr.group'),
                        $prevHeader = $headers.eq($headers.length - 1);
                    if(typeof $prevHeader != 'undefined'){
                        $prevHeader.find('td:first .numRows').html( numRows );
                    }
                    $this.element.find('.dataTables_info').text(totRows+' actionable items'); // push totRows to info area...
                }
            }

            redrawResizeDataTable();
        },

        _getCurrentRowIDs: function(){
            var $this = this,
                api = currentDT.oTbl,
                // rows = api.rows( {page:'current'} ).nodes(),
                rowData = api.rows({
                    order:  'current',  // 'current', 'applied', 'index',  'original'
                    page:   'all',      // 'all',     'current'
                    search: 'applied'      // 'none',    'applied', 'removed'
                }).data(),
                zIDs = [];

            for(i=0;i<rowData.length;i++){
                // if(i==0){console.log(rowData[i])}
                var sID = rowData[i].pcnID ;
                zIDs.push(sID);
            }
            return zIDs;
        },

        registerFilterBar: function(){
            // For filter bar to register self with dataTableWidget
            var $this = this;
        },

        filterGrid: function(filters){
            var $this = this,
                oFilters = filters || $this.filtersUX.gridFilterBar('getFilters');

            $this.filters = oFilters;
            currentDtFilters = $this.filters;

            var bAll = true;
            $.each($this.filters, function(i,o){
                if($this.filters[i] !== true){
                    bAll = false;
                }
            });

            // Using Global Currents to avoid really expensive jQuery & DataTable lookups on each row...
            currentDtFilters = $this.filters;
            currentDtShowAll = bAll;
            currentDtPgName = $this.options.page;
            currentDtHasFild = true; // BUGBUG: Limit 1 DataGrid per page this way...

            iDebug = 0;
            $this._currentFilteredData = $($.fn.dataTable.fnTables()[0]).dataTable().fnFilter(''); // BUGBUG: Limit 1 DataGrid per page this way...
        },

        getFilters: function(){
            return this.filters;
        },

        _filterDataTableCallback: function(settings, data, dataIndex){
            // NOTE: this runs ONCE PER ROW, so OPTIMIZE All Js Execution (no JQuery lookups if we can avoid, etc)

            // Perf Saver: Bail Early if All selected
            if(currentDtShowAll || currentDtHasFild === false){ return true; }

            // Perf Saver: First Load is always All, but subsequent ones are not
            currentDtHasFild = true;

            var filters = currentDtFilters,
                department = data[1] || '',
                isPrimary = (department.indexOf('Secondary') == -1) ? true : false,
                isSecondary = !isPrimary,
                primalityMatch = (filters.primality === true) ? true : false,
                positionMatch = (filters.positions === true) ? true : false,
                trackMatch = (filters.tracks === true) ? true : false,
                titleMatch = (filters.titles === true) ? true : false,
                departmentMatch = (filters.departments === true) ? true : false,
                stypeMatch = (filters.actions === true) ? true : false,
                statusMatch = (filters.statuses === true) ? true : false,
                metaMatch = (currentDtPgName) == false,
                eventsMatch = (filters.events === true) ? true : false,
                tirMatch = filters['tir'],
                bTags = true,
                rowData = settings.aoData[dataIndex]._aData;

            // Dashboard support via overwrites:
            if (currentDtPgName == 'dashboard'){
                filters.primality = true;
                positionMatch = true;
                statusMatch = true;
                bTags = false;
                tirMatch = true;
            }

            //if(dataIndex < 3){console.log(filters);console.log(rowData)}

            if(tirMatch !== true && tirMatch > 0){
                if(data[6] < tirMatch){
                    return false;
                }
            }

            //
            // In this older version of filters, each one pipe delimits, we we match '|'+str +'|' in '|filterval1|2|3|4|'...
            //
            var _matchFilter = function(filters, hData, bTags){
                if(filters.indexOf('|'+hData+'|') >= 0 ){return true;}
                return false;
            }

            primalityMatch = (
                filters.primality === true || (
                    (filters.primality.indexOf('|Primary|') >= 0 && isPrimary) ||
                    (filters.primality.indexOf('|Secondary|') >= 0 && isSecondary))
                );
            if(!primalityMatch){
                return false;
            }

            if(!positionMatch && !_matchFilter(filters.positions, rowData.positions, bTags)){
                return false;
            }

            if(!trackMatch && !_matchFilter(filters.tracks, rowData.tracks, bTags)){
                return false;
            }

            if(!titleMatch && !_matchFilter(filters.titles, rowData.titles, bTags)){
                return false;
            }

            if(!departmentMatch && !_matchFilter(filters.departments, rowData.departments, bTags)){
                return false;
            }

            if(!eventsMatch && !_matchFilter(filters.events, rowData.events, bTags)){
                return false;
            }

            // NOTE: there is a mapping of server-side STR Flags to each meta type here... see wf.gridFilters.js line ~116
            if(!metaMatch && !((filters.metatrack.indexOf('|All|') >=0) ? true : _matchFilter(filters.metatrack, rowData.metatype, bTags))){
                return false;
            }

            if(!stypeMatch){
                var sData = rowData.actions || false;
                if(sData !== false && (sData.indexOf('>--<') >= 0 && filters.actions.indexOf('|None|') >= 0)){
                    stypeMatch = true;
                }
                else{
                    stypeMatch = _matchFilter(filters.actions, sData, bTags);
                }
                if(!stypeMatch){ return false; }
            }

            if(!statusMatch){
                var sData = rowData.statuses;
                if(sData.indexOf('>--<') >= 0 && filters.statuses.indexOf('|None|') >= 0){
                    statusMatch = true;
                }
                else{
                    statusMatch = _matchFilter(filters.statuses, sData, bTags);
                }
                if(!statusMatch){ return false; }
            }

            if(iDebug == 0){
                 // console.log($.inArray(data[0], currentDtFilters), currentDtFilters, data, primalityMatch , positionMatch , trackMatch , titleMatch , departmentMatch, stypeMatch, statusMatch, data, settings, dataIndex)
            }

            // Wow, that was potentially expensive...
            return true;

        },

        _requestJSON: function(){
            var $this = this,
                el = $this.element;
            $.ajax({
                url: $this.options.url,
                type: $this.options.method,
                data: null,
                headers: null,
                success: function(data, textStatus, xhr) {
                    if(wfApp._sessionExpiryLogoutRequired(data)){return false;} // Just in case we get a Success response...of the Login form

                    // Cache DATA
                    $this.data.filters = {
                        positions: data.position_status_list,
                        primality: data.primality_list,
                        tracks: data.track_list,
                        titles: data.title_list,
                        departments: data.department_list,
                        actions: data.job_action_type_list,
                        statuses: data.job_action_status_list,
                        events: data.event_list
                    };

                    // Create FilterBar
                    $this.filtersUX = $this.options.filterBar.gridFilterBar({
                        data: $this.data.filters,
                        gridWidget: el
                    });

                    // Create Table DOM; render dataTable
                    // $this._createDataTableHTML(data);
                    var munged = null;
                    munged = $this._mungeRosterDataForDashboard(data.dashboard);
                    $this.data.rows = munged;
                    $this._createDataTable(munged);
                    $this._fillHeader(munged);

                },
                error: function(jqXHR, textStatus, errorThrown) {
                    console.log('AJAX Error:', jqXHR, textStatus, errorThrown);
                }
            });
        },

        _mungeRosterDataForDashboard: function(events){
            var $this = this,
                zRows = [],
                zEvents = events;

            $.each(events, function(iE, bucket){
                var sBucket = bucket.description;
                $.each(bucket.items, function(iB, row){
                    var thisRow = {};

                    thisRow.names = row.person.full_name || '<i>Vacant</i>';
                    thisRow.events = sBucket;
                    thisRow.lastupdated = '<span title="Updated at: '+row.job_action.updated+'">'+row.job_action.updated+'</span>';
                    thisRow.tracks = row.track.descr || '';
                    thisRow.titles = row.title.descr || '';
                    thisRow.departments = row.department.descr || '';
                    thisRow.positions = row.title.descr || '';
                    thisRow.actions = row.workflow.descr || '';
                    thisRow.deleteLink = '<a href="#" class="wf-dash-delete btn-small btn-default" data-delete="'+row.deleteURL+'" title="Delete this event"><span class="glyphicon glyphicon-remove"></span></a>';
                    if(row.url != null){
                        thisRow.pcns = '<a class="wf_default_wf_link" href="'+row.url+'" target="_workflow">'+row.position.pcn+'</a>';
                    }
                    else{
                        thisRow.pcns = '<span class="wf_default_wf_link">'+row.position.pcn+'</span>';
                    }
                    thisRow.pcnID = row.position.pcn;
                    thisRow.workflows = row.workflow.descr;
                    thisRow.metatype = row.job_action_type.code;

                    zRows.push(thisRow);
                });
            });

            return zRows;
        },

        _initDataTableUXs: function(){
            var $this = this;

            // Used to move the datatable UXs around a bit...
            if($this._dataTableInitd){return true;}

            $('.cv-table-loading').hide();
            //return true;

            var $info = $this.element.find('.dataTables_info'),
                $leng = $this.element.find('.dataTables_length'),
                $filt = $this.element.find('.dataTables_filter'),
                $page = $this.element.find('.dataTables_paginate'),
                $stats = $('#wf-pseudo-reporting'),
                $top = $leng.parent(),
                $bot = $info.parent(),
                $tor = $filt.parent(),
                $wrapper = $('#wf-rooster-grid_wrapper');

            // Munge DataTables peripheral DOMs into our layout
            $info.appendTo($tor).css({'float': 'right', position: 'relative'});
            $filt.appendTo($top).css('float', 'left');
            $leng.hide(); // do not show chunk size for Dashboard (all are shown in buckets)
            $page.hide(); // ditto


            $this._dataTableInitd = true;

            $('.cv-table-loading').hide();

            // Little 'x' in Search to clear typing with one click
            var $label = $('#wf-rooster-grid_filter label:first'),
                $input = $label.find('input:first');
                $cancel = $label.append($('<span class="glyphicon glyphicon-remove-circle cancel_search"></span>'));

            $cancel.click(function(e){
                $input.val('');
                currentDT.oTbl.search('').draw();
            });

            return false;
        },

        _fillHeader: function(data){
            var $this = this,
                cpg = 'events';

            //$('#wf-rosterdash-count').html(data.length + ' actionable '+cpg+' are available to you')
        }

    });

    $(window).on('resize', function () {
        redrawResizeDataTable();
    });

    $(window).scroll(function() {
        clearTimeout($.data(this, 'scrollTimer'));
        $.data(this, 'scrollTimer', setTimeout(function() {
            $('#wf-rooster-grid').DataTable().fixedHeader.adjust();
            _equalizeFixedHeaderWidths();
        }, 200));
    });

});

var currentDtFilters = null;
var currentDtShowAll = null;
var currentDtHasFild = false;
var currentDtPgName = 'dashboard';
var currentWidget = false;
var iDebug = 0;
var currentDT = {
    oTbl: false,
    isResizing: false,
    unInitd: true
};

function redrawResizeDataTable(){
    if((currentDT.oTbl !== false || currentDT.unInitd) && currentDT.isResizing === false){
        currentDT.isResizing = true;
        window.setTimeout(function(){
            _equalizeFixedHeaderWidths();
            currentDT.isResizing = false;
            currentDT.unInitd = false;
        }, 0);
    }
    return false;
}

function _equalizeFixedHeaderWidths(){
    // var $table = $('#wf-rooster-grid').DataTable();
    // console.log('_equalizeFixedHeaderWidths');
    if($('.fixedHeader-floating').is(':visible')){
            var zBases = $('#wf-rooster-grid thead tr th'),
            zFixed = $('.fixedHeader-floating thead tr th');
            for(i=0;i < zBases.length; i++){
                var iBase = $(zBases[i]).width();
                $(zFixed[i]).width(iBase);
            }
    }
}
