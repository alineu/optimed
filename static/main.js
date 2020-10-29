(function () {

  'use strict';

  angular.module('WordcountApp', [])

  .controller('WordcountController', ['$scope', '$log', '$http', '$timeout',
    function($scope, $log, $http, $timeout) {

    $scope.submitButtonText = 'Submit';
    $scope.loading = false;
    $scope.urlerror = false;

    $scope.getResults = function() {

      $log.log('test');

      // get the URL from the input
      var userInput = $scope.url;

      // fire the API request
      $http.post('/start', {'url': userInput}).
        success(function(results) {
          $log.log(results);
          getWordCount(results);
          $scope.optimed_search_results = null;
          $scope.loading = true;
          $scope.submitButtonText = 'Loading...';
          $scope.urlerror = false;
        }).
        error(function(error) {
          $log.log(error);
        });

    };

    // $scope.submitButtonText = 'Find';
    // $scope.loading = false;
    // $scope.urlerror = false;

    // $scope.findMeds = function() {

    //   // get the URL from the input
    //   var userCond = $scope.user_condition;

    //   // fire the API request
    //   $http.post('/fidnmed', {'user_condition': userCond}).
    //     success(function(results) {
    //       $log.log(results);
    //       getWordCount(results);
    //       $scope.wordcounts = null;
    //       $scope.loading = true;
    //       $scope.submitButtonText = 'Loading...';
    //       $scope.urlerror = false;
    //     }).
    //     error(function(error) {
    //       $log.log(error);
    //     });

    // };

    function getWordCount(jobID) {

      var timeout = '';

      var poller = function() {
        // fire another request
        $http.get('/results/'+jobID).
          success(function(data, status, headers, config) {
            if(status === 202) {
              $log.log(data, status);
            } else if (status === 200){
              $log.log(data);
              $scope.loading = false;
              $scope.submitButtonText = "Submit";
              $scope.optimed_search_results = data;
              $timeout.cancel(timeout);
              return false;
            }
            // continue to call the poller() function every 2 seconds
            // until the timeout is cancelled
            timeout = $timeout(poller, 2000);
          }).
          error(function(error) {
            $log.log(error);
            $scope.loading = false;
            $scope.submitButtonText = "Submit";
            $scope.urlerror = true;
          });
      };

      poller();

    }

  }])

  .directive('wordCountChart', ['$parse', function ($parse) {
    return {
      restrict: 'E',
      replace: true,
      template: '<div id="chart"></div>',
      link: function (scope) {
        scope.$watch('optimed_search_results', function() {
          d3.select('#chart').selectAll('*').remove();
          var data = scope.optimed_search_results;
          for (var item in data) {
            // var drug = data[item][0];
            // var price = data[item][1];
            d3.select('#chart')
              .append('div')
              .selectAll('div')
              .data(item[0])
              .enter()
              .append('div')
              .style('width', function() {
                return (data[item] * 20) + 'px';
              })
              .text(function(d){
                return item;
              });
          }
        }, true);
      }
     };
  }]);

}());
