// [Copyright]
// SmartPath v1.0
// Copyright 2014-2015 Mountain Pass Solutions, Inc.
// This unpublished material is proprietary to Mountain Pass Solutions, Inc.
// [End Copyright]

$(function() {
    $.widget( "wfApp.gridFilterBar", {
        // default options
        options: {
            data: false,
            gridWidget: false,
            summaryBar: false
        },

        filters: {},

        _create: function(){
            var $this = this,
                $filterDom = $this.element,
                zBuckets = $filterDom.find('.wf-filter-wrapper');

            // Init Summary Bars
            $this.options.summaryBar = $($filterDom.data('summaryBar'));

            // Init Buckets
            zBuckets.each(function(i, el){
                var $bucket = $(this);

                // Find the correct bit of data:
                var sProp = $bucket.data('searchProp');

                // Init Filter Bucket:
                $bucket.gridFilter({
                    gridFilterBar: $this.element,
                    summaryBar: $this.options.summaryBar,
                    data: $this.options.data[sProp],
                    filterGUID: sProp
                });
            });

            // Bind Filter button
            $filterDom.on('click', 'button#wf-filter', function(e){
                $this.filters = $this.getFilters();
                //console.log($this.filters);
                $($this.options.gridWidget).gridWidget('filterGrid');
                $this.toggleFilterBar('hide');
            });

            // Bind Chevron to Toggle UXs
            $('body').on('click', '.wf-filter-summary', function(e){
                //console.log($(e.target));
                if(!$(e.target).is('select, option')){
                    $this.toggleFilterBar();
                }
                else{
                    // Select All?
                }
            });

            $('body').on('change', '#wf-metatrack', function(e){
                // console.log('event here...')
                $('#wf-filter').trigger('click');
            });

            // Bind Select All
            $('body').on('click', '.wf-filters-select-all', function(e){
                var $chks = $filterDom.find('.wf-filter-title');
                $chks.each(function(i, el){
                    if($(this).prop('checked') !== true){
                        $(this).click();
                    }
                });
                //$('#wf-filter').trigger('click');
                $this.toggleFilterBar('show');
                $('#wf-metatrack').val('All');
                $filterDom.find('select').each(function(i,el){$(el).val($(el).find('option:first').val()).trigger('change');}); // Reset Time In Rank filter
                e.preventDefault();
                e.stopPropagation();
            });

            $('#wf-filter-cancel').click(function(e){
                $('#wf-filter-summary').find('.wf-roster-filter-toggle').click();
            });

            $('#wf-summary-hidesubs').on('click', 'label', function(e){
                var $chk = $(this).find('input');
                e.stopPropagation();
                if(!$('#hideshowsubs').prop('checked')){ $('#wf-rooster-grid tbody .subRow').hide(); }
                else{ $('#wf-rooster-grid tbody .subRow').show(); }
            });

        },

        registerFilter: function(){
            // For individual filter buckets to register selves with wrapper
        },

        getFilters: function(){
            var $widget = this,
                filters = {};
            //
            // Filters will either be a Bool:
            //      True: Show all
            //      False: Broken state...
            // OR a '|' delimited str of values to compare to.

            // Build the list of Filters (search-props)
            $widget.element.find('.wf-filter-wrapper').each(function(i,o){
                var $bucket = $(this),
                    sKey = $bucket.data('searchProp'),
                    $box = $bucket.find('.wf-filter-content');

                // Special Time In Rank:
                if(sKey == 'Time in Rank'){
                    filters['tir'] = $box.find('select').val();
                }
                else{
                    // For each Filter, either set True or create the delimited string of values
                    if( $(this).find('.wf-filter-title').prop('checked') ){
                        // All are checked, Set True
                        filters[sKey] = true;
                    }
                    else{
                        // Not All are Checked, create Values String
                        var zChks = $box.find('input:checked');
                        filters[sKey] = '|'
                        zChks.each(function(k, el){
                            filters[sKey] += $(el).val() + '|';
                        });
                    }
                }

            });

            // Dashboard: Selected MetaTrack is also a Filter...and kind of special
            filters.metatrack = true;
            if($widget.options.summaryBar.find('select').length > 0){
                var sval = $widget.options.summaryBar.find('select').val()
                filters.metatrack = '|'+sval+'|';
                if(sval == 'Promotions'){filters.metatrack += 'PROMOTION|'}
                if(sval == 'Appointments'){filters.metatrack += 'NEWAPPOINT|REAPPOINT|TRACKCHANGE|'}
                if(sval == 'Credentialing'){filters.metatrack += 'CREDENTIAL|'}
                if(sval == 'Enrollment'){filters.metatrack += 'ENROLL|'}
            }

            $widget.filters = filters;
            return filters;
        },

        toggleFilterBar: function(sOverwrite){
            var $this = this,
                chevy = $this.options.summaryBar.find('.glyphicon');

            if(sOverwrite === 'show'){
                $this.element.slideDown('fast', function(){$this._resetHeaders();}).toggleClass('wf-open-filters-body');
                chevy.addClass('glyphicon-chevron-up').removeClass('glyphicon-chevron-down');
            }
            else if(sOverwrite === 'hide'){
                $this.element.slideUp('fast', function(){$this._resetHeaders();$('#wf-rooster-grid').DataTable().fixedHeader.adjust();_equalizeFixedHeaderWidths();}).toggleClass('wf-open-filters-body');;
                chevy.addClass('glyphicon-chevron-down').removeClass('glyphicon-chevron-up');
            }
            else{
                $this.element.slideToggle('fast', function(){$this._resetHeaders();$('#wf-rooster-grid').DataTable().fixedHeader.adjust();_equalizeFixedHeaderWidths();}).toggleClass('wf-open-filters-body');;
                chevy.toggleClass('glyphicon-chevron-up glyphicon-chevron-down');
            }

            if($this.element.is(':visible')){
                $this.options.summaryBar.css({'border-bottom-radius':'0px !important'});
                $this.element.css({'border-top-radius':'0px !important'});
            }
            else{
                $this.options.summaryBar.css({'border-bottom-radius':'6px !important'});
                $this.element.css({'border-top-radius':'6px !important'});
            }
        },

        _resetHeaders: function(){
            _equalizeFixedHeaderWidths();
            $('#wf-rooster-grid').DataTable().fixedHeader.adjust();
            _equalizeFixedHeaderWidths();
        },

        getFilterValues: function(sCode){
            var $this = this,
                $selected = $this.element.find('[data-search-prop="'+sCode+'"] .wf-filter-content input:checked'),
                zSelected = [];

            $selected.each(function(i, el){
                zSelected.push([$(this).val(), $(this).data('code')]);
            });

            return zSelected;
        }

    });
});

$(function() {
    $.widget( "wfApp.gridFilter", {
        // default options
        options: {
            gridFilterBar: false,
            summaryBar: false,
            data: false,
            filterGUID: false,

            selectAll: true,
            summaryNone: false,
            summaryTrue: false,
            summaryNNN: false
        },

        _create: function(){
            var $this = this,
                $filter = $this.element;

            $this._renderBucket($this.options.filterGUID, $this.options.data);

            // Attempt to init with smarter text <-> selection language: NOTE: This results in strange usability when there are only a few things to do or only one active TBD:
            //      '  All Events| Anesthesiology Department| Instructional Track| Associate Professor without Tenure Title| All Action Types '  <- Seems Weird!
            //
            // Seems much better to see just one or several rows with similar departments and titles with the Filter bar saying:
            //      ' All Events| All Departments| All Tracks| All Titles| All Actions '
            //
            // However, if we ever want to do this at init/create, the following line of code does so:

            // $this._updateSummaryText($this.options.filterGUID);

        },

        updateSummary: function(){
            // Update the Summary Link text for one filter bucket
        },

        _renderBucket: function(guid, data){
            var $this = this,
                $bucket = $($this.options.gridFilterBar).find('[data-search-prop="'+guid+'"]'),
                sTitle = $this._getTitle(guid);

            // Time In Rank is special, there is no CheckBox or Bucket...
            // Generic Fix: take the html() of the definition & insert it instead of a bucket?
            if($bucket.hasClass('wf-filter-no-bucket')){
                var $html = $bucket.html();
                $bucket.empty().append('<label>'+sTitle+'</label><div class="wf-filter-content wf-filter-content-borderless"></div>').find('.wf-filter-content').append($html);
                $bucket.find('select').bind('change', function(e){
                    // Update Summary Bar
                    $this._updateSummaryText($bucket.data('searchProp'));
                });
                return true;
            }

            // Create & Bind Title chkBox:
            $bucket.append('<input type="checkbox" id="title_'+guid+'" class="wf-filter-title" checked/><label for="title_'+guid+'">'+sTitle+'</label><div class="wf-filter-content"></div>');
            $bucket.on('click', 'input.wf-filter-title', function(e){
                // Select or De-Select All children
                var bChkd =  $(this).prop('checked');
                $bucket.find('.wf-filter-content input').each(function(i,o){
                    $(this).prop('checked', bChkd);
                });

                // Update Summary Bar
                $this._updateSummaryText(guid);
            });

            // Create & Bind Inner ChkBoxes
            var $box = $bucket.find('.wf-filter-content:first');

            // Insert special 'None' options for a couple Filters:
            if(guid == 'actions' || guid == 'statuses'){
                $box.append( $('<input id="wff_'+guid+'_none" type="checkbox" checked value="None"/><label for="wff_'+guid+'_none">None</label>') );
            }

            // Render data-driven checkboxes:
            $.each(data,function(i,v){
                // Genericize data schema by grabbing properly named property for each type...
                var sVal = '',
                    sCod = '';
                switch(guid){
                    case 'positions':
                        sVal = v.status_descr;
                        break;
                    case 'primality':
                        sVal = v.descr;
                        break;
                    case 'tracks':
                        sVal = v.track_descr;
                        break;
                    case 'titles':
                        sVal = v.title_descr;
                        break;
                    case 'departments':
                        sVal = v.department_descr;
                        sCod = v.department_code;
                        break;
                    case 'actions':
                        sVal = v.job_action_type_descr;
                        break;
                    case 'statuses':
                        sVal = v.job_action_status;
                        break;
                    case 'events':
                        sVal = v.event_descr;
                        // sCod = v.event_code;
                        break;
                    default:
                        sVal = '';
                        break;
                }

                $box.append( $('<input id="wff_'+guid+'_'+i+'" type="checkbox" checked value="'+sVal+'" data-code="'+sCod+'"/><label for="wff_'+guid+'_'+i+'">'+sVal+'</label>') );

            });
            $box.on('click', 'input', function(e){
                // Toggle Title chkBox to false if uncheck
                if(!$(this).prop('checked')){
                    $bucket.find('input.wf-filter-title:first').prop('checked', false);
                }
                else{
                    if($box.find('input:not(:checked)').length == 0){
                        $bucket.find('input.wf-filter-title:first').prop('checked', true);
                    }
                }

                // Update Summary Bar
                $this._updateSummaryText($box.closest('.wf-filter-wrapper').data('searchProp'));
            });
        },

        _getTitle: function(guid){
            // Note: default will Capitalize, so only str != title need this...
            switch (guid){
                case ('primality'):
                    return 'Primary/Secondary';
                case ('actions'):
                    return 'Action Type';
                case ('statuses'):
                    return 'Status';
                default:
                    return guid.capitalize();
            }
        },

        _updateSummaryText: function(sProp){
            var $this = this,
                $bar = $this.options.summaryBar,
                $bucket = $($this.options.gridFilterBar).find('[data-search-prop="'+sProp+'"]'),
                $link = $bar.find('[data-search-prop="'+sProp+'"] a'),
                $box = $bucket.find('.wf-filter-content:first'),
                $zInputs = $box.find('input'),
                iTotal = $zInputs.length,
                $zChecked = $zInputs.filter(':checked'),
                iChecked = $zChecked.length,
                sFriendly = $this._getTitle(sProp);


            // Special Time In Rank
            if(sProp == "Time in Rank"){
                var $link = $bar.find('[data-search-prop="tir_filter"] a');
                // Strip ':...'
                var sTxt = $link.text(),
                    iPos = sTxt.indexOf(':'),
                    sSuf = $box.find('select option:selected').text(),
                    sNew = (iPos > 0) ? ( sTxt.substring(0, sTxt.indexOf(':')) + ': '+sSuf ) : sTxt+': '+sSuf;
                $link.text(sNew);
                return true;
            }

            // Figure out All, None, or NNN - and apply/remove Warnings
            if(iChecked != 0){
                $link.removeClass('warning');
            }
            if(iChecked == 0){
                // 0: '0 Foos'...and Turn Red?  Print 'Foos Required!'??  !!No results possible!! [as logic is now]
                $link.addClass('warning');
                $link.text(sFriendly.singularize() + ' Selection Required!').addClass('warning');
            }
            else if(iChecked == 1){
                // 1: 'Blah Foo(s), eg 'Clinical track', 'Clinical Lecturers', 'Cardiology Department', 'In-Progess Status', etc
                var foo = $zChecked.eq(0).next('label').text(),
                    str = sProp.capitalize();
                if(str.indexOf(sDeptLabel+'s') >=0 || str.indexOf('Tracks') >=0 || str.indexOf('Titles') >=0){
                    $link.text(foo + ' ' + str.singularize());
                }
                else{
                    $link.text(foo + ' ' + str.pluralize());
                }
            }
            else if(iChecked == iTotal){
                // All: 'All Foos', eg 'All Titles', 'All Departments'
                $link.text('All ' + sFriendly.pluralize());
            }
            else{
                // All> N > 1: 'N Foos Selected', eg '7 Departments Selected'
                $link.text(iChecked + ' ' + sFriendly.pluralize() + ' Selected');
            }
        }
    });
});