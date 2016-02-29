// [Copyright]
// SmartPath v1.0
// Copyright 2014-2015 Mountain Pass Solutions, Inc.
// This unpublished material is proprietary to Mountain Pass Solutions, Inc.
// [End Copyright]
var ov;
function findWithAttr(array, attr, value) {
    for(var i = 0; i < array.length; i += 1) {
        if(array[i][attr] === value) {
            return i;
        }
    }
    return false;
}
$(function() {
    $.widget( "wfWidgets.workFlowPage", {
        // default options
        options: {
            data: false,
            dataUrl: false,
            auth: false
        },

        itemWidgets: [],
        firstActionableItemDone: false,
        areCandidateViewNonOptionalsComplete: false,
        completedFLRRs: [],
        uxStates:{
            // closedContainers: [],
            currentDetailsView: false,
            lastActionType: false,
            forceDetailsView: false
        },
        _isInitialLoad: true,
        _successMsg: false,

        _create: function(){
            var $this = this,
                $element = $this.element;

            // AJAX call:
            $this._getData();

            // UX Bindings
            $this._bindings();

            // Hmmm.callbacks?
            _workflowWidget = $this;

            // Look for page reload via _create, load sub-item if present...
            if(window.location.hash != ''){
                $this.uxStates.pageLoadDetailView = window.location.hash;
            }

            $this.isCandidateView = $('body').hasClass('wf-candidate-view');
        },

        refreshWorkflowPage: function(data){
            var $this = this;

            // Handler for responses from AJAX Form Posts which contain full definition (Updated with changes) of the Workflow:

            // SAVE UX STATES we will return to after refresh/reload:

            // 0) Clear saved states:
            $this.uxStates.currentDetailsView = false;
            wfApp.usedGuids = [];

            // 1) LeftNav states: DEPRECATED (by newer Dials UXs)

            // 2) Open details pane state:
            if(!$this.isCandidateView){
                $this.uxStates.currentDetailsView = $('#wf-details-content-body .wf-itemWidgetWrapper:visible:first').data('code');
            }

            // WIPE Current UX & Add a Loading state:
            $this.element.empty().append($('<div id="wf-workflow-loading" class="cv-table-loading"><img src="'+imgPath+'ajax-loader.gif"/>Loading...</div>'));

            // We may need to go get data for Workflow now:
            if(typeof data.workflow == 'undefined'){
                // Generally, this is a response with either successMsg or redirect...
                if(typeof data.successMsg === 'string' && data.successMsg.length > 0){
                    $this._successMsg = data.successMsg;
                }
                else{
                    $this._successMsg = false;
                }
                $this._getData();
            }
            else{
                $this._renderWorkflow(data);
            }
        },

        _getFirstRelevantNavItemToShow: function(){
            // console.log('WTH, is this called twice?!?');
            var $this = this,
                returnString = false;

            // BUGBUG: Could be a Var for $this.uxStates.pageLoadDetailView.. Deal with that?
            //  NOTE: areCandidateViewNonOptionalsComplete <- available from load()...

            // Are there TBD FLRRs ?
            var zRevsReqd = $('.wf-overview-item-status-revs_reqd');
            if(zRevsReqd.length > 0){
                $.each(zRevsReqd, function(i,el){
                    var $el = $(el),
                        sLection = $el.find('a:first').data('section');

                    //console.log('sLection:', sLection, $this.completedFLRRs);
                    if(typeof sLection != 'undefined' && $.inArray(sLection, $this.completedFLRRs) == -1){
                        // Use This one!
                        //console.log('Found one to use:', sLection);
                        returnString = sLection;
                        return false;
                    }
                });
            }
            if(returnString !== false){return returnString;}

            // Are there TBD required items?
            //console.log('_getFirstRelevantNavItemToShow says areCandidateViewNonOptionalsComplete is', $this.areCandidateViewNonOptionalsComplete);
            if(!$this.areCandidateViewNonOptionalsComplete){
                // If there are no relevant Revs Reqd above, use first TBD item:
                var firstTBD = $('.wf-overview-col .wf-overview-item-status-tbd').filter(function(i,el){
                    var $item = $(el);
                    if($item.hasClass('wf-disclosure-parent')){ return false; } // Do not count group wrappers
                    if($item.find('a.wf-external-link').length > 0) { return false; } // Do Not count special External Links
                    return true;
                }).eq(0)[0];
                firstTBD = $(firstTBD);
                //console.log('firstTBD', firstTBD, typeof firstTBD, firstTBD[0], firstTBD.length);
                // OR this??: $('.wf-overview-item-wrap').has('.wf-overview-item-status-tbd')
                if(firstTBD.length > 0){
                    // Required Uploads in Candidate View need to show the item:
                    var upD = firstTBD.data('cvUpload');
                    if(typeof upD != 'undefined' && upD !== false){
                        var oItem = $('#'+upD);
                        //
                        // Crud: everything is written for a links... BUGBUG: Fix all this!
                        //
                        firstTBD.prepend('<a href="#" data-section="'+upD+'" class="starthidden" style="display:none!important;">&nbsp</a>');
                        $this._highlightCandidateNav(firstTBD);
                        return upD;
                    }
                    else{
                        returnString = firstTBD.find('a:first').data('section');
                    }

                }
                //console.log('returnString is at 2:', returnString);
                if(returnString !== false){return returnString;}
            }
            else{
                // if all things are complete, show Thank You...
                if($('#wf-thankyou-item').length > 0){
                    //console.log('Returning:', '#wf-thankyou-item')
                    returnString = '#wf-thankyou-item';
                }
                else{
                    // Safety: just show the first whatever?
                    console.log('Weird - hit safety here?')
                }
            }
            //console.log('returnString is at 3:', returnString);
            if(returnString !== false){return returnString;}

        },

        _forceSmartCandidateViewLocation: function(){
            var $this = this;

            // If the Candidate has FLRR, open any parent group wrapping it so it shows:
            var zRevsReqd = $('.wf-overview-item-status-revs_reqd');
            if(zRevsReqd.length > 0){
                $.each(zRevsReqd, function(i,el){
                    var $el = $(el);
                    if($el.hasClass('wf-disclosure-child')){
                        var $wrapper = $el.closest('.wf-disclosure-wrapper'),
                            $group = $el.prev('.wf-disclosure-child');
                        if(!$group.hasClass('wf-disclosure-open')){
                            $this._toggleDisclosureSection($wrapper, true);
                        }
                    }
                });
            }

            var bestGuess = $this._getFirstRelevantNavItemToShow();
            //console.log('_forceSmartCandidateViewLocation bestGuess is', bestGuess)
            if(window.location.hash === '' && typeof bestGuess != 'undefined'){
                window.location.hash = bestGuess;
                //console.log('using _getFirstRelevantNavItemToShow', bestGuess);
                $this._showSectionById(bestGuess);
                $this._highlightCandidateNav($('a[data-section="'+bestGuess+'"]'));
            }
            else{
                // console.log('Here 3...');
                $this._showSectionById(window.location.hash);
                $this._highlightCandidateNav($('a[data-section="'+window.location.hash.substring(1)+'"]'));
            }

        },


        _getData: function(){
            var $this = this;
            $.ajax({
                url: $this.options.dataURL,
                type: 'POST',
                success: function(data, textStatus, xhr) {
                    if(wfApp._sessionExpiryLogoutRequired(data)){return false;} // Just in case we get a Success response redirect to the Login form
                    $this._renderWorkflow(data);
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    console.log('AJAX Error:', jqXHR, textStatus, errorThrown);
                }
            });
        },

        _renderWorkflow: function(data){
            var $this = this;

            $this.options.data = data;
            $this.options.auth = data.auth;

            // TBD: respond to set uxStates from reloads...
            // a) remove Loading...
            // b) activate Details view

            // Once we have the context data, we need to render various UXs with it:
            $this._insertStatus();
            $this._insertTOC();
            $this._renderDetails();
            $this._iterateData();
            $this.$content.append($this.$wf_details);
            $this._insertContactInfo();

            // New subPage buttons need to reload their PARENT, not Overview or themselves:
            if($this.uxStates.forceDetailsView !== false){
                $this._showSectionById($this.uxStates.forceDetailsView);
                $this.uxStates.forceDetailsView = false;
            }

            // NOTE: Multiple File uploads stay on page, Singles go to Overview... All else to Overview?
            else if($this.uxStates.currentDetailsView){
                // If Multiple Uploads, return to Details
                // If File Delete, return to Details
                // Else return to Overview...
                var $section = $('.wf-itemWidgetWrapper[data-code='+$this.uxStates.currentDetailsView+']:first'),
                    isMultipleUpload = $section.find('form:first').hasClass('wf-upload-multiple');

                if(isMultipleUpload || $this.uxStates.lastActionType !== false){
                    if($this.uxStates.currentDetailsView !== false){$this._showSectionById($this.uxStates.currentDetailsView);}
                    $this.uxStates.lastActionType = false;
                }
            }

            // Expose Revisions Required if in that state
            if($this.options.data.job_action.revisions_required === true){
                $('#wf-revisions-required-title, #wf-revisions-required-note').removeClass('starthidden').show();
            }

            // Expose Historical Information if Historical Appt.
            if($this.options.data.historicalIndicatorStatus.length > 0){
                $('#wf-historical-action-note, #wf-historical-appt-title').removeClass('starthidden').show();
            }

            $('.wf-loading-msg').remove();
            $('#wf-workflow-loading, .wf-workflow-loading').hide();
            $('#wf-modal-backdrop').hide().addClass('starthidden');

            // Show UX success message if present
            if(!$this._isInitialLoad && $this._successMsg){
                //var sMsg = (typeof data.status != 'undefined') ? data.status : 'Your changes were saved.';
                cvApp.hideHeaderMessage($this._successMsg);
            }

            $('.wf-disclosure-parent .wf-item-after').show();   // New Disclosure Items should show chevron always

            $('#wf-workflow-loading, .wf-workflow-loading').hide();

            $this._isInitialLoad = false;

            // Optional messages need better floating in DOM (but get inserted afterwards)
            $this.element.find('.wf-overview-col-first .wf-item-optional').each(function(i, oO){
                $(oO).prependTo($(oO).parent());
            });

            $('#wf-workflow-loading-inner').hide();

            $this.element.trigger('fixPaneHeights');

            // Candidate View Specials
            if($this.isCandidateView){
                // Candidate View gets special LeftNav treatment for multiple Workflows
                $this._insertCandidateViewParents();

                // Candidate View also might have a FLRR we should highlight...
                $this._forceSmartCandidateViewLocation();

                $this._moveSubsequentCandidateCols();

                return true;
            }

            // New generic F5 with #ID support
            if(typeof $this.uxStates.pageLoadDetailView != 'undefined' && $this.uxStates.pageLoadDetailView != '' && $this.uxStates.pageLoadDetailView !== false && $this.uxStates.pageLoadDetailView != '#overview'){
                //console.log('This line...1');
                $this._showSectionById($this.uxStates.pageLoadDetailView);
            }

        },

        _moveSubsequentCandidateCols: function(){
            var $secondaries = $('.wf-overview-col').not(':first'),
                $last = $('.wf-overview-col:first .wf-overview-section:last');

            $.each($secondaries, function(i,o){
                var $o = $(o),
                    $sections = $o.find('.wf-overview-section');
                $sections.insertAfter($last);
                $o.remove();
            });
        },

        _insertCandidateViewParents: function(){
            // Thjis is to render Container/Section names in the Candidate LeftNav instead of the Dials non-candidate uses.
            // Parent links go Above until after the current item...
            var $this = this,
                containers = $this.options.data.leftNavWorkflows,
                openOneDone = false,
                oLast = false;

            for(var i = (containers.length - 1); i >= 0; i--){
                // var perComplete = (dial.denominator > 0) ? Math.floor(dial.numerator / dial.denominator * 100) : 0,
                var container = containers[i],
                    perComplete = Math.floor(container.numerator / container.denominator * 100) + '%',
                    bOpen = (window.location.pathname.indexOf(container.workflow_url) >= 0) ? true : false,
                    sGlyph = (!bOpen) ? '<a href="'+container.workflow_url+'" class="wf-dial-btn btn btn-sm btn-default"><span class="glyphicon glyphicon-chevron-right"></span></a>' : '',
                    oLink = $('<div class="wf-candidate-parent">'+sGlyph+'<a href="'+container.workflow_url+'" class="'+((bOpen) ? 'active' : '')+'">'+container.title+' Items ('+ perComplete +')</a></div>');
                if(bOpen){openOneDone = true;}
                var $col = $('.wf-overview-col:first');
                if(openOneDone){
                    $col.prepend(oLink);
                }
                else{
                    oLink.attr('style', 'margin-bottom:10px;');
                    if(oLast !== false){oLink.insertBefore(oLast);}
                    else{$col.append(oLink);}
                }
                oLast = oLink;
            };
        },

        _insertStatus: function(){
            var $this = this,
                data = $this.options.data,
                tmpl = $('#wf-workflow-template-status').html(),
                pName = data.person.full_name || false;

            // Candidate View always Closed, otherwise per Cookie for preference/last
            data.viewState = (!$this.isCandidateView && $.cookie('wf-header') != 'closed') ? 'wf-workflow-status-open' : 'wf-workflow-status-closed';
            data.viewStateIcon = (($.cookie('wf-header') != 'closed')?'up':'down');

            if($this.isCandidateView){
                data.nullablePersonLink = (pName !== false) ? ': <span>'+data.person.full_name+'</span>': '';
                data.positionLink = '<span>#'+data.position.pcn+'';
            }
            else{
                data.nullablePersonLink = (pName !== false) ? ': <a href="'+data.person.url+'" target="_blank">'+data.person.full_name+'</a>': '';
                data.positionLink = '<a href="'+data.position.url+'" target="_blank">#'+data.position.pcn+'</a>';
            }
            data.uniqname = (typeof data.person != 'undefined' && typeof data.person.username != 'undefined' && data.person.username.length > 0) ? '('+data.person.username+')' : '';

            // These links depend on permissions of logged in user from server...
            data.hideCancelLink = (data.canCancelJobAction === true) ? false : true;
            data.hideResendLink = (data.canResendEmail === true) ? false : true;
            data.hideFacultyLink = (typeof data.person.id === 'undefined') ? true : false;

            // Start Date:
            var isDate = (data.job_action.proposed_start_date != ""),
                sEnter = '<span class="glyphicon glyphicon-calendar" aria-hidden="true"></span>Set Proposed Start Date';

            data.startDatePrefix = isDate ? ' Proposed Start Date: &nbsp;' : '';
            data.hideProposedStartDate = (data.show_proposed_start) ? false : true;
            data.proposedStartDate = (isDate) ? '<span class="glyphicon glyphicon-calendar" aria-hidden="true"></span>' + data.job_action.proposed_start_date : sEnter;
            var sWarn = (data.job_action.countdown_warning === true) ? ' wf-startdate-warn' : '';
            data.daysRemaining = (isDate && typeof data.job_action.countdown_days != 'undefined' && data.job_action.countdown_days != null) ? ('&nbsp; | &nbsp;<span class="wf-startdate-count '+sWarn+'">Submit Within '+data.job_action.countdown_days + ' Days</span>' ) : '';

            // Push content...
            var sCls =  (data.viewState == 'wf-workflow-status-open') ? ' wf-toc-short' : '';
            $this.$content = $('<div class="wf-details-page-content clearfix '+sCls+'"></div>');
            $this.element.append($this.$content);
            $this.$content.prepend($(wfApp.wfTemplate(tmpl, data)));
        },

        _insertTOC: function(){
            var $this = this,
                data = $this.options.data,
                tmpl = $('#wf-workflow-template-leftnav').html();

            data.viewState = (($.cookie('wf-header') != 'closed')?'wf-details-toc-short':'wf-details-toc-tall');
            var $wrap = $(wfApp.wfTemplate(tmpl, data));

            $this.$toc = $wrap.find('#wf-details-toc-body');
            $this.$content.append($wrap);
            $this._renderLeftNav($wrap);
        },

        _renderDetails: function(){
            var $this = this,
                tmpl = ($this.isCandidateView) ? $('#wf-workflow-details-candidate').html(): $('#wf-workflow-details').html(),
                $data = $this.options.data,
                rrTxt = ($data.job_action.revisions_required === true) ? $data.revisions_required_comment.activity +' by ' + $data.revisions_required_comment.username + ' at ' + $data.revisions_required_comment.created : '',
                rrNote = '';

            $this.options.data.revReqdTxt = rrTxt;
            $this.options.data.revReqdNotes = $data.revisions_required_comment.comment;
            $this.$wf_details = $(wfApp.wfTemplate(tmpl, $this.options.data));
            $this.$details_body = $this.$wf_details.find('#wf-details-content-body');
        },

        _insertContactInfo: function(){
            var $this = this,
                data = $this.options.data,
                tmpl = $('#wf-workflow-contact-information').html(),
                $wrap = $(wfApp.wfTemplate(tmpl, data));

            $this.$wf_details.find('#wf-details-content-body').append($wrap);
        },

        _iCol: 0,
        _insertOverviewColumn: function(container){
            console.log(container);
            var $this = this;
            var containers = $this.options.data.leftNavWorkflows;
            var overviewTEST = {
                'container':{
                    'title': false,
                    'header':container.common.header,
                    'status':container.ppStatus,
                    'desc':container.common.descr,
                    'sections':[

                    ]
                }
            };
            for(var ci = 0; ci < containers.length; ci++)
            {
                var conter = containers[ci];
                if(!overviewTEST.container.title)
                {
                    if(window.location.pathname.indexOf(conter.workflow_url) >= 0)
                    {
                        overviewTEST.container.title = conter.title + " Items";
                        overviewTEST.container.percentage = Math.floor((conter.numerator / conter.denominator) * 100);
                    }
                }
            }
            $.each(container.sections, function(index, value){
                var section = {
                    'title': value.common.descr,
                    'items': [
                    ]
                };
                $.each(value.items, function(index, value){
                    var item = {
                        'title': value.common.descr,
                        'code': value.common.code,
                        'class_name': value.common.class_name,
                        'status': value.ppStatus,
                        'guid': value.common.guid,
                        'config': value.config,
                        'data': value.data,
                        'blocked': value.common.is_blocked,
                        'disclosureGroup': value.config.disclosureGroup ? {'title':value.config.disclosureGroup.descr, 'code':value.config.disclosureGroup.code} : false
                    };
                    section.items.push(item);
                });
                overviewTEST.container.sections.push(section);
            });
            var priorities = [
                '',
                'blocked',
                'complete',
                'pending',
                'tbd',
                'rev_req'
            ];
            var totalItems = 0;
            $.each(overviewTEST.container.sections, function(index, section){
                section.disclosureGroups = [];
                $.each(section.items, function(index, item){
                    if(item.disclosureGroup)
                    {
                        if(findWithAttr(section.disclosureGroups,'title',item.disclosureGroup.title) === false)
                        {
                            section.disclosureGroups.push({
                                'title':item.disclosureGroup.title,
                                'subitems':[item],
                                'status':''
                            });
                        }
                        else
                        {
                            var ind  = findWithAttr(section.disclosureGroups,'title',item.disclosureGroup.title);
                            section.disclosureGroups[ind].subitems.push(item);
                            section.disclosureGroups[ind].status = priorities.indexOf(item.status) > priorities.indexOf(section.disclosureGroups[ind].status) ? item.status : section.disclosureGroups[ind].status;
                        }

                    }
                });
                $.each(section.disclosureGroups, function(index, dgroup){
                    var indexOfFirstItem = findWithAttr(section.items, 'title', dgroup.subitems[0].title);
                    section.items.splice(indexOfFirstItem, dgroup.subitems.length, dgroup);
                });
                $.each(section.items, function(){
                    totalItems += 1;
                    console.count('totalItems');
                });
            });
            overviewTEST.container.widths = 100 / totalItems;
            var canViewNavTmpl = $("#canview-bottom-nav-tmpl").html();
            ov = wfApp.wfTemplate(canViewNavTmpl, overviewTEST.container);
            var container_tmpl = $('#wf-workflow-overview-col').html(),
                container_vals = {
                    title: container.common.descr,
                    sections: false
                },
                section_tmpl = $('#wf-workflow-overview-col-section').html(),
                section_vals = {
                    title: false,
                    items: false
                },
                item_tmpl_link = $('#wf-workflow-overview-col-section-item-link').html(),
                item_tmpl_span = $('#wf-workflow-overview-col-section-item-span').html(),
                item_tmpl_btn = $('#wf-workflow-overview-col-section-item-button').html(),                              // Not Currently used, this is for making certain Approve/Submit type items Buttons in the Overview
                item_tmpl_singleFileUpload = $('#wf-workflow-overview-col-section-singlefile-upload').html(),
                item_tmpl_singleFileDownload = $('#wf-workflow-overview-col-section-singlefile-download').html(),
                sSections = '',
                sItems = '',
                isCandidateView = $this.isCandidateView,
                item_vals = {
                    title: false,
                    pre_icon: false,
                    post_icon: false,
                    guid: false
                };

            var oNewNav = $('<div class="sf-new-nav"></div>');

            $this.areCandidateViewNonOptionalsComplete = true;

            container_vals.bordered = ($this._iCol == 1) ? 'wf-col-bordered' : '';

            $.each(container.sections, function(iS,section){
                sItems = '';
                lastDisclosure = false;
                var oNewNavUl = $('<ul class="new-nav-ul"></ul>');
                $.each(section.items, function(iI,item){
                    var complete = '<span class="glyphicon glyphicon-ok wf-item-before"></span>',
                        blocked = '<span class="glyphicon glyphicon-ban-circle wf-item-before"></span>',
                        tbd = '<span class="glyphicon glyphicon-plus wf-item-before"></span>',
                        pending = '<span class="glyphicon glyphicon-time wf-item-before"></span>',
                        rev_req = '<span class="glyphicon glyphicon-warning-sign wf-item-before"></span>',
                        status = (item.ppStatus == 'blocked') ? blocked : (item.ppStatus == 'complete') ? complete : (item.ppStatus == 'pending') ? pending : (item.ppStatus == 'tbd') ? tbd : rev_req,
                        isDisclosure = (typeof item.config.disclosureGroup != 'undefined') ? item.config.disclosureGroup.code : false;

                    var oNewNavLi = $('<li class="new-nav-li"></li>');

                    item_vals.title = item.common.descr;
                    item_vals.pre_icon = status;
                    // OLD: item_vals.post_icon = item.common.optional === false ? item.ppStatus == 'pending' && item.common.class_name !== 'PacketDownload' ? '<span class="wf-item-pending">(pending...)</span>' : '' + item.common.class_name !== 'PacketDownload' ? '<span class="wf-item-after">*</span>' : '' : '';
                    // NEW: Optional gray italic to right of ONLY !complete && TBD && !item-status items:
                    item_vals.post_icon = item.common.optional === false ? (item.ppStatus == 'pending' && item.common.class_name !== 'PacketDownload') ? '<span class="wf-item-pending">(pending...)</span>' : '' + item.common.class_name !== 'PacketDownload' ? '<span class="wf-item-after"></span>' : '' : (item.common.is_complete === false && item.ppStatus == 'tbd' && item.common.class_name !== 'PacketDownload') ? '<span class="wf-item-optional">Optional</span>' : '';
                    item.common.guid = wfApp._createUniqueID(item.common.code);
                    item_vals.guid = item.common.guid;
                    item_vals.status = item.ppStatus;
                    item_vals.daSectionParent = section.common.code;
                    item_vals.extraClasses = '';
                    item_vals.wrapperExtraClasses ='';
                    item_vals.childDisclosure = '';

                    // New: Disclosure Groups (eg CBC)
                    if(lastDisclosure != isDisclosure || isDisclosure === false){ // <- Have Begun or Ended a disclosure section
                        if(lastDisclosure !== false){ sItems += '</div>' } // <- Ended a disclosure section:
                        lastDisclosure = isDisclosure; // <- Set current disclosure
                        if( isDisclosure !== false ){ // <- Open a disclosure wrapper:
                            if(item.ppStatus == 'pending'){item_vals.pre_icon = pending;}
                            // BUGBUG: WRapper should show Orange with RevReqd state!
                            var isThisGroupRevReqd = false,
                                thisDGCode = item.config.disclosureGroup.code;
                            $.each(section.items, function(ii, i2){ if( typeof i2.config.disclosureGroup != 'undefined' && i2.config.disclosureGroup.code == thisDGCode && (i2.common.field_revisions_required === true || i2.common.revisions_required === true)){ isThisGroupRevReqd = true; }});

                            sItems += '<div class="wf-disclosure-wrapper '+((isThisGroupRevReqd) ? 'wf-disclosure-wrapper-revreqd':'')+'"><div class="wf-overview-item-wrap wf-overview-item-status-'+item.ppStatus+' wf-disclosure-parent" data-disclosure-parent="'+item.config.disclosureGroup.code+'">'+item_vals.pre_icon+'<a class="wf-overview-link-title">'+item.config.disclosureGroup.descr+'</a><span class="wf-item-after wf-item-after-clickable glyphicon glyphicon-chevron-'+((item.ppStatus != 'tbd') ? 'down':'up')+'"></span></div>';
                        }
                    }
                    if(isDisclosure !== false){ // <- Disclosure Child Item states
                        item_vals.childDisclosure = 'data-disclosure-child="'+item.config.disclosureGroup.code+'"';
                        item_vals.wrapperExtraClasses += 'wf-disclosure-child';
                    }

                    // Special Single File Upload Download Btn
                    var isSingleFileUpload = false,
                        isSingleFileDownload = false,
                        isPacketDownload = false;

                    // Single File Uploads with File already present
                    if(item.common.class_name === 'FileUpload'
                        && item.config.min === '1' && item.config.max === '1'
                        && (typeof item.data.sequence_list[0].current.file_name != 'undefined' && item.data.sequence_list[0].current.file_name.length > 0)
                        && item.common.is_blocked === false){
                            isSingleFileDownload = true;
                            item_vals.extraClasses += 'wf-upload-has-edit';
                            item_vals.post_icon = '<a class="wf-details-dl-link" href="#" data-section="'+item.common.guid+'" data-breadcrumb="'+item.common.descr+'"><span class="glyphicon glyphicon-cog"></span>edit</a>';
                            item_vals.daDlLink = item.data.sequence_list[0].current.download_url || '';
                    }
                    // Single File Uploads with No File Uploaded
                    else if(item.common.class_name === 'FileUpload'
                        && item.config.min === '1' && item.config.max === '1'
                        && (typeof item.data.sequence_list[0].current.file_name == 'undefined')
                        && item.data.disabled === false && item.common.is_blocked === false){
                        // Form for immediate upload from link, take 1:
                        isSingleFileUpload = true;
                        item_vals.uploadURL = item.data.sequence_list[0].upload_url;
                        item_vals.daGuid = item.common.guid;
                        item_vals.site = $this.options.data.auth.site;
                        item_vals.mpsid = $this.options.data.auth.mpsid;
                        item_vals.appCode = $this.options.data.auth.appCode;
                        item_vals.xsrf = $this.options.data.auth._xsrf;
                        //console.log(item);
                    }

                    // Multiple-File Uploads: Special Multi-File (X/Y) UX:
                    if(item.common.class_name === 'FileUpload'
                        && typeof item.config.min != 'undefined' && item.config.min > 0
                        && typeof item.config.max != 'undefined' && item.config.max > 1
                        ){
                        var iCurrent = 0;
                        $.each(item.data.sequence_list, function(iS, sequence){
                            var iCL = sequence.current.file_name || false;
                            if(iCL){iCurrent++;}
                        });
                        item_vals.post_icon = '<span class="wf-complete-count">('+iCurrent+' / '+item.config.max+')</span>';
                    }

                    // Special PacketDownload States:
                    if(item.common.class_name === 'PacketDownload' && item.data.disabled === false){
                        item_vals.pre_icon = '<span class="glyphicon glyphicon-download-alt wf-item-before"></span>';
                        item_vals.status = 'packet';
                        item_vals.daDlLink = item.data.url.replace('/packet/', '/packet/download/') || '';
                        isPacketDownload = true;
                    }

                    // Special Approve & Completion Buttons:
                    //  NOTE: Not Currently used, this is for making certain Approve/Submit type items Buttons in the Overview
                    var isButton = false;
                    if((item.common.class_name === 'Approval' || item.common.class_name === 'Completion' || item.common.class_name === 'Submit')
                        && item.common.is_complete === false && item.data.disabled === false && item.common.view_details === true && item.common.is_blocked === false){
                        isButton = true;
                    }
                    var tmpl_to_use = (isButton) ? item_tmpl_link : ((item.common.view_details === true) ? item_tmpl_link : item_tmpl_span);

                    // Template selection:
                    if(isPacketDownload){tmpl_to_use = item_tmpl_singleFileDownload;}
                    if(isSingleFileUpload){tmpl_to_use = item_tmpl_singleFileUpload;}
                    if(isSingleFileDownload){
                        tmpl_to_use = item_tmpl_singleFileDownload;
                    }

                    if(item.common.class_name === 'Approval' && typeof item.data.approvalStatus != 'undefined' && item.data.approvalStatus == 'DENY'){
                        item_vals.pre_icon = '<span class="glyphicon glyphicon-remove wf-item-before wf-approval-denied"></span>';
                        item_vals.title += ' (Denied)';
                        item_vals.wrapperExtraClasses += ' notheavy';
                        item_vals.tooltip = 'title="This approval was Denied. The history of the denial and any comments submitted with it are available in the item\'s Details by clicking this link."';
                    }

                    // Special Academic Evaluations (X/Y) in title:
                    if(item.common.class_name === 'Evaluations'){
                        item_vals.post_icon = '<span class="wf-complete-count">('+item.data.nbr_complete+'/'+item.data.nbr_required+')</span>';
                    }

                    sItems += wfApp.wfTemplate(tmpl_to_use, item_vals);

                    // Special Candidate View Complete Detection
                    if(isCandidateView && item.common.is_complete !== true && item.common.optional !== true){
                        $this.areCandidateViewNonOptionalsComplete = false;
                    }


                    if(isCandidateView){
                        // New Candidate View NavBar?
                        oNewNavLi.append($(wfApp.wfTemplate(tmpl_to_use, item_vals)));
                        oNewNavUl.append(oNewNavLi);
                    }

                });

                section_vals.items = sItems;
                section_vals.title = section.common.descr;
                sSections += wfApp.wfTemplate(section_tmpl, section_vals);

                //if(isCandidateView){ oNewNav.append(oNewNavUl); }

            });
            $this._iCol++;
            container_vals.sections = sSections;

            var sout = wfApp.wfTemplate(container_tmpl, container_vals);

            if(isCandidateView){
                //$("body").append(oNewNav);
            }

            return sout;
        },

        _renderLeftNav: function(toc){
            var $this = this,
                dials = $this.options.data.leftNavWorkflows,
                tmpl_enabled = $('#wf-workflow-knob-template-enabled').html(),
                tmpl_readonly = $('#wf-workflow-knob-template-readonly').html(),
                sout = '';

            $('#wf-overview-link').remove();

            // NOT Candidate View...Dials:
            $.each(dials, function(prop, dial){
                var oDial = {},
                    rawPerc = (dial.numerator / dial.denominator) * 100,
                    isSelected = dial.selected,
                    isLink = dial.workflow_url.length > 0;
                oDial.dialColor = (rawPerc == 100) ? '#6db26d' : (rawPerc > 25) ? '#6699cc' : '#6699cc';
                oDial.dialPercent = Math.floor(rawPerc) + '%';
                oDial.dialTitle = dial.title;
                oDial.dialSubtitle = dial.numerator + ' of ' + dial.denominator;
                oDial.dialStatus = dial.status_descr;
                oDial.dialUrl = dial.workflow_url;
                oDial.dialHighlight = (isSelected) ? 'wf-nav-highlight' : '';

                var tmpl_to_use = (isLink) ? tmpl_enabled : tmpl_readonly,
                    sD = wfApp.wfTemplate(tmpl_to_use, oDial),
                    sSep = ( (!isSelected && prop == dials.length-1) || !isSelected && prop < dials.length-1 && dials[prop+1].selected == false) ? '<hr class="wf-dial-border"/>' : '';

                sout += sD + sSep;

            });

            $this.$toc.append($(sout));

            $this.$toc.find('.dial').each(function () {
                var elm = $(this);
                var color = elm.attr("data-fgColor");
                var perc = elm.attr("value");

                elm.knob({
                    value: 0,
                    min: 0,
                    max: 100,
                    // skin: "tron",
                    readOnly: true,
                    thickness: .125,
                    dynamicDraw: true,
                    displayInput: false,
                    displayPrevious: true,
                    bgColor: '#ddd'
                });

                elm.hide();

                setTimeout(function(){
                    elm.fadeIn();
                    $({value: 0}).animate({
                        value: perc
                        }, {
                            duration: 1000,
                            easing: 'swing',
                            progress: function() {
                                elm.val(Math.ceil(this.value)).trigger('change');
                            }
                    });
                }, 250);

                //circular progress bar color
                $(this).append(function() {
                    var $par = elm.parent().parent(),
                        $content = $par.find('.circular-bar-content'),
                        $label = $content.find('.circular-bar-content label')
                    $content.css('color', color);
                    $label.text('asdf'); // wth?
                });

            });
        },

        _iterateData: function(){
            var $this = this,
                data = $this.options.data;

            // New & Important: we have one centralized status munger for the front end (extra iteration on all, but WFs are not that large...)
            $this._preProcessData();

            if(data.workflow.container.length == 0){
                var oErr = $('<div class="wf-overview-col clearfix  wf-overview-col-first" style="width:263px !important;"><div class="wf-overview-section"><div class="wf-overview-item-wrap wf-overview-item-status-complete"><span class="wf-overview-link-title"></span></div></div></div>');
                $this.$wf_details.find('#wf-details-content-body').append(oErr);
                return false;
            }

            $.each(data.workflow.container, function(iC,container){
                // Newer:
                var $sec = $($this._insertOverviewColumn(container));
                if(iC == 0){$sec.find('div:first').parent().addClass('wf-overview-col-first');}
                $this._renderSmartDisclosureIcon($sec);
                $this.$wf_details.find('#wf-overview-item').append($sec);

                $.each(container.sections, function(iS,section){
                    $.each(section.items, function(iI,item){
                        // We need tied GUID - should be set already from above:
                        //console.log('_iterateData()...')
                        var $guid = item.common.guid,
                            stype = 'wf-item-type-'+item.common.class_name,
                            $wrapper = $('<div id="'+$guid+'" class="wf-itemWidgetWrapper '+stype+' clearfix" data-code="'+$guid+'" data-breadcrumbone="'+item.common.descr+'"></div>');
                        // Appends to DOM
                        $this.$details_body.append($wrapper);
                        $this._renderItem(item, $wrapper, $guid);
                    });
                });
            });

            // Finally, add the Activity Area
            var $activitiesBody = $this._activityBody(data.workflow.activity_log);
            $this.$wf_details.find('#wf-details-content-body').append($activitiesBody);
            $this.$toc.append($('<a href="#" class="wf-details-toc-top" data-section="ActivityLog"><span class="glyphicon glyphicon-list-alt"></span>Activity Log ('+data.workflow.activity_log.length+')</a>'));
        },

        _preProcessData: function(){
            //
            // This iterator processes data for a few different UX statuses & some business logic:
            //
            var $this = this,
                data = $this.options.data,
                isRevReqd = data.job_action.revisions_required || data.job_action.field_revisions_required,
                has1stRRSubmitPassed = false;

            $.each(data.workflow.container, function(iC,container){
                var ppContainerReqdTBDs = 0,
                    ppContainerHasOpts = false,
                    ppContainerComplete = true,
                    ppContainerRevsReqd = false;
                $.each(container.sections, function(iS,section){
                    var ppSectionStarted = false,
                        ppSectionComplete = true,
                        ppSectionRevReqd = false;
                    $.each(section.items, function(iI,item){
                        // Set Item Status:
                        item.ppStatus = (isRevReqd === true && (item.common.revisions_required === true || item.common.field_revisions_required === true)) ? 'revs_reqd' :
                                    (item.common.is_complete === true) ? 'complete' :
                                    (item.common.is_complete === false && item.data.disabled === true && item.common.is_blocked === false) ? 'pending' :
                                    (item.common.is_complete === false && item.data.disabled === false && item.common.is_blocked === false ) ? 'tbd' :
                                    'blocked';
                        // Prep Section & Container Statuses:
                        if(item.ppStatus === 'complete'){
                            ppSectionStarted = true;
                        }
                        if(item.common.optional === false && item.ppStatus !== 'complete'){
                            ppSectionComplete = false;
                            ppContainerComplete = false;
                            ppContainerReqdTBDs++;
                        }
                        if(item.ppStatus === 'revs_reqd'){
                            ppSectionRevReqd = true;
                            ppContainerRevsReqd = true;
                            if(!has1stRRSubmitPassed && item.common.class_name == 'Submit'){
                                has1stRRSubmitPassed = true;
                            }
                        }
                        if(item.common.optional === true && item.common.is_complete == false && item.common.class_name != 'PacketDownload'){
                            ppContainerHasOpts = true;
                        }
                        // console.log('Item ', item.common.descr, ' is ', item.ppStatus);
                    });
                    // Set Overall Section Status:
                    section.ppStatus = (ppSectionRevReqd) ? 'revs_reqd' :
                                        (ppSectionComplete) ? 'complete' :
                                         (ppSectionStarted) ? 'started' :
                                         'unstarted';
                    // console.log('Section ', section.common.descr, ' is ' , section.ppStatus);
                });
                // Set Container statuses:
                container.ppStatus = (ppContainerRevsReqd) ? 'revs_reqd' :
                                     (ppContainerComplete) ? 'complete' : 'incomplete';
                container.ppTbdCount = ppContainerReqdTBDs;
                container.ppContainerHasOpts = ppContainerHasOpts;

                // console.log('Container ', container.common.descr, ' is ' , container.ppStatus, ' with ',  ppContainerReqdTBDs, ' incompleteReqs ', ((ppContainerHasOpts)?'+':''));
            });
        },

        // AKA Audit Log:
        _activityBody: function(activities){
            var tplWrap = $('#wf-workflow-template-activities').html(),
                tplLog = $('#wf-workflow-template-activity-logs').html(),
                tplComm = $('#wf-workflow-template-activity-comments').html(),
                sFinal = '',
                sLogs = '';

            $.each(activities, function(iA, activity){
                // Insert BRs?
                $.each(activity.comments, function(i,comm){
                    comm.comment = wfApp.replaceLineBreaks(comm.comment);
                    comm.daHide = ''
                });
                // Check for empty & insert stub
                if(activity.comments.length == 0){
                    activity.comments = [{
                        comment: '',
                        comment_code: '',
                        daHide: 'startinvisible wf-size-0'
                    }]
                }
                else{

                }
                var commentString = '';
                $.each(activity.comments, function(index, comment){
                    commentString += wfApp.wfTemplate(tplComm, comment);
                });
                var vals = {
                    comments: commentString,
                    datestamp: activity.created,
                    user: activity.username,
                    action: activity.activity
                }
                sLogs += wfApp.wfTemplate(tplLog, vals);
            });
            sFinal = wfApp.wfTemplate(tplWrap, {logs: sLogs});
            return $(sFinal);

        },

        _renderItem: function(current_item, $wrapper, $guid){
            var $this = this,
                $item = false,
                jOpts = {
                    item: current_item,
                    auth: $this.options.auth
                };

            // Add a state for isFirstActionableItem to each
            current_item.common.isFirstActionableItem = false;
            if(!$this.firstActionableItemDone && current_item.common.is_blocked === false && current_item.common.is_complete === false){
                current_item.common.isFirstActionableItem = true;
                $this.firstActionableItemDone = true;
            }

            // Mark Single vs Multiple Upload widgets
            if(current_item.common.class_name == "FileUpload" && current_item.data.sequence_list.length < 2 && current_item.common.is_complete == true){
                current_item.common.isCompleteSingleUpload = true;
            }

            // Render a Widget
            switch(current_item.common.class_name){
                case 'FileUpload':
                    $item = $wrapper.fileUploadWidget(jOpts);
                    break;
                case 'PacketDownload':
                    $item = $wrapper.serverSideAjaxForm(jOpts);
                    break;
                case 'Submit':
                    $wrapper.serverSideAjaxForm(jOpts);
                    break;
                case 'SubmitBackgroundCheck':
                    $wrapper.serverSideAjaxForm(jOpts);
                    break;
                case 'Approval':
                    $wrapper.serverSideAjaxForm(jOpts);
                    break;
                case 'Completion':
                    $wrapper.serverSideAjaxForm(jOpts);
                    break;
                case 'Placeholder':
                    $wrapper.serverSideAjaxForm(jOpts);
                    break;
                case 'IdentifyCandidate':
                    $wrapper.serverSideAjaxForm(jOpts);
                    break;
                case 'QA':
                    $wrapper.serverSideAjaxForm(jOpts);
                    break;
                case 'Evaluations':
                    $wrapper.serverSideAjaxForm(jOpts);
                    break;
                case 'ConfirmTitle':
                    $wrapper.serverSideAjaxForm(jOpts);
                    break;
                case 'JobPosting':
                    $wrapper.serverSideAjaxForm(jOpts);
                    break;
                case 'Attest':
                    $wrapper.serverSideAjaxForm(jOpts);
                    break;
                case 'NPI':
                    $wrapper.serverSideAjaxForm(jOpts);
                    break;
                case 'Disclosure':
                    $wrapper.serverSideAjaxForm(jOpts);
                    break;
                case 'PersonalInfoSummary':
                    $wrapper.serverSideAjaxForm(jOpts);
                    break;
                case 'BackgroundCheck':
                    $wrapper.serverSideAjaxForm(jOpts);
                    break;
                case 'UberForm':
                    $wrapper.serverSideAjaxForm(jOpts);
                    break;
                case 'ItemInjector':
                    $wrapper.serverSideAjaxForm(jOpts);
                    break;
                case 'JointPromotion':
                    $wrapper.serverSideAjaxForm(jOpts);
                    break;
                case 'ServiceAndRank':
                    $wrapper.serverSideAjaxForm(jOpts);
                    break;

                default:
                    console.log('Uh Oh - we have an unrecognized Item Type we are trying to render...');
                    break;
            }
            $this.itemWidgets.push($item);
            return $item;
        },

        _showOverview: function(e){
            var $this = this,
                $over = $('#wf-overview-item').removeClass('show');

            window.location.hash = '#overview';

            // Potential bug in open subPages: delete any dangling states for reloads:
            $this.uxStates.currentDetailsView = false;
            $this.uxStates.forceDetailsView = false;

            // Exception for subForms (eg Evals)
            if($('#wf-breadcrumb-one a').length > 0 && $('#wf-breadcrumb-one .stitle').length > 0 && !$(e.target).hasClass('overview-breadcrumb')){
                $('#wf-breadcrumb-one a:first').click();
                return false;
            }

            $('#wf-breadcrumb-one').hide();
            if(!$over.is(':visible')){
                $('.wf-itemWidgetWrapper').hide();
                $over.show('slide', {direction: 'left'}, 500);
            }
            else{
                $('.wf-itemWidgetWrapper').hide();
                $over.fadeIn();
            }

            // Smart Handle Breadcrumbs:
            $this._writeBreadcrumbs($over);

            $("html, body").animate({ scrollTop: -140 }, "slow");

            // if(!mpsApp._isCandidateView) checkFlrrStatus();
            $('#workflow-content').data('wfWidgets-workFlowPage')._maybeInsertFlrrButton();

            $this.element.trigger('fixPaneHeights');

        },

        _showSectionView: function(section, $link){
            if($link.is('a')){$link.attr('href', '#'+section)}
            // setTimeout(function(){window.location.hash = section;}, 0);

            var $this = this,
                $target = $('#'+section),
                $over = $('#wf-overview-item').removeClass('show'),
                sCrumbTxt = (typeof $link != 'undefined' && typeof $link.data('breadcrumb') != 'undefined') ?  $link.data('breadcrumb') : $link.text();

            $('.wf-itemWidgetWrapper').hide();
            if($this.isCandidateView){
                $target.show();
            }
            else{
                $target.show();
            }
            $target.trigger('_showItemWidget');

            // Candidate View developed into something else, DOM munge for now:
            if($this.isCandidateView){
                $over.addClass('show').show();
                var $wrap = $link.closest('.wf-overview-item-wrap');
                $this._highlightCandidateNav($link);
            }

            $this._writeBreadcrumbs($target);
            $("html, body").animate({ scrollTop: -140 }, "slow");

            // if(!mpsApp._isCandidateView) checkFlrrStatus();
            $this._maybeInsertFlrrButton();

            $this.element.trigger('fixPaneHeights');
        },

        _showSectionById: function(sID, pushHashToURL, over){
            var bHashPush = pushHashToURL || false;
            window.location.hash = '';

            //console.log('_showSectionById:', sID, ' <-- Look for # or not?')

            $this = this;
            // BUGBUG!!!  undefined is still causing issues on Candidate Loads with no FLRR???
            if(typeof sID == 'undefined'){
                // console.log('and... $this._getFirstRelevantNavItemToShow():', $this._getFirstRelevantNavItemToShow());
                sID = $this._getFirstRelevantNavItemToShow();
            }
            var sID = (sID.indexOf('#') == -1) ? '#'+sID : sID,
                $target = $(sID);
                //$target = ($('.wf-itemWidgetWrapper[data-code='+sID+']:first').length > 0) ? $('.wf-itemWidgetWrapper[data-code='+sID+']:first') : (sID.indexOf('#') >= 0) ? $(sID) : false;

            var $over = $('#wf-overview-item').removeClass('show'),
                sCrumbTxt = $target.find('.wf-header-title:first').text().replace(':','');

            $('.wf-itemWidgetWrapper').hide();
            //$target.show('slide', {direction: 'up'}, 500);
            $target.show();
            $target.trigger('_showItemWidget');

            // Candidate View developed into something else, DOM munge for now:
            if($this.isCandidateView){
                $over.addClass('show').show();
                var $link = $('#wf-overview-item').find('a[data-section="'+sID+'"]');
                //console.log('yo:', $link)
                $this._highlightCandidateNav($link);
            }

            $this._writeBreadcrumbs($target);
            $("html, body").animate({ scrollTop: -140 }, "slow");

            sID = (sID.indexOf('#') >= 0) ? sID : '#'+sID;
            if(bHashPush && sID != window.location.hash){
                window.location.hash = sID;
            }

            // if(!mpsApp._isCandidateView) checkFlrrStatus();
            $this._maybeInsertFlrrButton();

            $this.element.trigger('fixPaneHeights');
        },

        _writeBreadcrumbs: function($wrapper){
            var $this = this,
                sOne = (typeof $wrapper.data('breadcrumbone') != 'undefined') ? $wrapper.data('breadcrumbone') : false,
                sTwo = (typeof $wrapper.data('breadcrumbtwo') != 'undefined') ? $wrapper.data('breadcrumbtwo') : false,
                $bcZero = $('#wf-details-titlebar-breadcrumbs #wf-breadcrumb-zero'),
                $bcOne = $('#wf-details-titlebar-breadcrumbs #wf-breadcrumb-one'),
                $bcTwo = $('#wf-details-titlebar-breadcrumbs #wf-breadcrumb-two');

            $bcZero.remove();

            if(!sOne && !sTwo){
                // Overview:
                $bcOne.hide();
                $bcTwo.hide();
            }
            else if(sTwo){
                // Show a SUB page BC:
                var s1 = $bcOne.find('.stitle').text();
                $bcOne.show().find('.stitle').remove();
                $bcOne.append($('<a href="#" class="stitle" data-section="'+$bcOne.data('code')+'">'+s1+'</a>'));
                $bcTwo.show().find('.stitle').text(sTwo);
            }
            else{
                // Set Previous CrumbOne code:
                $bcOne.data('code', $wrapper.data('code'));
                // Show just ONE breadcrumb
                $bcOne.find('.stitle').remove();
                $bcOne.show().append($('<span class="stitle">'+sOne+'</span>'));
                $bcTwo.hide();
            }

            // Special Candidate View: Nested disclosureGroup Breadcrumbing
            if($this.isCandidateView){
                var $wrap = $('.wf-can-view-lite').closest('.wf-disclosure-wrapper');
                if($wrap.length > 0){
                    var $title = $wrap.find('.wf-disclosure-parent .wf-overview-link-title'),
                        $bcZero = $bcOne.clone().attr('id', 'wf-breadcrumb-zero');
                    $bcZero.insertBefore($bcOne).show().find('.stitle').text($title.text());
                }
            }

        },

        _scrollTop: function(){
            // Scroll up if Nav too long...
            $('html, body').animate({
                scrollTop: 0-140                // BUGBUG: Should be dynamic heights of chrome 7 workflow header?
            }, 50);
        },

        _toggleDisclosureSection: function($wrapper, forceOpen){
            //console.log('_toggleDisclosureSection:', $wrapper, forceOpen)
            var $this = this,
                $title = $wrapper.find('.wf-disclosure-parent'),
                $children = $wrapper.find('.wf-disclosure-child'),
                bForceShow = forceOpen || false;
            if(bForceShow){
                $children.show();
                $title.addClass('wf-disclosure-open');
                $title.find('.wf-item-after').addClass('glyphicon-chevron-up').removeClass('glyphicon-chevron-down');
            }
            else{
                $children.toggle();
                $title.toggleClass('wf-disclosure-open');
                $title.find('.wf-item-after').toggleClass('glyphicon-chevron-down glyphicon-chevron-up');
            }

        },

        _highlightCandidateNav: function($link){
            //console.log('_highlightCandidateNav:', $link);
            var $this = this;
            if($this.isCandidateView){
                //console.log('highlight says:',$link.is('.wf-overview-item-wrap'))
                var $wrap = ($link.is('.wf-overview-item-wrap')) ? $link : $link.closest('.wf-overview-item-wrap');
                $('.wf-overview-item-wrap').removeClass('wf-can-view-lite');
                $wrap.addClass('wf-can-view-lite');

                // It is possible this is a child in a closed group, open it if so...
                if(!$wrap.closest('.wf-disclosure-wrapper').find('.wf-disclosure-parent').hasClass('wf-disclosure-open')){
                    $this._toggleDisclosureSection($wrap.closest('.wf-disclosure-wrapper'), true);
                }
            }
        },

        _renderSmartDisclosureIcon: function($sec){
            var $this = this, zDscs = $sec.find('.wf-disclosure-wrapper');
            $.each(zDscs, function(iD, dg){
                var $dg = $(dg), zTems = $dg.find('.wf-disclosure-child'),
                    zBlocked = zTems.filter('.wf-overview-item-status-blocked'), zTBD = zTems.filter('.wf-overview-item-status-tbd'), zDun = zTems.filter('.wf-overview-item-status-complete'), zPend = zTems.filter('.wf-overview-item-status-pending'),
                    $pLink = $dg.find('.wf-disclosure-parent'), $pIcon = $pLink.find('.wf-item-before'),
                    _resetClasses = function(sNot, sIcon){
                        zTems.hide();
                        $pLink.removeClass('wf-overview-item-status-complete wf-overview-item-status-blocked wf-overview-item-status-tbd').addClass(sNot);
                        $pIcon.removeClass('glyphicon-ban-circle glyphicon-plus glyphicon-ok').addClass(sIcon);
                    };
                if(zDun.length == zTems.length){_resetClasses('wf-overview-item-status-complete', 'glyphicon-ok');} // Mark parent COMPLETE:
                else if(zTBD.length > 0){_resetClasses('wf-overview-item-status-tbd', 'glyphicon-plus'); zTems.show();}// Mark parent TBD & show children
                else if(zPend.length > 0){_resetClasses('wf-overview-item-status-pending', 'glyphicon-time');}// Mark parent TBD
                else{_resetClasses('wf-overview-item-status-blocked', 'glyphicon-ban-circle');}// Mark parent BLOCKED
            });
        },

        _bindings: function(){
            var $this = this;

            $('body').on('click', '#wf-overview-item .wf-overview-item-wrap a, .overview-breadcrumb, .wf-details-form-btn-bar a, .wf-contact-info, a.stitle', function(e){

                var $link = $(this),
                    starget = $link.data('section'),
                    $target = $('#'+starget),
                    $itemWrap = $link.closest('.wf-overview-item-wrap');

                // Exempt External & Download Packet links
                if($link.hasClass('wf-external-link') || $link.parent().hasClass('wf-overview-item-status-packet')){
                    // e.preventDefault();
                    // e.stopPropagation();
                    return true;
                }

                // New: Disclosure Groups
                if(typeof $itemWrap.data('disclosureParent') != 'undefined'){
                    $this._toggleDisclosureSection($itemWrap.parent());
                    return false;
                }

                // Download in new Tab/Window link:
                if($link.hasClass('wf-details-dl-link') && $link.data('section').length < 1){
                    e.preventDefault();
                    e.stopPropagation();
                    window.open($link.attr('href'));
                    return true;
                }
                // Print (or other) links in command bar should sometimes not close item or link to others:
                // BUGBUG: Deprecate?
                if($link.hasClass('wf-do-not-overview-link')){
                    e.stopPropagation();
                    return true;
                }


                // All Others...
                $('#wf-overview-item').removeClass('show');
                if($target.length <= 0 || starget == 'wf-overview-item'){
                    $this._showOverview(e);
                }
                else{
                    $this._showSectionView(starget, $link);
                }

                // Scroll up if Nav too long...
                $('html, body').animate({
                    scrollTop: 0-140
                }, 50);

                return true;

            });

            $('body').on('click', '#wf-details-toc a', function(e){
                var $link = $(this);

                if($link.hasClass('section-title')){
                    $link.parent().find('.sections').toggle();
                    $link.find('.glyphicon').toggleClass('glyphicon-chevron-up glyphicon-chevron-down');
                    // $this._showOverview();
                }

                if($link.data('section') === 'wf-overview-item'){$this._showOverview();}
                if($link.data('section') === 'ActivityLog'){$this._showSectionView('ActivityLog', $link);}
                if($link.data('section') === 'WFContactInformation'){$this._showSectionView('WFContactInformation', $link);}

            });

            $('body').on('click', '.wf-accordion-title .tab-toggler', function(e){
                var $this = $(this),
                    $titlebar = $this.closest('.wf-accordion-title'),
                    $container = $titlebar.next('.wf-accordion-content');

                    $this.toggleClass('glyphicon-chevron-down glyphicon-chevron-up');
                    $container.slideToggle();
            });

            $('body').on('change', '.wf-single-file-upload-overview-form input:file', function(e){
                var $input = $(e.target).closest('form').find('input[type=file]'),
                    label = $input.val().replace(/\\/g, '/').replace(/.*\//, '');
                    $input.trigger('fileselect', [label]);
                    e.stopPropagation();
            });
            $('body').on('fileselect', '.wf-single-file-upload-overview-form input:file', function(event, label) {
                var $target = $(event.target),
                    $form = $target.closest('form');

                // Asynchronous IFrame POST:
                $form.submit();
                $('#wf-modal-backdrop').show().removeClass('starthidden');
                cvApp.showHeaderMessage('Uploading file...', 'info', true);
                event.stopPropagation();
            });

            $('body').on('click', '.wf-toggle-trigger', function(e){
                var $trigger = $(this),
                    sToggle = $trigger.find('.glyphicon').data('toggleClasses'),
                    $parent = $trigger.closest('.wf-toggle-parent'),
                    $target = $parent.find('.wf-toggle-target'),
                    $text = $trigger.find('.wf-rr-text'),
                    sNextText = $trigger.data('toggleText'),
                    sCurrent = $trigger.text();

                    if($target.is(':visible')){
                        $trigger.css({float:'left'}).find('.glyphicon').toggleClass(sToggle);
                    }
                    else{
                        $trigger.css({float:'left'}).find('.glyphicon').toggleClass(sToggle);
                    }
                    $trigger.data('toggleText', sCurrent);
                    $text.text(sNextText)
                    $target.toggle();
                    e.preventDefault();
                    e.stopPropagation();
            });

            $('body').on('click', '.wf-rr-toggle', function(e){
                var $el = $(this),
                    $icon = $el.find('.glyphicon'),
                    sToggleClasses = $icon.data('toggleClasses'),
                    sNewText = $el.data('toggleText'),
                    sOldText = $el.find('.wf-rr-text').text();
                $el.parent().find('.wf-rr-target').toggle();
                $icon.toggleClass(sToggleClasses);
                $el.data('toggleText', sOldText).find('.wf-rr-text').text(sNewText);
                e.preventDefault();
                e.stopPropagation();
            });

            $('body').on('click', '#wf-workflow-status h4 .toggler', function(e){
                var $el = $(this)
                    $header = $el.closest('#wf-workflow-status'),
                    $glyph = $el.find('.glyphicon'),
                    $toc = $('#wf-details-toc'),
                    $tocParent = $toc.parent();
                $header.toggleClass('wf-workflow-status-open wf-workflow-status-closed');
                if($header.hasClass('wf-workflow-status-open')){
                    $tocParent.addClass('wf-toc-short');
                }
                else{
                    $tocParent.removeClass('wf-toc-short');
                }
                $glyph.toggleClass('glyphicon-chevron-up glyphicon-chevron-down');
                $toc.toggleClass('wf-details-toc-short wf-details-toc-tall');
                // View Prefs:
                $.cookie('wf-header', (($header.hasClass('wf-workflow-status-open')) ? 'open' : 'closed'), { expires: 365, path: '/' });

                $this.element.trigger('fixPaneHeights');
            });

            $('body').on('click', '.wf-item-after-clickable', function(e){
                $(this).closest('.wf-overview-item-wrap').find('.wf-overview-link-title').click();
            });

            //
            // STart Date One-Offs
            //
            $('body').on('click', '.wf-start-date-save',  function(e){
                $(this).closest('form').trigger('submit');
            });
            $('body').on('click', '.wf-start-date-link', function(e){
                var $link = $(this);
                    $read = $link.closest('.wf-status-start-date').find('.wf-start-date-read'),
                    $form = $read.siblings('.wf-start-date-enter'),
                    $dp = $form.find('.mps-date-picker');

                if($form.find('.mps-date-picker-wrapper').length == 0){
                    $dp.mpsDatePicker();
                    $('<a href="#" class="input-group-addon btn btn-default wf-start-date-save" alt="Save proposed start date" title="Save proposed start date"><span class="glyphicon glyphicon-floppy-disk"></span></a>').insertAfter($dp);
                }
                $read.toggle();
                $form.toggle();
            });
            $('body').on('submit', '.wf-start-date-form', function(event){
                var $form = $(this);
                var sURL = $form.attr('action');
                cvApp.ubiquitousPageRequest({
                    url: sURL,
                    data: JSON.stringify($form.serializeObject()),
                    errorMessage: '#modalerrormessage'
                });
                return false;
            });

            //
            // New Field Level Revisions Required work includes a generic-ish itemJSON load event on Forms/Templates that delivers extra JSON with a template via AJAX:
            //
            $('body').on('itemLoadJSON', function(event, JSON){
                console.log('Trigger for itemLoadJSON(event, JSON) fired with data: ', JSON);
            });

            $('body').on('fixPaneHeights', function(e){
                // Slightly Kludge-y JS Layout fix for Candidate View as we have an abs-ps'd leftNav that might or might not be taller than content area.
                window.setTimeout(function(){               // Timeout is to let the items complete rendering (slides, animations, etc)
                    var $TOC = $('#wf-details-toc'),
                        iTOC = $TOC.height(),
                        $Content = $('#wf-details-content'),
                        iContent = $Content.height();
                    if( iContent < iTOC + $TOC.offset().top                             // Content too short
                        || $('#workflow-content').height() > iTOC + $TOC.offset().top   // Right too long from prev load
                    ){
                        $('#workflow-content').height(iTOC + $('#wf-workflow-status').height());
                    }
                },0);
            });
        },

        _maybeInsertFlrrButton: function(areFlrr){
            var $this = this;
            if ($this.isCandidateView){return false;}

            // console.log('_maybeInsertFlrrButton got called with: ', areFlrr);

            // Make an ajax call to see if this user & workflow has FLRR pending, so the button should show...
            var sP = window.location.pathname,
			    sId = sP.substring(sP.lastIndexOf('/')),
			    sPath = '/appt/jobaction/revisionsavailable' + sId;

            $.ajax({
				url: sPath,
				type: 'POST',
				dataType: 'json'
			})
			.done(function(data, textStatus, jqXHR){
                if(data.revisionsAvailable === true){
                    var sId = window.location.pathname.substring(sP.lastIndexOf('/')),
                        $titleBar = $('#wf-details-titlebar'),
                        $flrrBtn = $('<a href="/appt/jobaction/revisionsnotification'+sId+'" class="btn btn-sm btn-warning wf-flrr-notify-btn" style="float:right; position:relative; top:2px; font-weight:bold;">Submit Pending Revisions Required...</a>');
                    $titleBar.find('.wf-flrr-notify-btn').remove();
                    $titleBar.prepend($flrrBtn);
                }else{
                    $('#wf-details-titlebar wf-flrr-notify-btn').remove();
                }
            })
            .fail(function( jqXHR, textStatus, errorThrown ){
                // Errors Exist:
                console.log('AJAX post received error response.', jqXHR);
            });

        }
    });
});
