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
     gGridWidget = $.widget( "wfWidgets.rosterWidget", {
        options: {
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

            // Setup an init bool to use for re-drawing controls or not later:
            $this._dataTableInitd = false;

            // Load DATA from JSON
            $this._requestJSON();

            //We have special filter needs...add a special filter callback fn
            // BUGBUG - This?
            // $.fn.dataTable.ext.search.push($this._filterDataTableCallback);
            $.fn.dataTable.ext.search.push($this._filterRosterCallback);

            // ROSTER ONLY
            $('body').on('change', 'select[name="wf-rooster-grid_length"]', function(e){
                // Cookie user selected page size:
                var sVal = $(e.target).val(),
                    sSize = (sVal != 'All') ? sVal : '-1';
                $.cookie('rosterPgSize', sSize, { path: '/', expires: 365});
                $this._hideShowSubs();
            });

            // ROSTER ONLY
            $('#wf-roster-stat-toggler').click(function(e){
                var $this = this,
                    $el = $(this),
                    $table = $el.closest('table');
                $el.find('.glyphicon').toggleClass('glyphicon-chevron-up glyphicon-chevron-down');
                $table.find('tbody').toggle();
                $table.toggleClass('wf-stats-closed wf-stats-open');
                //setTimeout(function(){window.scrollBy(0, 10)}, 1);
                window.scrollBy(0, 10);
                setTimeout(function(){window.scrollBy(0, -10)}, 2);
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
            });

            currentWidget = $this;

        },

        _createDataTable: function(rows){
            var $this = this,
                $that = $this;

            // Then we have to create generated column options for the DataTable init...
            var colOpts = [];
            for(var index=0; index < $this.options.columns.length; index++){
                var oCol = $this.options.columns[index],
                    jCol = {};

                jCol.title = oCol.title;
                jCol.data = oCol.guid,
                jCol.visible = oCol.visible;
                jCol.render = oCol.render || null;
                colOpts.push(jCol);
            }

            // ROSTER
            var instanceOptions = {
                data: rows,
                columns: colOpts,
                autoWidth: false,
                theme: 'bootstrap',
                deferRender: true,
                drawCallback: function(){$this._rosterDrawCallback();},
                // fixedHeader: {headerOffset: 94},
                initComplete: function(settings, json){
                    $this.oApi = this.api();
                    $this._rosterHeaderFilters(settings, $this.data.filters);
                    $this.filterRoster();
                },
                dom: '<"clear"><"H"Blfr>t<"F"ip>',
                autoWidth: false,
                oLanguage: {
                    sEmptyTable: 'No matching records found.',
                    sZeroRecords: 'No matching records found.'
                },
                pageLength: (typeof $.cookie('rosterPgSize') != 'undefined') ? ($.cookie('rosterPgSize') <= 0) ? -1 : $.cookie('rosterPgSize') : 50,
                lengthMenu: (rows.length < 1000) ? [ [10, 25, 50, 100, 250, -1], [10, 25, 50, 100, 250, "All"] ] : [ [10, 25, 50], [10, 25, 50] ],
                buttons: [
                        {
                            extend: 'csv',
                            exportOptions: {
                                columns: ':visible'
                            }
                        },{
                            extend: 'excel',
                            exportOptions: {
                                columns: ':visible'
                            }
                        },{
                            extend: 'print',
                            orientation: 'landscape',
                            exportOptions: {
                                columns: ':visible'
                            },
                            // message: '<div id="wf-print-msg">BUGBUG TestTest</div>',
                            message: '',
                            header: true,
                            autoPrint: true,
                            customize: function(window){
                                var $body = $(window.document.body);

                                // Build some arbitrary HTML to insert above table
                                $body.prepend($(_rosterPrintHTML));

                            }
                        }
                    ]
            }

            // Finally we init the dataTable...
            var $oTable = $('<table id="wf-rooster-grid" class="table wf-data-table table-condensed wf-clientsort"></table>');
            $('.wf-gridWidget').prepend($oTable);
            currentDT.oTbl = $oTable.DataTable(instanceOptions);
            $('#wf-filter').trigger('click'); // Forces Dashboard Bucketing, and also filter load
            currentWidget._initDataTableUXs();

            // Buttons conflict with FixedHeader, init'ing fixedHeader after buttons fixes fixed header:
            var table = $oTable.DataTable();

            // New scheme for Multi-Skin Rosters with Fixed Header vals - use min-height prop
            var iMH = $('.mps-body .mpsheader').css('min-height').replace('px','')*1;
            new $.fn.dataTable.FixedHeader( currentDT.oTbl, {
                headerOffset: iMH,
                forceChange: false
            } );

            //
            // Attempt to intercept Export Button clicks so we can munge DOM a bit for a few things...
            //
            $this._interceptDirectExportBtnClicks();

        },

        _interceptDirectExportBtnClicks: function(){
            //
            // The dt-buttons are the Print & Export buttons the Datatable renders when we use that plugin - but WE HIDE THEM.
            // We have an Actions menu with simple links that trigger them instead
            //
            var $this = this,
                $that = $this;

            // Move click events to dblClick, mainly so we can safe-trigger via click():
            $('.dt-buttons .dt-button').each(function(i, el){
                var $el = $(el),
                    zEvents = $._data($el.get(0), "events");
                $el.addClass('wf-click-intercept');
                $el.on('dblclick', zEvents['click'][0].handler);
                $el.off('click');
            });

            $('.dt-buttons .dt-button').on('click', function(e){
                var target = e.target,
                    $target = $(target);

                e.stopPropagation();
                e.preventDefault();

                // If Psuedoreporting is closed, open it:
                var $reportingClone = $('#wf-roster-stats').clone().removeClass('starthidden wf-stats-closed').addClass('wf-stats-open'),
                    $wrap = $('<div><h3>Report Summary</h3></div>');

                $reportingClone.find('.starthidden').removeClass('starthidden');
                $reportingClone.find('.glyphicon').hide();
                var $info = $reportingClone.find('#wf-rooster-grid_info');
                var sShowing = $info.text();
                sShowing = 'Showing ' + sShowing.substr(sShowing.indexOf('of ')+3).replace('entries', 'matching results');
                $info.text(sShowing);
                //$info.parent().contents().filter(function() {return this.nodeType === 3}).remove(); // Removes ':' in parent el, which wraps oddly in Print modes
                var sInfo = $reportingClone.find('thead tr:first th:first').text();
                $reportingClone.prepend('<div class="indent">'+sInfo+'</div>');
                $reportingClone.find('thead tr:first th:first').empty();
                $wrap.append($reportingClone);

                var sPRS = $wrap.html()+'<br/><br/>'

                //
                // Smart Filter summaries
                //
                var zBuckets = $('#wf-rooster-grid thead th .wf-hf-wrap');
                var sHF = '<div><h4>Filters In Effect:</h4><div class="indent">';

                zBuckets.each(function(i,o){
                    var $bucket = $(o),
                        $all = $bucket.find('input[type=checkbox]').filter(function(){
                            var $el = $(this);
                            return !$el.parent().hasClass('ms-search') && !$el.parent().hasClass('optgroup') && !$el.parent().parent().hasClass('ms-select-all');
                        }),
                        $chks = $all.filter(function(){return $(this).is(':checked');}),
                        sType = wfApp.textNodes($bucket.closest('th')),
                        zPrintedFilters = ['Track', 'Title / Rank', 'Department'],
                        bSelect = $bucket.find('select').length > 0 ? true : false,
                        bAll = $all.length == $chks.length;

                    //console.log('Type:', sType, ' bAll:', bAll, ' bSelect:',bSelect, ' $all:', $all.length, ' $chks:', $chks.length, ' um: ', $bucket.find('select').val());//

                    if($.inArray(sType, zPrintedFilters) >= 0 || !bAll){
                        // TIR Select:
                        if(bSelect){
                            var $sel = $bucket.find('select'),
                                $val = $sel.val();

                            if($.isArray($val)){
                                sHF += sType + ': ';
                                sHF += (bAll) ? 'No Filter Restrictions' : ('('+$chks.length + ' of ' + $all.length +' selected): ');
                                if(bAll){
                                    // sHF += $chks.length + ' of ' + $all.length +' options selected';
                                }
                                else{
                                    $.each($val, function(nth,valu){
                                        sHF += (nth != $val.length-1) ? valu+', ' : valu;
                                    });
                                }

                                sHF += '<br/><br/>';
                            }
                        }
                    }
                });
                sHF += '</div></div>';

                // If there is a further search string being used, show that too:
                var $txtSearch = $('#wf-rooster-grid_filter input[type=search]'),
                    curSearch = $txtSearch.val(),
                    zTxts = $('#wf-rooster-grid thead th .wf-hf-wrap input[type=text]'),
                    sTs = '';

                var tTxt = curSearch;
                zTxts.each(function(nth,valu){
                    tTxt += $(valu).val();
                });
                if(tTxt != ''){
                    sTs = '<h4>Text Search(es) in effect:</h4>';
                    if(curSearch != ''){
                        sTs += '<div class="indent">Results only include rows matching "'+ curSearch +'" in any cell</div></br>';
                    }
                    zTxts.each(function(nth,valu){
                        var sV = $(valu).val();
                        if(sV != ''){
                            sTs += '<div class="indent">Results only include rows in the '+wfApp.textNodes(zTxts[nth].closest('th'))+' column containing "'+ $(valu).val() +'"</div></br>';
                        }
                    });
                    sTs += '<br/>';
                }

                _rosterPrintHTML = sPRS + sHF + sTs;

                //
                // Challenge here: The Print, CSV, and XLSW Column Headers cannot have the giant filter selects & inputs in them - the innerText/HTML must be just the colName.
                //

                $that.shadowHeader = [];

                // Move the filters out of the Col Headers into a store (necessary for all CSV, XLS, Print output is a simple string col header)
                $('.wf-data-table:first thead tr th').each(function(i,th){
                    var $th = $(th),
                        $filter = $th.find('.wf-hf-wrap').detach();

                    $that.shadowHeader.push($filter);
                });

                //
                // Add a Style blob el for layout in Print
                //
                var sCss = '<style>table tbody tr td{padding:0 5px 0 0 !important;} .indent{padding-left:15px;}</style>';
                _rosterPrintHTML += sCss;

                // We moved the Datatable events to dblClick...
                $target.trigger('dblclick');

                // This will run AFTER the Print window closes - main need is to replace Col Header Fitlers:
                window.setTimeout(function(){
                    //console.log('TimeOut Runner Running...', $that.shadowHeader);
                    $('.wf-data-table:first thead tr th').each(function(i,th){
                        $(th).append($that.shadowHeader[i]);
                    });
                },1000);

            });
        },

        _rosterHeaderFilters: function (settings, zFilters) {
            var $this = this;
            $this.oApi.columns().every( function (index, tableLoop, columnLoop) {
                var column = this,
                    def = settings.aoColumns[index],
                    $wrap = $('<div class="wf-hf-wrap"></div>'),
                    zSelects = ['departments', 'tracks', 'titles', 'tir', 'actions', 'statuses'],
                    zInputs = ['pcns', 'names','lastupdated','proposedstart'],
                    zDates = ['lastupdated','proposedstart'],
                    sCol = '', colData = [], colTitle = '', allTitle = '', keyTitle = '', keyValue = '', xtraVal = false, dProp = ''
                    showNone = false, useSelect = false, useInput = false, isSpecialTIRMenu = false, useDatePicker = false,
                    jOpts = {
                        filter: true,
                        selectAllText: 'Select All',
                        selectAllDelimiter: ['',''],
                        width:'99%',
                        onOpen: function(){
                            _scrollTopFilter();
                            _preventDoubleDropdowns();
                        },
                        onClose: function(){_preventDoubleDropdowns()}
                    };

                if(def.bVisible !== true){
                    return false;
                }
                else{
                    sCol = def.data;
                }

                // Map the Data.Filter Lists into the column select > options
                switch(sCol){
                    case 'departments':
                        useSelect = true;
                        colData = zFilters.departments;
                        colTitle = 'All Departments';
                        keyTitle = 'department_descr';
                        //keyValue = 'department_code';
                        keyValue = 'department_descr';
                        dProp = 'departments';
                        break;
                    case 'tracks':
                        useSelect = true;
                        colData = zFilters.tracks;
                        colTitle = 'All Tracks';
                        keyTitle = 'track_descr';
                        //keyValue = 'track_code';
                        keyValue = 'track_descr';
                        dProp = 'tracks';
                        break;
                    case 'titles':
                        useSelect = true;
                        colData = zFilters.titles;
                        colTitle = 'All Titles';
                        keyTitle = 'title_descr';
                        //keyValue = 'title_code';
                        keyValue = 'title_descr';
                        dProp = 'titles';
                        break;
                    case 'tir':
                        useSelect = true;
                        colData = zFilters.primality;
                        colTitle = 'All TIRs';
                        keyTitle = 'descr';
                        //keyValue = 'primality';
                        keyValue = 'descr';
                        dProp = 'tir';
                        isSpecialTIRMenu = true;
                        jOpts.multiple = true;
                        jOpts.multipleWidth = 150;
                        break;
                    case 'actions':
                        useSelect = true;
                        colData = zFilters.actions;
                        colTitle = 'All Actions';
                        keyTitle = 'job_action_type_descr';
                        //keyValue = 'job_action_type_code';
                        keyValue = 'job_action_type_descr';
                        dProp = 'actions';
                        showNone = true;
                        break;
                    case 'statuses':
                        useSelect = true;
                        colData = zFilters.statuses;
                        colTitle = 'All Statuses';
                        keyTitle = 'job_action_status';
                        keyValue = 'job_action_status';
                        dProp = 'statuses';
                        showNone = true;
                        break;
                    case 'pcns':
                        useInput = true;
                        dProp = 'pcns';
                        break;
                    case 'names':
                        useInput = true;
                        dProp = 'names';
                        break;
                    case 'lastupdated':
                        useInput = true;
                        dProp = 'lastupdated';
                        useDatePicker = true;
                        break;
                    case 'proposedstart':
                        useInput = true;
                        dProp = 'proposedstart';
                        useInput = true;
                        break;
                    default:
                        return false;
                }

                if(useSelect){
                    var select = $('<select id="fw-hf-'+sCol+'" class="wf-kill-dupes" multiple="multiple" data-prop="'+dProp+'"></select>');

                    if(showNone){
                        select.append('<option value="NONE" checked selected>None</option>');
                    }

                    if(isSpecialTIRMenu){
                        var zPos = [];
                        $.each($this.data.filters.positions, function(i,v){
                            var sName = v.status_code.humanize(),
                                sVal = v.status_descr,
                                oPos = {
                                    name: (sName == 'Inprogress') ? 'In Progress': sName,
                                    val: sVal
                                };
                            zPos.push(oPos);
                        });
                        var zVals = [
                                {   ogName: 'Position Status',
                                    ogVals: zPos
                                },
                                {   ogName: 'Time In Rank',
                                    ogVals: [
                                        {name:'0-1 yr', val:'0-12'},
                                        {name:'1-2 yrs', val:'12-24'},
                                        {name:'2-3 yrs', val:'24-36'},
                                        {name:'3-4 yrs', val:'36-48'},
                                        {name:'4-5 yrs', val:'48-60'},
                                        {name:'5+ yrs', val:'60+'}
                                    ]
                                }
                            ],
                            sHTML = '';
                        $.each(zVals, function(i, optGroup){
                            sHTML += '<optgroup label="'+zVals[i].ogName+'">';
                            $.each(optGroup.ogVals, function(j,v){
                                sHTML += '<option value="'+ optGroup.ogVals[j].val+'" selected>'+optGroup.ogVals[j].name+'</option>';
                            });
                            sHTML += '</optgroup>';
                        });
                        select.append($(sHTML));
                    }
                    else{
                        column.data().unique().each( function ( d, j ) {
                            if(d == '' && showNone){return false;}
                            select.append( '<option value="'+d+'" selected>'+d+'</option>' )
                        } );
                    }

                    select.on( 'change', function (e) {
                        wfApp.inputDelay(function(){
                            $this.filterRoster(index);
                            e.stopPropagation();
                            e.preventDefault();
                            return true;
                        }, 500);
                    });

                    //select.appendTo( $(column.header()).empty() );
                    select.appendTo( $wrap );
                    $wrap.appendTo($(column.header()));

                    jOpts.allSelected = colTitle;

                    $(select).multipleSelect(jOpts);

                }
                else if(useInput){
                    var input = $('<input type="text" id="fw-hf-'+sCol+'" class="wf-kill-dupes wf-hf-input" data-prop="'+dProp+'"/>'),
                        delay = (function(){
                            var timer = 0;
                            return function(callback, ms){
                                clearTimeout (timer);
                                timer = setTimeout(callback, ms);
                            };
                        })(),
                        filter = function(e){
                            $this.filterRoster(index);
                            e.stopPropagation();
                            e.preventDefault();
                            return true;
                        };

                    input.on( 'keyup clearMe', function (e) {
                        if(e.type == 'clearMe'){
                            input.val('');
                            filter(e);
                        }
                        else{
                            delay(function(){
                                filter(e);
                                input.focus();                          //  Filtering triggers inserts (total #s table), col/cell layout, tons of stuff...and somewhere along the line, focus is lost.
                                delay(function(){input.focus()}, 0);    //   It is not super elegant, but focus() and a timeout'd focus() here seem very robust cross-browser to solve.
                            }, 250);
                        }

                    });

                    input.appendTo( $wrap );

                    // Little Cancel Buttons for text inputs:
                    var $cancel = $('<span class="glyphicon glyphicon-remove-circle cancel_search"></span>');
                    $cancel.click(function(e){
                        input.trigger('clearMe');
                        // $this.oApi.search('').draw();
                    });

                    // Insert to DOM:
                    $cancel.appendTo($wrap);
                    input.appendTo($wrap);
                    $wrap.appendTo($(column.header()));
                }
                else if(useDatePicker){
                    // Before & After select, plus date picker input...
                    var $drop = $('<select class="wf-roster-date-drop" data-prop="'+dProp+'"><option value="after">&gt;=</option><option value="before">&lt;=</option></select>'),
                        $date = $('<input type="text" <input type="text" placeholder="MM/DD/YYYY" class="mps-date-picker wf-roster-date-pick" data-prop="'+dProp+'"/>'),
                        $wrap = $('<div class="wf-roster-date-wrap"></div>');

                    $wrap.append($drop);
                    $wrap.append($date);

                    $wrap.children().on( 'change', function (e) {
                        wfApp.inputDelay(function(){
                            $this.filterRoster(index);
                            e.stopPropagation();
                            e.preventDefault();
                            return true;
                        }, 500);
                    });
                    //$wrap.appendTo($(column.header()));
                    mpsApp.mpsDatePickerizeDom($(column.header()));
                }
            });

            // This is to prevent bubbling clicks in inserted filters from Sorting columns
            $('#wf-rooster-grid th, .fixedHeader-floating th').each(function(i, el){
                var $el = $(el),
                    zEvents = $._data($el.get(0), "events");
                //console.log(zEvents['click'][0].handler);
                //$(el).data('oldClick', zEvents['click']);
                $el.on('dblclick', zEvents['click'][0].handler);
                $el.off('click');
            });

            $('body').on('click', 'th', function(e){
                var target = e.target,
                    $target = $(target);
                if(!$target.hasClass('ms-choice') && $target.prop('tagName') == "TH"){
                    $target.trigger('dblclick');
                }
                else{
                    //$target.off('click'); ???
                }
                // !!! BUGBUG: Scroll Select to top of visible pane !!! ???
            });
        },

        _vacantPrimaries: [],
        _vacantSecondaries: [],
        _vacantSupplementals: [],
        _reportPrimaries: [],
        _reportSecondaries: [],
        _reportSupplementals: [],
        _pendingPrimaries: [],
        _pendingSecondaries: [],
        _pendingSupplementals: [],
        _lastCountedData: false,
        _lastCountedDate: false,
        _rosterDrawCallback: function(){
            var $that = this,
                $this = currentWidget;

            /*
            -----
            SPEC:
            -----
            Counts from the Roster page:
            Counting needs to work differently depending on the users department selections.
            When the filter is set to more than one Department (or the entire school) counting should follow these rules.

                - A faculty member can only be counted in one slot. (Primary, Secondary or Supplemental).  No double counting
                - If the faculty member has a primary appointment then count them as primary in the Primary
                - If the faculty member has no primary but has a secondary count them as a secondary.  (this happens when the primary is outside of the medical school)
                - Supplemental positions are always counted as the # of faculty in a supplemental track. (not sure how we deal with schools that do not have supplemental positions)

            When the filter is set to one Department counting should follow these rules.

                - The counts should only apply to positions within the selected department. This is an odd one because the roster will show a primary appointment in another department
                        but the counts should not include that primary appointment because it is not in the selected department.
                - After that the rules are the same as above.

            //
            // UPDATED Logic:
            //      1) NEVER COUNT 'rows' (parent or child) with ANY OPEN ACTION/Status  -> UPDATE 3: Count them as Pending!
            //      2) If we process Single vs. Multiple Department BOTH before (filter) and After (text search), we can post-process to decide whether to count secondary...Maybe?!?
            //          - If Single Department in Filters, NEVER count any other, regardless of Text Search
            //          - If
            //

            */
            var zRows = $('#wf-rooster-grid').DataTable().rows( {search:'applied'} ).data();

            // Special ZERO RESULTS UX:
            if(zRows.length == 0){$('#wf-pseudo-reporting').hide(); return false;}
            else{$('#wf-pseudo-reporting').show();}

            var api = $('#wf-rooster-grid').DataTable(),
                zDeps = currentWidget._getFilteredDepartments(),
                isSingleDept = (zDeps.length == 1) ? zDeps[0] : false,
                isMultiDeptsRawData = currentWidget._isMultiDepartmentsData(zRows),
                safeAddToArray = function(sVal, zArray){
                    if($.inArray(sVal, zArray) == -1){
                        zArray.push(sVal);
                    }
                    return zArray;
                },
                removeFromArray = function(sVal, zArray){
                    var iZ = $.inArray(sVal, zArray);
                    if(iZ != -1){
                        zArray = zArray.splice(iZ, 1);
                        zArray = removeFromArray(sVal, zArray);
                    }
                    return zArray;
                },
                compareDataForSameness = function(z1, z2){
                    if($this._lastCountedData === false){return false;}
                    if(zRows.length != $this._lastCountedData.length){return false;}
                    if(!_.isEqual(z1[0], z2[0])){return false;}
                    if(!_.isEqual(z1[z1.length-1], z2[z2.length-1])){return false;}
                    if($this._lastCountedDate !== null && Math.abs(new Date() - $this._lastCountedDate) < 500){return false;}
                    return true;
                },
                iDebug = false;

            //
            // Perf: Due to sticky headers & other options on DataTables, we get multiple triggers of DrawCallback().
            //       In order to not count the same thing ~3 times, we need to compare last results to current & bail if we think we have already counted the current set.
            //
            var bSame = compareDataForSameness(currentWidget._lastCountedData, zRows);
            if(bSame){
                $this._lastCountedData = zRows;
                $this._lastCountedDate = new Date();
                //console.log('BAIL!  Data seems to be the same, save some work...')
                return false;
            }
            else{
                //console.log(bSame, 'Looks like data is different:', ($this._lastCountedData === false) ? false : $this._lastCountedData.length, zRows.length);
            }
            $this._lastCountedData = zRows;
            $this._lastCountedDate = new Date();

            // For FE Debugging:d
            if(zRows.length < 10 && iDebug){console.log(zRows);}

            $('#wf-pseudo-reporting, #wf-roster-stats').hide();

            if(iDebug)console.log(
                'Debug: ', '# Detps Selected:', zDeps.length,
                'isSingleDept:', isSingleDept,
                'zDeps', zDeps,
                'isMultiDeptsRawData: ', isMultiDeptsRawData,
                'zRows len:', zRows.length,
                'zRows[0]:', zRows[0]
            );

            // Reset Counts:
            $this._vacantPrimaries = []; $this._vacantSecondaries = []; $this._vacantSupplementals = [];
            $this._reportPrimaries = []; $this._reportSecondaries = []; $this._reportSupplementals = [];
            $this._pendingPrimaries = []; $this._pendingSecondaries = []; $this._pendingSupplementals = [];

            for(i=0; i < zRows.length; i++){
                var row = zRows[i],
                    appt = row.z_row_appt;

                //if(iDebug)console.log(appt.department_code, appt);

                if( isSingleDept === false || (isSingleDept !== false && appt.department_descr == isSingleDept) ){  // If we have a single department selected, ignore all other department's positions/appointments....

                    var personGuid = appt.person_id,
                        bActions = (row.z_row_jact === false) ? false : true;

                    // VACANT FACULTY COUNT
                    if(personGuid == null){
                        // Appt has VACANCY
                        if(appt.metatrack_supplemental === true){safeAddToArray(appt.pcn, $this._vacantSupplementals);}
                        else if(appt.is_primary === true){safeAddToArray(appt.pcn, $this._vacantPrimaries);}
                        else{safeAddToArray(appt.pcn, $this._vacantSecondaries);}
                        if(bActions){
                            // Appt ALSO has PENDING
                            if(appt.metatrack_supplemental === true){safeAddToArray(appt.pcn, $this._pendingSupplementals);}
                            else if(appt.is_primary === true){safeAddToArray(appt.pcn, $this._pendingPrimaries);}
                            else{safeAddToArray(appt.pcn, $this._pendingSecondaries);}
                        }
                    }
                    else{
                        if(bActions){
                            // Appt is PENDING
                            if(appt.metatrack_supplemental === true){$this._pendingSupplementals.push(appt.pcn+'|'+appt.appointment_id)}
                            else if(appt.is_primary === true){$this._pendingPrimaries.push(appt.pcn+'|'+appt.appointment_id)}
                            else{$this._pendingSecondaries.push(appt.pcn+'|'+appt.appointment_id)}
                        }
                        else{
                            // Appt is FILLED
                            if(appt.metatrack_supplemental === true){
                                // ADD to Supplementals
                                $this._reportSupplementals = safeAddToArray(personGuid, $this._reportSupplementals);
                                $this._reportSecondaries = removeFromArray(personGuid, $this._reportSecondaries);
                                $this._reportPrimaries = removeFromArray(personGuid, $this._reportPrimaries);
                                if(i < 10 && iDebug)console.log('Added Supplemental:', personGuid, $this._reportPrimaries, $this._reportSecondaries, $this._reportSupplementals);
                            }
                            else if(appt.is_primary === true){
                                // ADD to Primaries, remove from Others
                                $this._reportPrimaries = safeAddToArray(personGuid, $this._reportPrimaries);
                                $this._reportSecondaries = removeFromArray(personGuid, $this._reportSecondaries);
                                $this._reportSupplementals = removeFromArray(personGuid, $this._reportSupplementals);
                                if(i < 10 && iDebug)console.log('Added Primary:', personGuid, $this._reportPrimaries, $this._reportSecondaries, $this._reportSupplementals);
                            }
                            else{
                                // ADD to Secondaries
                                $this._reportSecondaries = safeAddToArray(personGuid, $this._reportSecondaries);
                                if(i < 10 && iDebug)console.log('Added Secondary:', personGuid, $this._reportPrimaries, $this._reportSecondaries, $this._reportSupplementals);
                            }
                        }
                    }
                }
            };

            // Render Counts to UX:
            $('#wf-pseudo-reporting-primary span').text($this._reportPrimaries.length);
            $('#wf-pseudo-reporting-secondary span').text($this._reportSecondaries.length);
            $('#wf-pseudo-reporting-supplemental span').text($this._reportSupplementals.length);
            $('#wf-pseudo-reporting-total span').text($this._reportPrimaries.length);
            $('#wf-vacant-reporting-primary span').text($this._vacantPrimaries.length);
            $('#wf-vacant-reporting-secondary span').text($this._vacantSecondaries.length);
            $('#wf-vacant-reporting-supplemental span').text($this._vacantSupplementals.length);
            $('#wf-vacant-reporting-total span').text($this._vacantPrimaries.length);
            $('#wf-pending-reporting-primary span').text($this._pendingPrimaries.length);
            $('#wf-pending-reporting-secondary span').text($this._pendingSecondaries.length);
            $('#wf-pending-reporting-supplemental span').text($this._pendingSupplementals.length);
            $('#wf-pending-reporting-total span').text($this._pendingPrimaries.length);
            $('#wf-pseudo-reporting, #wf-roster-stats').show();

            if(i < 10 && iDebug)console.log('These were the rows:', zRows);

            $that._hideShowSubs();
            if(!$that._hasSubRows){$('#wf-summary-hidesubs').hide();}else{$('#wf-summary-hidesubs').show();}
            $that._hasSubRows = false;

            redrawResizeDataTable();
        },

        _hideShowSubs: function(){
            // NEW: Hide/Show Subrows integrated
            if(!$('#hideshowsubs').prop('checked')){ $('#wf-rooster-grid tbody tr:visible .subRow').hide(); }
            else{ $('#wf-rooster-grid tbody tr:visible .subRow').show(); }
        },

        _getFilteredDepartments: function(){
            return $('#fw-hf-departments').val();
        },

        _isMultiDepartmentsData: function(zA){
            // Takes an array of row data & fast-searches for whether there are multiple Appointment[0] Departments.
            var iL = zA.length,
                bM = zA[0].rawData.appointment_list[0].department_code;
            for(i=0;i<iL;i++){
                if(zA[i].rawData.appointment_list[0].department_code !== bM){
                    return false;
                }
                return true;
            }
        },

        _getCurrentRowIDs: function(){
            var $this = this,
                api = currentDT.oTbl,
                // rows = api.rows( {page:'current'} ).nodes(),
                rowData = api.rows({
                    order:  'current',  // 'current', 'applied', 'index',  'original'
                    page:   'all',      // 'all',     'current'
                    search: 'applied'   // 'none',    'applied', 'removed'
                }).data(),
                zIDs = [];

            for(i=0;i<rowData.length;i++){
                var sID = rowData[i].rawData.pcn;
                zIDs.push(sID);
            }
            return zIDs;
        },

        _selectAllFilters: function(){
            var $this = this,
                headerFilterSelects = $('#wf-rooster-grid thead th select'),
                headerFilterInputs = $('#wf-rooster-grid thead th input.wf-hf-input');

            headerFilterSelects.each(function(i, ob){
                $(ob).multipleSelect('checkAll');
            });
            headerFilterInputs.each(function(i, inp){
                $(inp).val('');
            });
            //$($.fn.dataTable.fnTables()[0]).dataTable().fnFilter('');
            //setTimeout(function(){currentDT.oTbl.search('').draw();}, 0);
            $this.filterRoster();
        },

        filterRoster: function(colIndex, api){
            var $this = this;
            // Get the Select Vals...
            headerFilterSelects = $('#wf-rooster-grid thead th select');
            //console.log('select 0s getSelects:', $(headerFilterSelects[0]).multipleSelect('getSelects'));
            headerFilterSelectVals = {
                departments: $('#wf-rooster-grid thead th select[data-prop=departments]').val(),
                tracks: $('#wf-rooster-grid thead th select[data-prop=tracks]').val(),
                titles: $('#wf-rooster-grid thead th select[data-prop=titles]').val(),
                tir: $('#wf-rooster-grid thead th select[data-prop=tir]').val(),
                actions:$('#wf-rooster-grid thead th select[data-prop=actions]').val(),
                statuses:$('#wf-rooster-grid thead th select[data-prop=statuses]').val()
            };
            headerFilterInputs = {
                pcns: $('#wf-rooster-grid thead th input[data-prop=pcns]').val(),
                names: $('#wf-rooster-grid thead th input[data-prop=names]').val(),
                proposedstart: $('#wf-rooster-grid thead th input[data-prop=proposedstart]').val(),
            };
            headerFilterDates = {
                lastupdated: [$('#wf-rooster-grid thead th select[data-prop=lastupdated]').val(), $('#wf-rooster-grid thead th input[data-prop=lastupdated]').val()]
            };

            $($.fn.dataTable.fnTables()[0]).dataTable().fnFilter('');
            // Filter will call itself with the above line...
        },

        _filterRosterCallback: function(settings, data, dataIndex, rowData){

            var zFilteredProps = [
                ['pcns', 'text'],
                ['departments', 'multipleSelect'],
                ['names', 'text'],
                ['tracks', 'multipleSelect'],
                ['titles', 'multipleSelect'],
                ['tir', 'special_tir'],
                ['actions', 'multipleSelect'],
                ['statuses', 'multipleSelect'],
                ['lastupdated', 'date'],
                ['proposedstart', 'text']
            ];

            for(var i=0; i < zFilteredProps.length; i++){
                var sProp = zFilteredProps[i][0],
                    sType = zFilteredProps[i][1],
                    cellData = (typeof rowData[sProp] != 'undefined') ? rowData[sProp] : false,
                    selVals = (typeof headerFilterSelectVals[sProp] != 'undefined') ? headerFilterSelectVals[sProp] : false,
                    textVal = (typeof headerFilterInputs[sProp] != 'undefined') ? headerFilterInputs[sProp] : false,
                    dateVals = (typeof headerFilterDates[sProp] != 'undefined') ? headerFilterDates : false;

                if(sType == "text"){ // Text Input
                    if(textVal.length > 1 && cellData.toLowerCase().indexOf(textVal.toLowerCase()) == -1){
                        return false;
                    }
                }
                else if(sType == "special_tir"){
                    // Used for TIR, maybe others in future...
                    if(dataIndex < 3 && iDebug){
                        console.log($.inArray('> 5 yrs', selVals), sProp, sType, cellData, selVals, textVal, rowData)
                    }

                    //
                    // NOTE: Must OR here with the Top vs Bottom areas of TIR filter
                    //

                    // Filled vs In Progress etc
                    if($.inArray(rowData.positions, selVals) < 0){
                        return false;
                    }

                    // Mapped >1, >2 etc to # months in position

                    var iTIR = (typeof rowData.tir_filter !== 'undefined' && rowData.tir_filter % 1 === 0) ? rowData.tir_filter : -1;
                    if(iTIR >= 60 && $.inArray('60+', selVals) < 0){return false;}
                    if(iTIR >= 48 && iTIR < 60 && $.inArray('48-60', selVals) < 0){return false;}
                    if(iTIR >= 36 && iTIR < 48 && $.inArray('36-48', selVals) < 0){return false;}
                    if(iTIR >= 24 && iTIR < 36 && $.inArray('24-36', selVals) < 0){return false;}
                    if(iTIR >= 12 && iTIR < 24 && $.inArray('12-24', selVals) < 0){return false;}
                    if(iTIR >= 0 && iTIR < 12 && $.inArray('0-12', selVals) < 0){return false;}
                }
                else if(sType == "date"){
                    var isBefore = dateVals[0] == 'before',
                        sDate = dateVals[1];

                    if(textVal.length > 1 && cellData.toLowerCase().indexOf(textVal.toLowerCase()) == -1){
                        return false;
                    }
                }
                else{ // multiSelect!!!
                    // Empty values in Actions & Statuses are OK if the Non box is checked...
                    if(cellData == ''){
                        if($.inArray('NONE', selVals) < 0 && $.inArray('None', selVals) < 0){
                            return false;
                        }
                    }
                    else{
                        // All Other Selects must have a matching value
                        if($.inArray(cellData, selVals) < 0){
                            // bReturn = false;
                            return false;
                        }
                    }
                    if(iDebug == 10 && iDebug){console.log(rowData)}
                }
            }

            // If all the columns matched past the loop, we allow the row:
            return true;

        },

        getFilters: function(){
            return this.filters;
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

                    // Create Table DOM; render dataTable
                    // $this._createDataTableHTML(data);
                    var munged = $this._flattenRosterRows(data.rows);

                    $this.data.rows = munged;
                    $this._createDataTable(munged);
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    console.log('AJAX Error:', jqXHR, textStatus, errorThrown);
                }
            });
        },

        _flattenRosterRows: function(rows){
            var flattenedRows = [],
                _makeRow = function(iRow, iApp, iAct){
                    var row = rows[iRow],
                        oApp = row.appointment_list[iApp],
                        isTIR = (typeof oApp.time_in_rank_display !== 'undefined'
                                    && typeof oApp.time_in_rank_months !== 'undefined'
                                    && oApp.time_in_rank_display.length > 0) ? true : false,
                        newRow = {
                            pcns: oApp.pcn,
                            names:(typeof oApp.display_name != 'undefined') ? oApp.display_name : 'Vacant',
                            tracks: oApp.track_descr,
                            titles: oApp.title_descr,
                            positions:oApp.status_descr,
                            actions: (iAct !== false && oApp.job_action_list.length > 0) ? oApp.job_action_list[iAct].job_action_type_descr : '',
                            statuses:(iAct !== false && oApp.job_action_list.length > 0) ? oApp.job_action_list[iAct].job_action_status : '',
                            departments: oApp.department_descr,
                            lastupdated: (iAct !== false && oApp.job_action_list.length > 0) ? oApp.job_action_list[iAct].job_action_updated : '',
                            proposedstart: (iAct !== false && oApp.job_action_list.length > 0) ? oApp.job_action_list[iAct].proposed_start_date : false,
                            tir:(isTIR) ? oApp.time_in_rank_display : oApp.status_descr,
                            tir_filter: (isTIR) ? oApp.time_in_rank_months : 0,
                            z_person_url: rows[iRow].appointment_list[iApp].person_url,
                            z_action_url: '',
                            z_act_id: false,
                            z_app_used: iApp,
                            z_act_used: iAct,
                            z_row_appt: rows[iRow].appointment_list[iApp],
                            z_row_jact: (iAct === false) ? false : rows[iRow].appointment_list[iApp].job_action_list[iAct],
                            rawData: rows[iRow] // RAW data for some newer features
                        };

                    // newRow.rawData.appointment = oApp;
                    if(iAct !== false){
                        // newRow.rawData.job_action = rows[iRow].appointment_list[iApp].job_action_list[iAct];
                        newRow.z_action_url = rows[iRow].appointment_list[iApp].job_action_list[iAct].job_action_url;
                        newRow.z_act_id = rows[iRow].appointment_list[iApp].job_action_list[iAct].job_action_id;
                    }

                    return newRow;
                };
            if($.each(rows, function(iRow, row){
                $.each(row.appointment_list, function(iAppointment, appointment){
                    //newRow.rawData.appointment = appointment;
                    if(appointment.job_action_list.length > 0){
                        $.each(appointment.job_action_list, function(iAction, action){
                            var tbdRow = _makeRow(iRow, iAppointment, iAction);
                            flattenedRows.push(tbdRow);
                        });
                    }
                    else{
                        var tbdRow = _makeRow(iRow, iAppointment, false);
                        flattenedRows.push(tbdRow);
                    }
                });
            })){
                return flattenedRows;
            };
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
            $stats.prependTo($wrapper);
            $filt.parent().css('float', 'left');
            $filt.parent().prependTo($wrapper);
            $info.prependTo($('#wf-stats-tr'));
            $leng.appendTo($bot).css('float', 'left');

            $this._dataTableInitd = true;

            $('.cv-table-loading').hide();

            // Little 'x' in Search to clear typing with one click
            var $label = $('#wf-rooster-grid_filter label:first'),
                $temp = $('<div></div>'),
                $input = $label.find('input:first').appendTo($temp);
                $cancel = $temp.append($('<span class="glyphicon glyphicon-remove-circle cancel_search"></span>'))
                $selectAll = $('<a href="#" id="wf-filter-select-all" style="padding-right:10px; margin-right:10px; border-right:solid 1px #999; font-weight:bold;">Select All</a>');

            $label.text('Search All:');
            $label.append($input);
            $label.append($cancel);
            $label.prepend($selectAll);

            $selectAll.on('click', function(e){
                $this._selectAllFilters();
            });

            $cancel.click(function(e){
                $input.val('');
                currentDT.oTbl.search('').draw();
            });

            return false;
        }

    });

    $(window).on('resize', function () {
        redrawResizeDataTable();
    });

    $(window).scroll(function() {
        clearTimeout($.data(this, 'scrollTimer'));
        _preventDoubleDropdowns();
        $.data(this, 'scrollTimer', setTimeout(function() {
            $('#wf-rooster-grid').DataTable().fixedHeader.adjust();
            _equalizeFixedHeaderWidths();
        }, 200));

    });

});

var currentDtFilters = null;
var currentDtShowAll = null;
var currentDtHasFild = false;
var currentDtPgName = 'roster';
var currentWidget = false;
var headerFilterSelects = false;
var headerFilterSelectVals = false;
var headerFilterInputs = false;
var headerFilterDates = false;
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
            //_equalizeFixedHeaderWidths();
            $('#wf-rooster-grid').DataTable().fixedHeader.adjust();
            _equalizeFixedHeaderWidths();
            _equalizeNestedRowHeights();
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
    _preventDoubleDropdowns();
}

function _preventDoubleDropdowns(){
    //console.log('_preventDoubleDropdowns')
    if($('.fixedHeader-floating .ms-drop:visible').length > 0){
        $('#wf-rooster-grid .ms-drop:visible').hide().css('position', 'fixed');
    }
    else{
        $('#wf-rooster-grid .ms-drop:visible').css('position', 'absolute');
    }
}

function _scrollTopFilter(){
    // Scrolls the Dropdown into view if it is not already in view...
    var oDrop = $('#wf-rooster-grid .ms-drop:visible');
    if(oDrop.length >= 0 && oDrop.position()){
        var odHeight = oDrop.height(),
            odOT = oDrop.offset().top,
            wst = $(window).scrollTop();
        if(odOT < wst){
            //scroll up
            $('html,body').animate({scrollTop:odOT}, 1000);
        }
        else if(odOT + odHeight > wst + (window.innerHeight || document.documentElement.clientHeight)){
            //scroll down
            $('html,body').animate({scrollTop:odOT - (window.innerHeight || document.documentElement.clientHeight) + odHeight + 40 }, 500);
        }
    }
}

function _equalizeNestedRowHeights(){
     // console.log('_equalizeNestedRowHeights...');
     // Experimental: equalize row div heights - might get SLOW on ~100 x N x 8 subrows?
     if(true){
        var zRows = $('#wf-rooster-grid tbody tr:visible');
        var zRows = $('#wf-rooster-grid tbody tr:visible'),
            lastRowPCN = false,
            lastStripe = false;

         $.each(zRows, function(ir, row){
            var $row = $(row), zCells = $row.find('td:visible'), maxH = 0;
            $.each(zCells, function(ic, cell){
                if(maxH < 40){
                    var iH = $(cell).find('div:first').css('height', 'auto').height();
                    if(iH > maxH){maxH = iH;}
                }
            });
            if(maxH == 40){ $.each(zCells, function(ic, cell){ $(cell).find('div:first').height(maxH) });}
            var $row = $(row),
                pcn = $row.find('td:first a, td:first span').text(),
                zTDs = $row.find('td');

            if(ir == 0){
                lastRowPCN = pcn;
                lastStripe = 'odd';
                $(zTDs[0]).removeClass('wf-seq-sub-null').find('*').show();
                $(zTDs[1]).removeClass('wf-seq-sub-null').find('*').show();
                $row.removeClass('even odd wf-seq-subrow').addClass(lastStripe);
            }
            else if(pcn == lastRowPCN){
                // SUBROW !!!
                $row.removeClass('even odd').addClass('wf-seq-subrow '+lastStripe);
                $(zTDs[0]).addClass('wf-seq-sub-null').find('*').hide();
                $(zTDs[1]).addClass('wf-seq-sub-null').find('*').hide();
            }
            else{
                // NOT a SubRow:
                $(zTDs[0]).removeClass('wf-seq-sub-null').find('*').show();
                $(zTDs[1]).removeClass('wf-seq-sub-null').find('*').show();
                lastRowPCN = pcn;
                lastStripe = (lastStripe == 'odd') ? 'even' : 'odd';
                $row.removeClass('even odd wf-seq-subrow').addClass(lastStripe);
            }

         });
     }
 }

var _rosterPrintHTML = '';
