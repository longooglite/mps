// [Copyright]
// SmartPath v1.0
// Copyright 2014-2015 Mountain Pass Solutions, Inc.
// This unpublished material is proprietary to Mountain Pass Solutions, Inc.
// [End Copyright]

$(function() {
    $.widget( "wfWidgets.fileUploadWidget", $.wfWidgets.itemWidget, {
        options: {
            item: false,
            auth: false
        },

        _create: function(){
            var $this = this,
                $element = $this.element;

            uxDebug('fileUploadWidget:', $this.options.item);

            // New: Common Config States for each Widget Instance (for non-selector based OO code later)
            $this.states = {};
            $this.states = $this.options.item.common;
            uxDebug('fileUploadWidget states:', $this.states);

            // Make HTML -> jQ obj:
            $this.$form = $($this._renderUploadControls());

            // LOGIC HERE: This is where to do Disable, Hide/Show, etc on the above obj...

            // Global Disable safety.  BUGBUG: server side forms should also either not render things or add disabled to tags?
            if($this.options.item.data.disabled === true){
                $this.$form.find('input, textarea, button, select').attr('disabled', 'disabled');
                $this.$form.find('.btn-primary').addClass('btn-default').removeClass('btn-primary');
            }

            // RENDER:
            $this.element.append($this.$form);

            $this._bindings();

            // $this.setWidgetToAjaxFormInterfaces();

            // console.log($element);

            // return $this._super();

            // Workaround for File Upload errors - any UploadWidget will do...
            _uploadWidget = $this;
        },

        getCommonHeader: function(){
            var $this = this,
                min = $this.options.item.config.min,
                max = $this.options.item.config.max,
                isSingle = ($this.options.item.data.sequence_list.length < 2) ? true : false,
                sTxt = (isSingle) ? '': (min+' required');
            return this._super(this.states, sTxt);
        },

        _renderUploadControls: function(){
            var $this = this,
                tplItem = $('#wf-workflow-widget-upload-file').html(),
                tplSumm = $('#wf-workflow-upload-file-summary').html(),
                tplHist = $('#wf-workflow-upload-file-history').html(),
                sContent = '',
                isSingle = ($this.options.item.data.sequence_list.length < 2) ? true : false,
                auth = $this.options.auth;

            $this.getCommonHeader();

            $.each($this.options.item.data.sequence_list, function(i, sequence){
                var isSummary = (typeof sequence.current.file_name != 'undefined') ? true : false,
                    summaryOpts = {},
                    bFile = (typeof sequence.current.lastuser != 'undefined'),
                    iHistoryCount = sequence.versions.length + ((bFile) ? 1 : 0);

                $.each(sequence.versions, function(iV, version){
                    version.daVerb = (typeof sequence.current.lastuser != 'undefined') ? 'updated' : 'deleted';
                });


                if(isSummary){
                    summaryOpts = {
                        currentFileName: sequence.current.file_name,
                        currentFileUrl: sequence.current.download_url,
                        currentFileDeleteUrl: sequence.current.delete_url,
                        historyCount: iHistoryCount,
                        historyHide: (iHistoryCount > 0) ? '' : 'starthidden'
                    }
                };

                // Complete history including current item:
                //sequence.versions

                var sSummary = (isSummary) ? wfApp.wfTemplate(tplSumm, summaryOpts) : '',
                    controlOpts = {
                        uploadURL: sequence.upload_url,
                        site: auth.site,
                        mpsid: auth.mpsid,
                        appCode: auth.appCode,
                        xsrf: auth._xsrf,
                        existingSummary: sSummary,
                        starthidden: (isSummary) ? 'starthidden':'',
                        notstarthidden: (isSummary) ? '':'starthidden',
                        domGuid: wfApp._createUniqueID('up'),
                        history: (sequence.versions.length > 0) ? wfApp.wfTemplate(tplHist, sequence.versions) : '',
                        current: (typeof sequence.current.lastuser != 'undefined') ? wfApp.wfTemplate(tplHist, sequence.current) : '',
                        singleMultipleClass: ($this.options.item.data.sequence_list.length < 2) ? 'wf-upload-single' : 'wf-upload-multiple',
                        historyCount: iHistoryCount,
                        historyHide: (iHistoryCount > 0 && !isSummary) ? '' : 'starthidden'
                    };

                sContent += wfApp.wfTemplate(tplItem, controlOpts);
            });

            var tplWrap = $('#wf-workflow-upload-wrapper').html(),
                item = $this.options.item,
                data = {
                    widget: sContent,
                    header: $this.getCommonHeader(),
                    backLink: '<div class="wf-details-form-btn-bar col-xs-12"><a data-section="wf-overview-item" class="overview-breadcrumb wf-details-footer-cancel" href="#"><span class="glyphicon glyphicon-circle-arrow-left"></span><span>'+((item.common.is_complete)?'Back':'Cancel')+'</span></a></div>'
                };
            // ($this.options.item.data.sequence_list.length < 2)
            sContent = $(wfApp.wfTemplate(tplWrap, data));

            // Special Complete Single Upload state:
            if(isSingle && $this.options.item.common.is_complete){
                return sContent;
            }

            return sContent;
        },

        _bindings: function(){
            var $this = this,
                $that = $this,
                $el = $this.element;

            $el.on('fileselect', '.btn-file :file', function(event, label) {
                var $target = $(event.target),
                    $form = $target.closest('form');
                $target.closest('.row').find('input').prop('disabled',false);
                $target.closest('.row').find('.btn').toggleClass('btn-primary btn-default');
                $target.closest('.input-group').find('.cv-import-label').val(label);
                $target.closest('.row').find('input:first').show().focus().click().val('Uploading...').prop('disabled', true);

                // Asynchronous IFrame POST:
                _uploadWidget = $that;
                $('#wf-modal-backdrop').show().removeClass('starthidden');
                cvApp.showHeaderMessage('Uploading file...', 'info', true);
                $form.submit();
                event.stopPropagation();

            });

            $el.on('change', '.btn-file :file', function(e) {
                var input = $(e.target),
                    label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
                input.trigger('fileselect', [label]);
                e.stopPropagation();
            });

            $el.on('click', '.wf-common-header .wf-replace-file', function(e){
                var $this = $(this),
                    $controls = $this.closest('.wf-itemWidgetWRapper').find('.wf-upload-inputs').toggle();
            });
            $el.on('click', 'form .wf-replace-file', function(e){
                var $this = $(this),
                    $controls = $this.closest('.wf-uploaded-summary').siblings('.wf-upload-inputs').toggle();
            });
            $el.on('click', 'form .wf-upload-cancel', function(e){
                var $this = $(this),
                    $controls = $this.closest('.wf-upload-inputs').toggle();
            });
            $el.on('click', 'form .wf-item-history-toggle', function(e){
                var $this = $(this),
                    $target = $this.closest('form').find('.wf-item-history'),
                    $chevrons = $target.find('.glyphicon');

                    $target.toggleClass('item-history-closed');
                    $this = $(this).find('.glyphicon').toggleClass('glyphicon-chevron-down glyphicon-chevron-up');
            });

            $el.on('click', '.deleteMarinaBtn', function(event){
                var $this = $(this), sURL = ($this.is('[data-wf-url]')) ? $this.data('wfUrl') : $this.closest('[data-wf-url]').data('wfUrl');
                _uploadWidget = $that;
                var $workflowWidget = $('#workflow-content').data('wfWidgets-workFlowPage');
                $workflowWidget.uxStates.lastActionType = 'deleteExistingFile';
                cvApp.ubiquitousPageRequest({
                    url: sURL,
                    data: JSON.stringify(ajaxPayload),
                    errorMessage: '#modalerrormessage',
                    success: function(data){
                        $that._globalResponseHandler(data, false, false);
                    }
                });
            });

        }
    });



});