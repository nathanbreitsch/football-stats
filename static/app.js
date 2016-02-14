$(function(){
  function ViewModel(){
    var self = this;

    self.quarterbacks = ko.observableArray();
    self.positionOptions = ["quarterback"];
    self.quarterOptions = ko.observableArray(['All','1','2','3','4','5']);
    self.downOptions = ko.observableArray(['All','1','2', '3', '4']);
    self.selectedDown = ko.observableArray([]);
    self.selectedQuarter = ko.observableArray([]);
    self.selectedPosition = ko.observable("quarterback");

    self.selectedDown.subscribe(function(){self.getQuarterbackStats(); console.log('hello')});
    self.selectedQuarter.subscribe(function(){self.getQuarterbackStats();});

    self.getQuarterbackStats = function(){
      reqwest({
        url: 'http://localhost:8000/quarterback/stats',
        type: 'json',
        method: 'post',
        crossOrigin: true,
        headers: {
          //'Access-Control-Request-Headers': 'x-requested-with',
          //'Access-Control-Allow-Credentials': true
        },
        data: {
            action_type: self.selectedPosition(),
            down: self.selectedDown(),
            quarter: self.selectedQuarter()
        }
      })
      .then(function (resp) {
        self.quarterbacks(resp.quarterbacks)
        $("#stats-table").tablesorter();
        $(".select2").chosen();
      }, function (err, msg) {
        console.error(err);
      });
    };

    self.getQuarterbackStats();
  }

  ko.applyBindings(new ViewModel())
})
