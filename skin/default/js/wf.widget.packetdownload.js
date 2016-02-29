// [Copyright]
// SmartPath v1.0
// Copyright 2014-2015 Mountain Pass Solutions, Inc.
// This unpublished material is proprietary to Mountain Pass Solutions, Inc.
// [End Copyright]

 $(function() {
    $.widget( "wfWidgets.packetDownloadWidget", {
        options: {
            item: false,
            auth: false
        },

        _create: function(){
            var $this = this,
                $element = $this.element;

            // New: Common Config States for each Widget Instance (for non-selector based OO code later)
            $this.states = {};
            $this.states = $this.options.item.common;

            // Make HTML -> jQ obj:
            $this.$form = $($this._createForm());
            // RENDER:
            $this.element.append($this.$form);

            // LOGIC HERE: This is where to do Disable, Hide/Show, etc on the above obj...
            if($this.options.item.data.disabled === true){
                 $this.$form.find('input, textarea, button, select').attr('disabled', 'disabled');
            }

        },

        _createForm: function(){
            var $this = this,
                item = $this.options.item,
                auth = $this.options.auth,
                tplForm = $('#wf-workflow-packetdownload').html(),
                sGuid = wfApp._createUniqueID('GUID_'+wfApp._safeDomGuid(item.common.descr)),
                data = {
                    url: item.data.url,
                    name: item.common.descr
                };

            return wfApp.wfTemplate(tplForm, data);
        }
    });
});
