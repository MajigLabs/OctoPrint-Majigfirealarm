$(function() {
    function MajigFirealarmViewModel(parameters) {
        var self = this;

        self.alarmStatus = ko.observable();

        self.fromResponse = function(response){
            if (response.status === "FIRE"){
                //debugger;
                self.sendStop();
                //alert("testing attempting to do firealarm stop");
            }
            $("#majigfirealarm-span").text(response.status);
        };

        self.getStatus = function(){
            $.ajax({
                url: API_BASEURL + "plugin/majigfirealarm",
                type: "GET",
                dataType: "json",
                success: self.fromResponse
            });	
        };

        self.sendStop = function(){
            $.ajax({
                url: API_BASEURL + "plugin/majigfirealarm",
                type: "POST",
                dataType: "json",
                data: JSON.stringify({
                    command: "emergencyStop"
                }),
                contentType: "application/json; charset=UTF-8",
                success: function (data, status) {
                    alert('Fire alarm! Shutting off machine')
                }
            });
        }

        self.timeout = null;

        self.startLoop = function(){
            self.timeout = setInterval(self.getStatus, 1000);
        };

        self.stopLoop = function(){
            clearInterval(self.timeout);
        };

    }


    // This is how our plugin registers itself with the application, by adding some configuration
    // information to the global variable OCTOPRINT_VIEWMODELS
    ADDITIONAL_VIEWMODELS.push([
        // This is the constructor to call for instantiating the plugin
        MajigFirealarmViewModel,

        // This is a list of dependencies to inject into the plugin, the order which you request
        // here is the order in which the dependencies will be injected into your view model upon
        // instantiation via the parameters argument
        [],

        // Finally, this is the list of selectors for all elements we want this view model to be bound to.
	    ["#sidebar_plugin_majigfirealarm"]
    ]);

});
